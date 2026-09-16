import pygame

from karma.entities.buildings.building import Building
from karma.entities.buildings.coal_plant import CoalPlant
from karma.entities.buildings.energy_producer import EnergyProducer
from karma.entities.buildings.solar_panel import SolarPanel
from karma.entities.buildings.turret import Turret
from karma.entities.buildings.wall import Wall
from karma.entities.enemies.enemy import Enemy
from karma.entities.projectile import Projectile
from karma.enums import BuildingKind, RessourceType
from karma.environment.map import MapManager
from karma.resources.ressourceManager import RessourceManager
from karma.settings import (
    ASSETS_DIR,
    COAL_PLANT_COST,
    COAL_PLANT_HEALTH,
    COAL_PLANT_PRODUCTION_AMOUNT,
    COAL_PLANT_PRODUCTION_INTERVAL,
    SOLAR_PANEL_COST,
    SOLAR_PANEL_HEALTH,
    SOLAR_PANEL_PRODUCTION_AMOUNT,
    SOLAR_PANEL_PRODUCTION_INTERVAL,
    TURRET_ATTACK_INTERVAL,
    TURRET_COST,
    TURRET_DAMAGE,
    TURRET_HEALTH,
    TURRET_RANGE,
    WALL_COST,
    WALL_HEALTH,
)

_PROJECTILE_FRAME_SIZE = 8
_PROJECTILE_DRAW_SIZE = (16, 16)


class BuildSlot:
    # Emplacement constructible fixe défini sur la map (calque "BuildSlots")

    def __init__(self, name: str, position: pygame.Vector2, size: tuple[int, int]) -> None:
        self.name: str = name
        self.position: pygame.Vector2 = position
        self.size: tuple[int, int] = size
        self.building: Building | None = None

    def isEmpty(self) -> bool:
        return self.building is None or self.building.isDestroyed()

    def center(self) -> pygame.Vector2:
        return self.position + pygame.Vector2(self.size[0] / 2, self.size[1] / 2)


class CatalogEntry:
    # Une ligne du menu de construction (touche 1-4)

    def __init__(self, kind: BuildingKind, key: int, label: str, energyCost: int, requiresSlot: bool) -> None:
        self.kind: BuildingKind = kind
        self.key: int = key
        self.label: str = label
        self.energyCost: int = energyCost
        self.requiresSlot: bool = requiresSlot


BUILDING_CATALOG: list[CatalogEntry] = [
    CatalogEntry(BuildingKind.SolarPanel, 1, "Panneau solaire", SOLAR_PANEL_COST, requiresSlot=True),
    CatalogEntry(BuildingKind.CoalPlant, 2, "Centrale à charbon", COAL_PLANT_COST, requiresSlot=True),
    CatalogEntry(BuildingKind.Wall, 3, "Mur", WALL_COST, requiresSlot=False),
    CatalogEntry(BuildingKind.Turret, 4, "Tourelle", TURRET_COST, requiresSlot=False),
]


class BuildingSystem:
    # Gère les emplacements constructibles, la construction et le fonctionnement des bâtiments

    def __init__(self, mapManager: MapManager) -> None:
        self.slots: list[BuildSlot] = []
        for obj in mapManager.get_build_slots():
            size = (int(obj.width), int(obj.height))
            self.slots.append(BuildSlot(obj.name, pygame.Vector2(obj.x, obj.y), size))

        # Murs/tourelles posés librement sur la carte (pas dans un slot)
        self.freeBuildings: list[Building] = []
        self.projectiles: list[Projectile] = []
        self.projectileFrames = self._loadProjectileFrames()

        self.activeSlot: BuildSlot | None = None
        self.activePosition: pygame.Vector2 | None = None

    def _loadProjectileFrames(self) -> list[pygame.Surface]:
        sheet = pygame.image.load(ASSETS_DIR / "Projectiles" / "bullets+plasma.png").convert_alpha()
        frames = []
        for i in (1, 2):  # les deux frames "plasma" du sheet (la frame 0 est un simple pixel de balle)
            rect = pygame.Rect(i * _PROJECTILE_FRAME_SIZE, 0, _PROJECTILE_FRAME_SIZE, _PROJECTILE_FRAME_SIZE)
            frame = sheet.subsurface(rect).copy()
            frames.append(pygame.transform.scale(frame, _PROJECTILE_DRAW_SIZE))
        return frames

    def getWalls(self) -> list[Wall]:
        # Utilisé par le CombatSystem pour savoir quels murs bloquent les ennemis
        walls = []
        for slot in self.slots:
            if isinstance(slot.building, Wall) and not slot.building.isDestroyed():
                walls.append(slot.building)
        for building in self.freeBuildings:
            if isinstance(building, Wall) and not building.isDestroyed():
                walls.append(building)
        return walls

    def findNearestEmptySlot(self, position: pygame.Vector2, maxDistance: float) -> BuildSlot | None:
        nearest = None
        nearestDistance = maxDistance
        for slot in self.slots:
            if not slot.isEmpty():
                continue
            distance = position.distance_to(slot.center())
            if distance <= nearestDistance:
                nearest = slot
                nearestDistance = distance
        return nearest

    def findNearestUpgradable(self, position: pygame.Vector2, maxDistance: float) -> EnergyProducer | None:
        nearest = None
        nearestDistance = maxDistance
        for slot in self.slots:
            building = slot.building
            if not isinstance(building, EnergyProducer) or not building.canUpgrade():
                continue
            distance = position.distance_to(slot.center())
            if distance <= nearestDistance:
                nearest = building
                nearestDistance = distance
        return nearest

    def canPlaceFreely(self, position: pygame.Vector2, baseRect: pygame.Rect) -> bool:
        # Un mur/une tourelle ne peut pas se poser dans un build slot, sur la base, ni
        # sur un bâtiment déjà en place
        newRect = pygame.Rect(int(position.x), int(position.y), *Building.SIZE)
        if newRect.colliderect(baseRect):
            return False

        for slot in self.slots:
            slotRect = pygame.Rect(int(slot.position.x), int(slot.position.y), *slot.size)
            if newRect.colliderect(slotRect):
                return False
            if slot.building is not None and not slot.building.isDestroyed():
                buildingRect = pygame.Rect(int(slot.building.position.x), int(slot.building.position.y), *slot.building.SIZE)
                if newRect.colliderect(buildingRect):
                    return False

        for building in self.freeBuildings:
            if building.isDestroyed():
                continue
            buildingRect = pygame.Rect(int(building.position.x), int(building.position.y), *building.SIZE)
            if newRect.colliderect(buildingRect):
                return False

        return True

    def isMenuOpen(self) -> bool:
        return self.activeSlot is not None or self.activePosition is not None

    def interact(self, position: pygame.Vector2, maxDistance: float, resourceManager: RessourceManager, baseRect: pygame.Rect) -> None:
        # E fait tout : construction sur slot vide, sinon pose libre de mur/tourelle, sinon amélioration
        if self.isMenuOpen():
            self.closeMenu()
            return

        slot = self.findNearestEmptySlot(position, maxDistance)
        if slot is not None:
            self.activeSlot = slot
            return

        freePosition = position - pygame.Vector2(Building.SIZE[0] / 2, Building.SIZE[1] / 2)
        if self.canPlaceFreely(freePosition, baseRect):
            self.activePosition = freePosition
            return

        self.tryUpgradeNear(position, maxDistance, resourceManager)

    def closeMenu(self) -> None:
        self.activeSlot = None
        self.activePosition = None

    def closeMenuIfOutOfRange(self, position: pygame.Vector2, maxDistance: float) -> None:
        # Évite de construire "à distance" si le joueur s'éloigne pendant que le menu est ouvert
        if self.activeSlot is not None and position.distance_to(self.activeSlot.center()) > maxDistance:
            self.closeMenu()
        if self.activePosition is not None and position.distance_to(self.activePosition) > maxDistance:
            self.closeMenu()

    def build(self, key: int, resourceManager: RessourceManager) -> bool:
        entry = None
        for candidate in BUILDING_CATALOG:
            if candidate.key == key:
                entry = candidate
        if entry is None:
            return False

        if entry.requiresSlot:
            if self.activeSlot is None or not self.activeSlot.isEmpty():
                return False
            position = self.activeSlot.position
        else:
            if self.activePosition is None:
                return False
            position = self.activePosition

        if not resourceManager.hasEnough(RessourceType.Energy, entry.energyCost):
            return False
        resourceManager.consume(RessourceType.Energy, entry.energyCost)

        if entry.kind == BuildingKind.SolarPanel:
            building = SolarPanel(position, SOLAR_PANEL_HEALTH, SOLAR_PANEL_COST, SOLAR_PANEL_PRODUCTION_AMOUNT, SOLAR_PANEL_PRODUCTION_INTERVAL)
        elif entry.kind == BuildingKind.CoalPlant:
            building = CoalPlant(position, COAL_PLANT_HEALTH, COAL_PLANT_COST, COAL_PLANT_PRODUCTION_AMOUNT, COAL_PLANT_PRODUCTION_INTERVAL)
        elif entry.kind == BuildingKind.Wall:
            building = Wall(position, WALL_HEALTH, WALL_COST)
        else:
            building = Turret(position, TURRET_HEALTH, TURRET_COST, TURRET_RANGE, TURRET_DAMAGE, TURRET_ATTACK_INTERVAL)

        if entry.requiresSlot:
            self.activeSlot.building = building
        else:
            self.freeBuildings.append(building)

        self.closeMenu()
        return True

    def tryUpgradeNear(self, position: pygame.Vector2, maxDistance: float, resourceManager: RessourceManager) -> bool:
        # Achat unique, pas de conso continue ensuite
        building = self.findNearestUpgradable(position, maxDistance)
        if building is None:
            return False

        energyCost = building.UPGRADE_ENERGY_COST
        rawMaterialCost = building.UPGRADE_RAW_MATERIAL_COST
        if not resourceManager.hasEnough(RessourceType.Energy, energyCost):
            return False
        if not resourceManager.hasEnough(RessourceType.RawMaterial, rawMaterialCost):
            return False

        resourceManager.consume(RessourceType.Energy, energyCost)
        resourceManager.consume(RessourceType.RawMaterial, rawMaterialCost)
        building.upgrade()
        return True

    def _updateBuilding(self, building: Building, dt: float, isDay: bool, resourceManager: RessourceManager, enemies: list[Enemy]) -> None:
        resourceManager.applyKarmaDelta(building.getKarmaImpact(dt))

        if isinstance(building, EnergyProducer):
            building.updateAnimation(dt, isDay)
            produced = building.tryProduce(dt)
            if produced:
                resourceManager.add(RessourceType.Energy, produced)
        elif isinstance(building, Turret):
            target = building.update(dt, enemies)
            if target is not None:
                self.projectiles.append(Projectile(building.getMuzzlePosition(), target.position, self.projectileFrames))

    def update(self, dt: float, isDay: bool, resourceManager: RessourceManager, enemies: list[Enemy]) -> None:
        for slot in self.slots:
            building = slot.building
            if building is None:
                continue
            if building.isDestroyed():
                slot.building = None
                continue
            self._updateBuilding(building, dt, isDay, resourceManager, enemies)

        for building in self.freeBuildings:
            if building.isDestroyed():
                continue
            self._updateBuilding(building, dt, isDay, resourceManager, enemies)
        self.freeBuildings = [b for b in self.freeBuildings if not b.isDestroyed()]

        for projectile in self.projectiles:
            projectile.update(dt)
        self.projectiles = [p for p in self.projectiles if not p.reached]

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        for slot in self.slots:
            if slot.building is not None and not slot.building.isDestroyed():
                slot.building.draw(screen, camera)
        for building in self.freeBuildings:
            building.draw(screen, camera)
        for projectile in self.projectiles:
            projectile.draw(screen, camera)

import pygame

from karma.enums import BuildingKind, RessourceType
from karma.resources.ressourceManager import RessourceManager
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH
from karma.systems.building import BUILDING_CATALOG, BuildingSystem

_ICON_SIZE = (36, 36)
_ROW_HEIGHT = 44
_PANEL_WIDTH = 380
_PANEL_HEIGHT = 230


class BuildMenu:
    # Affiche l'indice de construction au sol et le menu de sélection (touches 1-4)

    def __init__(self) -> None:
        self.promptFont = pygame.font.Font(None, 22)
        self.labelFont = pygame.font.Font(None, 26)
        self.titleFont = pygame.font.Font(None, 30)

        solarPath = ASSETS_DIR / "buildings" / "solar_panel" / "day" / "top_view.png"
        coalPath = ASSETS_DIR / "buildings" / "coal_plant" / "day" / "top_view.png"
        self.solarIcon = pygame.transform.scale(pygame.image.load(solarPath).convert_alpha(), _ICON_SIZE)
        self.coalIcon = pygame.transform.scale(pygame.image.load(coalPath).convert_alpha(), _ICON_SIZE)

    def drawWorld(
        self,
        surface: pygame.Surface,
        camera,
        buildingSystem: BuildingSystem,
        playerPosition: pygame.Vector2,
        maxDistance: float,
    ) -> None:
        # Surligne un slot vide ou un producteur améliorable à portée
        # (la pose libre de mur/tourelle marche presque partout, donc pas de surlignage pour elle)
        if buildingSystem.isMenuOpen():
            return

        slot = buildingSystem.findNearestEmptySlot(playerPosition, maxDistance)
        if slot is not None:
            topLeft = camera.apply(slot.position) if camera else slot.position
            rect = pygame.Rect(int(topLeft.x), int(topLeft.y), *slot.size)
            pygame.draw.rect(surface, (255, 230, 120), rect, 2)

            promptSurf = self.promptFont.render("[E] Construire", False, (255, 230, 120))
            promptRect = promptSurf.get_rect(midbottom=(rect.centerx, rect.top - 4))
            surface.blit(promptSurf, promptRect)
            return

        building = buildingSystem.findNearestUpgradable(playerPosition, maxDistance)
        if building is None:
            return

        topLeft = camera.apply(building.position) if camera else building.position
        rect = pygame.Rect(int(topLeft.x), int(topLeft.y), *building.SIZE)
        pygame.draw.rect(surface, (120, 220, 255), rect, 2)

        costText = f"[E] Améliorer — {building.UPGRADE_ENERGY_COST} Énergie + {building.UPGRADE_RAW_MATERIAL_COST} Matière première"
        promptSurf = self.promptFont.render(costText, False, (120, 220, 255))
        promptRect = promptSurf.get_rect(midbottom=(rect.centerx, rect.top - 4))
        surface.blit(promptSurf, promptRect)

    def drawPanel(self, screen: pygame.Surface, buildingSystem: BuildingSystem, resourceManager: RessourceManager) -> None:
        if not buildingSystem.isMenuOpen():
            return

        panelRect = pygame.Rect(0, 0, _PANEL_WIDTH, _PANEL_HEIGHT)
        panelRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        panelSurf = pygame.Surface((panelRect.width, panelRect.height))
        panelSurf.set_alpha(235)
        panelSurf.fill((15, 15, 22))
        screen.blit(panelSurf, panelRect)
        pygame.draw.rect(screen, (255, 255, 255), panelRect, 2)

        titleSurf = self.titleFont.render("Construire", False, "white")
        screen.blit(titleSurf, (panelRect.left + 14, panelRect.top + 10))

        availableEnergy = resourceManager.getStock(RessourceType.Energy)
        onSlot = buildingSystem.activeSlot is not None
        entries = [entry for entry in BUILDING_CATALOG if entry.requiresSlot == onSlot]

        y = panelRect.top + 44
        for entry in entries:
            affordable = availableEnergy >= entry.energyCost
            textColor = (255, 255, 255) if affordable else (100, 100, 100)

            if entry.kind == BuildingKind.SolarPanel:
                icon = self.solarIcon
            elif entry.kind == BuildingKind.CoalPlant:
                icon = self.coalIcon
            else:
                icon = None

            x = panelRect.left + 14
            if icon is not None:
                iconSurf = icon if affordable else self._dim(icon)
                screen.blit(iconSurf, (x, y))

            labelX = x + (_ICON_SIZE[0] + 10 if icon is not None else 0)
            text = f"[{entry.key}] {entry.label} — {entry.energyCost} Énergie"
            textSurf = self.labelFont.render(text, False, textColor)
            textRect = textSurf.get_rect(midleft=(labelX, y + _ICON_SIZE[1] // 2))
            screen.blit(textSurf, textRect)

            y += _ROW_HEIGHT

        hintSurf = self.promptFont.render("Échap pour annuler", False, (180, 180, 180))
        screen.blit(hintSurf, (panelRect.left + 14, panelRect.bottom - 26))

    def _dim(self, surface: pygame.Surface) -> pygame.Surface:
        # Transparence = pas assez de ressources
        dimmed = surface.copy()
        dimmed.set_alpha(90)
        return dimmed

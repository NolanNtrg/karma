import pygame

from karma.entities.buildings.building import Building
from karma.settings import ASSETS_DIR


class EnergyProducer(Building):
    # Base des bâtiments qui produisent de l'Énergie à intervalle régulier.

    # Dossier dans assets/buildings/, avec des sous-dossiers day/ et night/
    ASSET_FOLDER: str | None = None

    # None = pas d'amélioration dispo pour ce bâtiment
    UPGRADE_ENERGY_COST: int | None = None
    UPGRADE_RAW_MATERIAL_COST: int | None = None
    UPGRADE_PRODUCTION_AMOUNT: int | None = None
    UPGRADE_PRODUCTION_INTERVAL: float | None = None

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        karmaImpact: float,
        productionAmount: int,
        productionInterval: float,
    ) -> None:
        super().__init__(position, health, energyCost, karmaImpact)
        self.productionAmount: int = productionAmount
        self.productionInterval: float = productionInterval
        self.timeSinceLastProduction: float = 0.0
        self.isUpgraded: bool = False

        self.dayFrames: list[pygame.Surface] = []
        self.nightFrames: list[pygame.Surface] = []
        self.imageIndex: float = 0.0
        self.image: pygame.Surface | None = None
        if self.ASSET_FOLDER is not None:
            self._loadSprites()

    def canUpgrade(self) -> bool:
        return not self.isUpgraded and self.UPGRADE_PRODUCTION_AMOUNT is not None

    def upgrade(self) -> None:
        # Ne change que le rythme de production : le coût est prélevé par l'appelant
        self.productionAmount = self.UPGRADE_PRODUCTION_AMOUNT
        self.productionInterval = self.UPGRADE_PRODUCTION_INTERVAL
        self.isUpgraded = True

    def _loadSprites(self) -> None:
        folder = ASSETS_DIR / "buildings" / self.ASSET_FOLDER
        for i in range(1, 5):
            imgDay = pygame.image.load(folder / "day" / f"idle_{i}.png").convert_alpha()
            self.dayFrames.append(pygame.transform.scale(imgDay, self.SIZE))
            imgNight = pygame.image.load(folder / "night" / f"idle_{i}.png").convert_alpha()
            self.nightFrames.append(pygame.transform.scale(imgNight, self.SIZE))
        self.image = self.dayFrames[0]

    def updateAnimation(self, dt: float, isDay: bool) -> None:
        # Ne fait rien pour les bâtiments sans sprite dédié
        if not self.dayFrames:
            return
        frames = self.dayFrames if isDay else self.nightFrames
        self.imageIndex += dt * 0.006
        self.image = frames[int(self.imageIndex) % len(frames)]

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        if not self.dayFrames or self.image is None:
            super().draw(screen, camera)
        else:
            position = camera.apply(self.position) if camera else self.position
            screen.blit(self.image, position)

        if self.isUpgraded:
            # Pas de sprite différent pour la version rapide, donc badge
            position = camera.apply(self.position) if camera else self.position
            badgeCenter = (int(position.x + self.SIZE[0] - 6), int(position.y + 6))
            pygame.draw.circle(screen, (255, 220, 60), badgeCenter, 5)
            pygame.draw.circle(screen, (20, 20, 20), badgeCenter, 5, 1)

    def tryProduce(self, dt: float) -> int:
        # Retourne l'Énergie produite pour cette frame, ou 0 si nécessaire.
        if not self.isOperational():
            return 0
        self.timeSinceLastProduction += dt
        if self.timeSinceLastProduction >= self.productionInterval:
            self.timeSinceLastProduction = 0.0
            return self.productionAmount
        return 0

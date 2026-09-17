from pathlib import Path

import pygame

from karma.entities.buildings.building import Building
from karma.settings import ASSETS_DIR


class EnergyProducer(Building):
    # Base des bâtiments qui produisent de l'Énergie à intervalle régulier.

    SIZE: tuple[int, int] = (64, 64)
    FRAME_COUNT: int = 4

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        karmaImpact: float,
        productionAmount: int,
        productionInterval: float,
        spriteFolder: str,
    ) -> None:
        super().__init__(position, health, energyCost, karmaImpact)
        self.productionAmount: int = productionAmount
        self.productionInterval: float = productionInterval
        self.timeSinceLastProduction: float = 0.0

        spritesDir = ASSETS_DIR / "buildings" / spriteFolder

        def loadFrame(path: Path) -> pygame.Surface:
            return pygame.transform.scale(pygame.image.load(path).convert_alpha(), self.SIZE)

        dayFrames = [loadFrame(spritesDir / "day" / f"idle_{i}.png") for i in range(1, self.FRAME_COUNT + 1)]
        nightFrames = [loadFrame(spritesDir / "night" / f"idle_{i}.png") for i in range(1, self.FRAME_COUNT + 1)]
        self.setFrames(dayFrames, nightFrames)

    def tryProduce(self, dt: float) -> int:
        # Retourne l'Énergie produite pour cette frame, ou 0 si nécessaire.
        if self.isDestroyed():
            return 0
        self.timeSinceLastProduction += dt
        if self.timeSinceLastProduction >= self.productionInterval:
            self.timeSinceLastProduction = 0.0
            return self.productionAmount
        return 0

    def update(self, dt: float, isDay: bool) -> None:
        self.updateSprite(dt, isDay)

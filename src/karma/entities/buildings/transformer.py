import pygame

from karma.entities.buildings.building import Building


class Transformer(Building):
    # Base des bâtiments qui transforment la matière première en énergie

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        karmaImpact: float,
        rawMaterialCost: int,
        energyOutput: int,
        transformInterval: float,
    ) -> None:
        super().__init__(position, health, energyCost, karmaImpact)
        self.rawMaterialCost: int = rawMaterialCost
        self.energyOutput: int = energyOutput
        self.transformInterval: float = transformInterval
        self.timeSinceLastTransform: float = 0.0

    def tryTransform(self, dt: float, availableRawMaterial: int) -> int:
        # Retourne l'énergie produite, ou 0 si la transformation est impossible.
        # Le stock est retiré par l'appelant après une transformation réussie.
        if not self.isOperational():
            return 0
        self.timeSinceLastTransform += dt
        if self.timeSinceLastTransform < self.transformInterval:
            return 0
        if availableRawMaterial < self.rawMaterialCost:
            return 0
        self.timeSinceLastTransform = 0.0
        return self.energyOutput

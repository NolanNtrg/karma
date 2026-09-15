import pygame

from karma.entities.buildings.building import Building


class EnergyProducer(Building):
    # Base des bâtiments qui produisent de l'Énergie à intervalle régulier.

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

    def tryProduce(self, dt: float) -> int:
        # Retourne l'Énergie produite pour cette frame, ou 0 si nécessaire.
        if not self.isOperational():
            return 0
        self.timeSinceLastProduction += dt
        if self.timeSinceLastProduction >= self.productionInterval:
            self.timeSinceLastProduction = 0.0
            return self.productionAmount
        return 0

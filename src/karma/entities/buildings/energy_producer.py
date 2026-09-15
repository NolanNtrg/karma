import pygame

from karma.entities.buildings.building import Building


class EnergyProducer(Building):
    # Classe mère des bâtiments de production d'Énergie : produit une quantité
    # fixe d'Énergie à intervalle régulier tant qu'il est opérationnel

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
        # dt : temps écoulé depuis la dernière frame, en millisecondes
        # Retourne l'Énergie produite ce frame (0 si inactif, détruit ou pas encore prêt)
        if not self.isOperational():
            return 0
        self.timeSinceLastProduction += dt
        if self.timeSinceLastProduction >= self.productionInterval:
            self.timeSinceLastProduction = 0.0
            return self.productionAmount
        return 0

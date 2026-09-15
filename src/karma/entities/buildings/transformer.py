import pygame

from karma.entities.buildings.building import Building


class Transformer(Building):
    # Classe mère des bâtiments de transformation : convertit de la Matière première
    # en Énergie à intervalle régulier tant qu'il est opérationnel

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
        # dt : temps écoulé depuis la dernière frame, en millisecondes
        # availableRawMaterial : stock de Matière première actuellement disponible
        # Retourne l'Énergie produite ce frame (0 si inactif, détruit, pas encore prêt
        # ou si le stock de Matière première est insuffisant). Ne déduit pas le stock
        # lui-même : c'est à l'appelant de retirer rawMaterialCost s'il reçoit un résultat
        if not self.isOperational():
            return 0
        self.timeSinceLastTransform += dt
        if self.timeSinceLastTransform < self.transformInterval:
            return 0
        if availableRawMaterial < self.rawMaterialCost:
            return 0
        self.timeSinceLastTransform = 0.0
        return self.energyOutput

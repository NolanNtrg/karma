import pygame

from karma.entities.buildings.energy_producer import EnergyProducer


class SolarPanel(EnergyProducer):
    # Panneau solaire : variante propre et lente de la production d'Énergie
    # Fait monter le karma tant qu'il est actif

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        productionAmount: int,
        productionInterval: float,
    ) -> None:
        super().__init__(position, health, energyCost, 1.0, productionAmount, productionInterval)

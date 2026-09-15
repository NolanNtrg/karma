import pygame

from karma.entities.buildings.energy_producer import EnergyProducer


class CoalPlant(EnergyProducer):
    # Centrale à charbon : variante sale et rapide de la production d'Énergie
    # Fait baisser le karma tant qu'elle est active

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        productionAmount: int,
        productionInterval: float,
    ) -> None:
        super().__init__(position, health, energyCost, -1.0, productionAmount, productionInterval)

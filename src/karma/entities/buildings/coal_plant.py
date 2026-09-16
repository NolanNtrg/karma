import pygame

from karma.entities.buildings.energy_producer import EnergyProducer
from karma.settings import ASSETS_DIR


class CoalPlant(EnergyProducer):
    # Centrale rapide qui diminue le karma.

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        productionAmount: int,
        productionInterval: float,
    ) -> None:
        super().__init__(position, health, energyCost, -100.0, productionAmount, productionInterval, "coal_plant")

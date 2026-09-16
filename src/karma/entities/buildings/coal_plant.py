import pygame

from karma.entities.buildings.energy_producer import EnergyProducer
from karma.settings import (
    COAL_UPGRADE_ENERGY_COST,
    COAL_UPGRADE_PRODUCTION_AMOUNT,
    COAL_UPGRADE_PRODUCTION_INTERVAL,
    COAL_UPGRADE_RAW_MATERIAL_COST,
)


class CoalPlant(EnergyProducer):
    # Centrale rapide qui diminue le karma.

    ASSET_FOLDER = "coal_plant"

    UPGRADE_ENERGY_COST = COAL_UPGRADE_ENERGY_COST
    UPGRADE_RAW_MATERIAL_COST = COAL_UPGRADE_RAW_MATERIAL_COST
    UPGRADE_PRODUCTION_AMOUNT = COAL_UPGRADE_PRODUCTION_AMOUNT
    UPGRADE_PRODUCTION_INTERVAL = COAL_UPGRADE_PRODUCTION_INTERVAL

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        productionAmount: int,
        productionInterval: float,
    ) -> None:
        super().__init__(position, health, energyCost, -100.0, productionAmount, productionInterval)

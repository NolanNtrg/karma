import pygame

from karma.entities.buildings.energy_producer import EnergyProducer
from karma.settings import (
    SOLAR_UPGRADE_ENERGY_COST,
    SOLAR_UPGRADE_PRODUCTION_AMOUNT,
    SOLAR_UPGRADE_PRODUCTION_INTERVAL,
    SOLAR_UPGRADE_RAW_MATERIAL_COST,
)


class SolarPanel(EnergyProducer):
    # Panneau solaire lent qui augmente le karma.

    ASSET_FOLDER = "solar_panel"

    UPGRADE_ENERGY_COST = SOLAR_UPGRADE_ENERGY_COST
    UPGRADE_RAW_MATERIAL_COST = SOLAR_UPGRADE_RAW_MATERIAL_COST
    UPGRADE_PRODUCTION_AMOUNT = SOLAR_UPGRADE_PRODUCTION_AMOUNT
    UPGRADE_PRODUCTION_INTERVAL = SOLAR_UPGRADE_PRODUCTION_INTERVAL

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        productionAmount: int,
        productionInterval: float,
    ) -> None:
        super().__init__(position, health, energyCost, 100.0, productionAmount, productionInterval)

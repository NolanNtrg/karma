import pygame
from karma.entities.buildings.ressourcesProducer import RessourcesProducer
from karma.enums import RessourceType

class SolarPanel(RessourcesProducer):
    def __init__(self, position: pygame.Vector2, health: int, energyCost: int, productionAmount: int, productionInterval: float) -> None:
        super().__init__(
            position, health, energyCost, 100.0, productionAmount, productionInterval,
            "solar_panel", resourceType=RessourceType.Energy, requiresDaylight=True
        )

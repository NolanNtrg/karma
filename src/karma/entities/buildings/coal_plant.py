import pygame
from karma.entities.buildings.ressourcesProducer import RessourcesProducer
from karma.enums import RessourceType

class CoalPlant(RessourcesProducer):
    def __init__(self, position: pygame.Vector2, health: int, energyCost: int, productionAmount: int, productionInterval: float) -> None:
        super().__init__(
            position, health, energyCost, -100.0, productionAmount, productionInterval,
            "coal_plant", resourceType=RessourceType.Energy, requiresDaylight=False
        )

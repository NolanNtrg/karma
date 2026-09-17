import pygame
from karma.entities.buildings.ressourcesProducer import RessourcesProducer
from karma.enums import RessourceType

class Driller(RessourcesProducer):
    def __init__(self, position: pygame.Vector2, health: int, energyCost: int, productionAmount: int, productionInterval: float) -> None:
        super().__init__(
            position, health, energyCost, -100.0, productionAmount, productionInterval, 
            "driller", resourceType=RessourceType.RawMaterial, requiresDaylight=False
        )


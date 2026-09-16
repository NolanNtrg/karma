import pygame

from karma.entities.buildings.building import Building


class Wall(Building):
    # Mur de défense qui canalise les ennemis.

    COLOR: tuple[int, int, int] = (120, 120, 120)

    def __init__(self, position: pygame.Vector2, health: int, energyCost: int) -> None:
        super().__init__(position, health, energyCost, karmaImpact=0.0)

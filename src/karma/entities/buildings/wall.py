import pygame

from karma.entities.buildings.building import Building


class Wall(Building):
    # Représente un mur de défense dans le jeu : canalise les ennemis, effet karma neutre

    def __init__(self, position: pygame.Vector2, health: int, energyCost: int) -> None:
        super().__init__(position, health, energyCost, karmaImpact=0.0)

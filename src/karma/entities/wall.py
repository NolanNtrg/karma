import pygame

from karma.entities.entity import Entity


class Wall(Entity):
    # Représente un mur de défense dans le jeu

    def __init__(self, position: pygame.Vector2, health: int) -> None:
        super().__init__(position, health)

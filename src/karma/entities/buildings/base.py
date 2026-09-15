import pygame

from karma.entities.core.entity import Entity


class Base(Entity):
    # Représente la base du joueur

    def __init__(self, position: pygame.Vector2, health: int) -> None:
        super().__init__(position, health)

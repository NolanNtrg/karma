import pygame


class Entity:
    # Base des entités avec une position et des points de vie.

    def __init__(self, position: pygame.Vector2, health: int) -> None:
        self.position: pygame.Vector2 = position
        self.max_health: int = health
        self.health: int = health

    def takeDamage(self, amount: int) -> None:
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def isDestroyed(self) -> bool:
        return self.health <= 0

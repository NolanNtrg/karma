import pygame


class Entity:
    # Base des entités avec une position et des points de vie.

    def __init__(self, position: pygame.Vector2, health: int) -> None:
        self.position: pygame.Vector2 = position
        self.max_health: int = health
        self.health: int = health

    def takeDamage(self, amount: int) -> None:
        # Réduit les points de vie de l'entité
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def isDestroyed(self) -> bool:
        # Vrai si l'entité n'a plus de points de vie
        return self.health <= 0

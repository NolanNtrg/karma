import pygame

from karma.entities.enemies.attacker import Attacker
from karma.entities.buildings.wall import Wall
from karma.entities.buildings.base import Base


class Enemy(Attacker):
    # Ennemi qui avance vers la base et attaque les obstacles rencontrés.

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        target: pygame.Vector2,
        speed: float,
        attackDamage: int,
        attackInterval: float,
        attackRange: float = 4.0,
    ) -> None:
        # target est la position de la base.
        # speed est exprimée en pixels par milliseconde.
        super().__init__(position, health, attackRange, attackDamage, attackInterval)
        self.target: pygame.Vector2 = target
        self.speed: float = speed

    def hasReachedTarget(self) -> bool:
        # Indique si l'ennemi est à portée de sa cible.
        return self.position.distance_to(self.target) <= self.attackRange

    def getVelocity(self) -> pygame.Vector2:
        # Retourne le déplacement vers la cible.
        direction = self.target - self.position
        if direction.length_squared() == 0:
            return pygame.Vector2(0, 0)
        return direction.normalize() * self.speed

    def update(self, dt: float, walls: list[Wall], base: Base) -> None:
        # Attaque un mur ou la base, sinon avance vers la base.
        blockingWall = self.findClosestTarget(self.position, walls)

        if blockingWall is not None:
            damage = self.tryAttack(dt)
            if damage:
                blockingWall.takeDamage(damage)
        elif self.hasReachedTarget():
            damage = self.tryAttack(dt)
            if damage:
                base.takeDamage(damage)
        else:
            self.position += self.getVelocity() * dt

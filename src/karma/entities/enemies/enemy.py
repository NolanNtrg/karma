import pygame

from karma.entities.enemies.attacker import Attacker
from karma.entities.buildings.wall import Wall
from karma.entities.buildings.base import Base


class Enemy(Attacker):
    # Représente un ennemi sur la carte : sa position, ses points de vie, son déplacement
    # en ligne droite vers la base et son attaque au contact

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
        # target : position de la base
        # speed : pixels par milliseconde
        super().__init__(position, health, attackRange, attackDamage, attackInterval)
        self.target: pygame.Vector2 = target
        self.speed: float = speed

    def hasReachedTarget(self) -> bool:
        # Vrai si l'ennemi est à portée d'attaque de sa cible (la base)
        return self.position.distance_to(self.target) <= self.attackRange

    def getVelocity(self) -> pygame.Vector2:
        # Vecteur de déplacement vers la cible, en pixels par milliseconde
        direction = self.target - self.position
        if direction.length_squared() == 0:
            return pygame.Vector2(0, 0)
        return direction.normalize() * self.speed

    def update(self, dt: float, walls: list[Wall], base: Base) -> None:
        # Met à jour l'ennemi pour une frame
        # dt : temps écoulé depuis la dernière frame, en millisecondes
        # walls : murs encore présents sur la carte
        # base : la base du joueur
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

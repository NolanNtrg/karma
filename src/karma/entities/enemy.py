import pygame

from karma.entities.entity import Entity
from karma.entities.enemy_ai import EnemyAI
from karma.entities.wall import Wall
from karma.entities.base import Base


class Enemy(Entity):
    # Représente un ennemi sur la carte : sa position, ses points de vie et son IA

    def __init__(self, position: pygame.Vector2, health: int, ai: EnemyAI) -> None:
        # ai : logique de déplacement et d'attaque propre à cet ennemi
        super().__init__(position, health)
        self.ai = ai

    def update(self, dt: float, walls: list[Wall], base: Base) -> None:
        # Met à jour l'ennemi pour une frame
        # dt : temps écoulé depuis la dernière frame, en millisecondes
        # walls : murs encore présents sur la carte
        # base : la base du joueur
        blockingWall = self.ai.findClosestTarget(self.position, walls)

        if blockingWall is not None:
            damage = self.ai.tryAttack(dt)
            if damage:
                blockingWall.takeDamage(damage)
        elif self.ai.hasReachedTarget(self.position):
            damage = self.ai.tryAttack(dt)
            if damage:
                base.takeDamage(damage)
        else:
            self.position += self.ai.getVelocity(self.position) * dt

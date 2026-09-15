import pygame

from karma.entities.enemy_ai import EnemyAI
from karma.entities.wall import Wall
from karma.entities.base import Base


class Enemy:
    """ Représente un ennemi sur la carte : sa position, ses points de vie et son IA """

    def __init__(self, position: pygame.Vector2, health: int, ai: EnemyAI) -> None:
        """
        position : position actuelle de l'ennemi
        health : points de vie de l'ennemi (réduits par le tir du joueur)
        ai : logique de déplacement et d'attaque propre à cet ennemi
        """
        self.position: pygame.Vector2 = position
        self.health: int = health
        self.ai: EnemyAI = ai

    def take_damage(self, amount: int) -> None:
        """ Réduit les points de vie de l'ennemi (appelé quand le joueur le touche) """
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_destroyed(self) -> bool:
        """ Vrai si l'ennemi n'a plus de points de vie """
        return self.health <= 0

    def update(self, dt: float, walls: list[Wall], base: Base) -> None:
        """
        Met à jour l'ennemi pour une frame.
        dt : temps écoulé depuis la dernière frame, en millisecondes
        walls : murs encore présents sur la carte
        base : la base du joueur
        """
        blocking_wall = self.ai.find_blocking_wall(self.position, walls)

        if blocking_wall is not None:
            damage = self.ai.try_attack(dt)
            if damage:
                blocking_wall.take_damage(damage)
        elif self.ai.has_reached_target(self.position):
            damage = self.ai.try_attack(dt)
            if damage:
                base.take_damage(damage)
        else:
            self.position += self.ai.get_velocity(self.position) * dt
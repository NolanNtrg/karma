import pygame

class Base:
    """ Classe représentant la base du joueur """

    def __init__(self, position: pygame.Vector2, health: int) -> None:
        """ position : position de la base. health : points de vie de la base """
        self.position = position
        self.health: int = health

    def take_damage(self, amount: int) -> None:
        """ Réduit les points de vie de la base """
        self.health -= amount
        if self.health < 0:
            self.health = 0
import pygame

class Wall:
    """ Classe représentant un mur de défense dans le jeu """

    def __init__(self, position: pygame.Vector2, health: int) -> None:
        """ position : position du mur. health : points de vie du mur """
        self.position = position
        self.health = health

    def take_damage(self, amount: int) -> None:
        """ Réduit les points de vie du mur """
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_destroyed(self) -> bool:
        """ Vrai si le mur n'a plus de points de vie """
        return self.health <= 0
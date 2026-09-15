import pygame

from karma.entities.attacker import Attacker


class EnemyAI(Attacker):
    # Calcule le déplacement en ligne droite d'un ennemi et gère son attaque au contact

    def __init__(
        self,
        target: pygame.Vector2,
        speed: float,
        attackDamage: int,
        attackInterval: float,
        attackRange: float = 4.0,
    ) -> None:
        # target : position de la base
        # speed : pixels par milliseconde
        super().__init__(attackRange, attackDamage, attackInterval)
        self.target = target
        self.speed = speed

    def hasReachedTarget(self, position: pygame.Vector2) -> bool:
        # Vrai si l'ennemi est à portée d'attaque de sa cible (la base)
        return position.distance_to(self.target) <= self.attackRange

    def getVelocity(self, position: pygame.Vector2) -> pygame.Vector2:
        # Vecteur de déplacement vers la cible, en pixels par milliseconde
        direction = self.target - position
        if direction.length_squared() == 0:
            return pygame.Vector2(0, 0)
        return direction.normalize() * self.speed

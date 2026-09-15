from typing import Sequence

import pygame

from karma.entities.entity import Entity


class Attacker(Entity):
    # Classe mère de toute entité capable d'attaquer une cible à portée avec un temps de recharge

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        attackRange: float,
        attackDamage: int,
        attackInterval: float,
    ) -> None:
        Entity.__init__(self, position, health)
        self.attackRange: float = attackRange
        self.attackDamage: int = attackDamage
        self.attackInterval: float = attackInterval
        self.timeSinceLastAttack: float = attackInterval

    def tryAttack(self, dt: float) -> int:
        # dt : temps écoulé depuis la dernière frame, en millisecondes
        # Retourne les dégâts à infliger ce frame (0 si le temps de recharge n'est pas écoulé)
        # À appeler uniquement quand l'appelant sait déjà qu'une cible est à portée :
        # cette méthode ne vérifie pas elle-même la distance
        self.timeSinceLastAttack += dt
        if self.timeSinceLastAttack >= self.attackInterval:
            self.timeSinceLastAttack = 0.0
            return self.attackDamage
        return 0

    def findClosestTarget(self, position: pygame.Vector2, candidates: Sequence[Entity]) -> Entity | None:
        # Cherche, parmi les candidats encore en vie, le plus proche qui est à portée
        # Retourne None si aucun candidat n'est assez proche
        closestTarget: Entity | None = None
        closestDistance: float = self.attackRange
        for candidate in candidates:
            if candidate.isDestroyed():
                continue
            distance = position.distance_to(candidate.position)
            if distance <= closestDistance:
                closestTarget = candidate
                closestDistance = distance
        return closestTarget

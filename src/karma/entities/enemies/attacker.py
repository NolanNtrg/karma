from typing import Sequence

import pygame

from karma.entities.entity import Entity


class Attacker(Entity):
    # Base des entités capables d'attaquer avec un délai.

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
        # La portée doit être vérifiée par l'appelant avant d'appeler tryAttack.
        self.timeSinceLastAttack += dt
        if self.timeSinceLastAttack >= self.attackInterval:
            self.timeSinceLastAttack = 0.0
            return self.attackDamage
        return 0

    def findClosestTarget(self, position: pygame.Vector2, candidates: Sequence[Entity]) -> Entity | None:
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

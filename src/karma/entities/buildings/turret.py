import pygame

from karma.entities.buildings.building import Building
from karma.entities.enemies.attacker import Attacker
from karma.entities.enemies.enemy import Enemy


class Turret(Building):
    # Tourelle statique qui attaque les ennemis proches.

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        attackRange: float,
        attackDamage: int,
        attackInterval: float,
    ) -> None:
        super().__init__(position, health, energyCost, karmaImpact=0.0)
        self.attacker = Attacker(position, health, attackRange, attackDamage, attackInterval)

    def update(self, dt: float, enemies: list[Enemy]) -> None:
        # Cherche une cible et attaque si le délai est écoulé.
        if not self.isOperational():
            return
        target = self.attacker.findClosestTarget(self.position, enemies)
        if target is not None:
            damage = self.attacker.tryAttack(dt)
            if damage:
                target.takeDamage(damage)

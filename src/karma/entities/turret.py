import pygame

from karma.entities.attacker import Attacker
from karma.entities.enemy import Enemy


class Turret(Attacker):
    # Tourelle de défense statique : cible automatiquement l'ennemi le plus proche à portée

    def __init__(
        self,
        position: pygame.Vector2,
        attackRange: float,
        attackDamage: int,
        attackInterval: float,
    ) -> None:
        super().__init__(attackRange, attackDamage, attackInterval)
        self.position = position

    def update(self, dt: float, enemies: list[Enemy]) -> None:
        # Met à jour la tourelle pour une frame : cherche une cible en portée et tire
        # si le temps de recharge est écoulé. Dégâts appliqués instantanément (pas de
        # sprite de projectile pour ce niveau 1, à ajouter plus tard si besoin)
        target = self.findClosestTarget(self.position, enemies)
        if target is not None:
            damage = self.tryAttack(dt)
            if damage:
                target.takeDamage(damage)

import pygame

from karma.entities.buildings.building import Building
from karma.entities.enemies.attacker import Attacker
from karma.entities.enemies.enemy import Enemy


class Turret(Building, Attacker):
    # Tourelle de défense statique : cible automatiquement l'ennemi le plus proche à portée
    # Effet karma neutre, coût payé en Énergie (construction et futurs niveaux 2-3)

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        attackRange: float,
        attackDamage: int,
        attackInterval: float,
    ) -> None:
        Building.__init__(self, position, health, energyCost, karmaImpact=0.0)
        Attacker.__init__(self, position, health, attackRange, attackDamage, attackInterval)

    def update(self, dt: float, enemies: list[Enemy]) -> None:
        # Met à jour la tourelle pour une frame : cherche une cible en portée et tire
        # si le temps de recharge est écoulé. Dégâts appliqués instantanément (pas de
        # sprite de projectile pour ce niveau 1, à ajouter plus tard si besoin)
        if not self.isOperational():
            return
        target = self.findClosestTarget(self.position, enemies)
        if target is not None:
            damage = self.tryAttack(dt)
            if damage:
                target.takeDamage(damage)

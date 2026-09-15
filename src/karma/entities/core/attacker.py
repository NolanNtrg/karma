import pygame


class Attacker:
    # Classe mère de toute entité capable d'attaquer une cible à portée avec un temps de recharge

    def __init__(self, attackRange: float, attackDamage: int, attackInterval: float) -> None:
        self.attackRange = attackRange
        self.attackDamage = attackDamage
        self.attackInterval = attackInterval
        self.timeSinceLastAttack = attackInterval

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

    def findClosestTarget(self, position: pygame.Vector2, candidates: list) -> object | None:
        # Cherche, parmi les candidats encore en vie, le plus proche qui est à portée
        # Retourne None si aucun candidat n'est assez proche
        closestTarget = None
        closestDistance = self.attackRange
        for candidate in candidates:
            if candidate.isDestroyed():
                continue
            distance = position.distance_to(candidate.position)
            if distance <= closestDistance:
                closestTarget = candidate
                closestDistance = distance
        return closestTarget

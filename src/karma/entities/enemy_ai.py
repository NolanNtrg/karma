import pygame

from karma.entities.wall import Wall


class EnemyAI:
    """ Calcule le déplacement en ligne droite d'un ennemi et gère son attaque au contact """

    def __init__(
        self,
        target: pygame.Vector2,
        speed: float,
        attack_damage: int,
        attack_interval: float,
        attack_range: float = 4.0,
    ) -> None:
        """
        target : position de la base
        speed : pixels par milliseconde
        attack_damage : dégâts infligés à chaque attaque
        attack_interval : délai en millisecondes entre deux attaques
        attack_range : distance à laquelle l'ennemi peut commencer à attaquer la base
        """
        self.target = target
        self.speed = speed
        self.attack_damage = attack_damage
        self.attack_interval = attack_interval
        self.attack_range = attack_range
        self.time_since_last_attack = self.attack_interval

    def get_velocity(self, position: pygame.Vector2) -> pygame.Vector2:
     return position.distance_to(self.target) <= self.attack_range

    def find_blocking_wall(self, position: pygame.Vector2, walls: list[Wall]) -> Wall | None:
        """
        Cherche, parmi les murs encore en vie, le plus proche qui est à portée d'attaque.
        Retourne None si aucun mur n'est assez proche.
        """
        closest_wall = None
        closest_distance = self.attack_range
        for wall in walls:
            if wall.is_destroyed():
                continue
            distance = position.distance_to(wall.position)
            if distance <= closest_distance:
                closest_wall = wall
                closest_distance = distance
        return closest_wall

    def try_attack(self, dt: float) -> int:
        """
        dt : temps écoulé depuis la dernière frame, en millisecondes.
        Retourne les dégâts à infliger ce frame (0 si le cooldown n'est pas écoulé).
        À appeler uniquement quand l'appelant sait déjà que l'ennemi est au contact
        d'une cible (mur bloquant ou base atteinte) : cette méthode ne vérifie pas
        elle-même la distance.
        """
        self.time_since_last_attack += dt
        if self.time_since_last_attack >= self.attack_interval:
            self.time_since_last_attack = 0.0
            return self.attack_damage
        return 0
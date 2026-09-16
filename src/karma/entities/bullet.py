from typing import Sequence

import pygame

from karma.entities.enemies.enemy import Enemy
from karma.settings import ASSETS_DIR


class Bullet:
    # Projectile qui vole en ligne droite jusqu'à percuter un ennemi OU sortir hors-cam

    HIT_RADIUS = 16  # distance de collision avec un ennemi

    # partagée par toutes les entités qui tirent (joueur, tourelle) pour éviter de recharger l'image à chaque fois
    @staticmethod
    def loadImage(size: tuple[int, int]) -> pygame.Surface:
        spriteSheet = pygame.image.load(ASSETS_DIR / "Projectiles" / "bullets+plasma.png").convert_alpha()
        # une seule case de la sprite sheet, découpée pour représenter la balle
        frame = spriteSheet.subsurface((8, 0, 8, 8))
        return pygame.transform.scale(frame, size)

    def __init__(self, position: pygame.Vector2, direction: pygame.Vector2, damage: int, speed: float, image: pygame.Surface) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(position)
        self.direction: pygame.Vector2 = pygame.Vector2(direction)
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
        self.damage: int = damage
        self.speed: float = speed
        self.image: pygame.Surface = image
        self.hit: bool = False

    # si la balle touche un ennemi, on inflige les dégâts 
    # et on marque la balle comme "hit" pour qu'elle disparaisse
    def update(self, dt: float, enemies: Sequence[Enemy] = (), camera=None) -> None:
        for enemy in enemies:
            if not enemy.isDestroyed() and self.position.distance_to(enemy.getCenter()) <= self.HIT_RADIUS:
                enemy.takeDamage(self.damage)
                self.hit = True
                return
        self.position += self.direction * self.speed * dt

        # si la balle sort de l'écran, on la marque comme "hit" pour qu'elle disparaisse
        if camera is not None and not camera.contains(self.position):
            self.hit = True

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        position = camera.apply(self.position) if camera else self.position
        screen.blit(self.image, position)

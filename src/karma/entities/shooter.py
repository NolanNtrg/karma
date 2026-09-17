from typing import Sequence

import pygame

from karma.entities.bullet import Bullet
from karma.entities.enemies.enemy import Enemy
from karma.settings import SOUNDS_DIR 


class Shooter:
    # Composant (pas une classe mère) qui gère la liste de balles d'une entité qui tire.
    bullet_sound = None

    def __init__(self, bulletImage: pygame.Surface) -> None:
        if Shooter.bullet_sound is None:
                Shooter.bullet_sound = pygame.mixer.Sound(SOUNDS_DIR / "gun-sound.mp3")
                Shooter.bullet_sound.set_volume(0.05)
        self.bulletImage: pygame.Surface = bulletImage
        self.bullets: list[Bullet] = []

    def spawnBullet(self, position: pygame.Vector2, direction: pygame.Vector2, damage: int, speed: float) -> None:
        self.bullets.append(Bullet(position, direction, damage, speed, self.bulletImage))
        Shooter.bullet_sound.play()

    def updateBullets(self, dt: float, enemies: Sequence[Enemy], camera=None) -> None:
        for bullet in self.bullets:
            bullet.update(dt, enemies, camera)
        self.bullets = [bullet for bullet in self.bullets if not bullet.hit]

    def drawBullets(self, screen: pygame.Surface, camera=None) -> None:
        for bullet in self.bullets:
            bullet.draw(screen, camera)
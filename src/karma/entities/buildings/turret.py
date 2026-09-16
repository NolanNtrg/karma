import math

import pygame

from karma.entities.buildings.building import Building
from karma.entities.bullet import Bullet
from karma.entities.enemies.attacker import Attacker
from karma.entities.enemies.enemy import Enemy
from karma.settings import ASSETS_DIR

TURRET_SIZE = (64, 64)
CANNON_LENGTH = TURRET_SIZE[0] * 0.45  # distance entre le centre et le bout du canon
BULLET_SIZE = (16, 16)
BULLET_SPEED = 0.5  # pixels par milliseconde


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
        self.bullets: list[Bullet] = []
        self.facing: pygame.Vector2 = pygame.Vector2(1, 0)

        dayImage = pygame.image.load(ASSETS_DIR / "buildings" / "turret" / "turret_assembled_day.png").convert_alpha()
        nightImage = pygame.image.load(ASSETS_DIR / "buildings" / "turret" / "turret_assembled_night.png").convert_alpha()
        self.dayImage = pygame.transform.scale(dayImage, TURRET_SIZE)
        self.nightImage = pygame.transform.scale(nightImage, TURRET_SIZE)
        self.image = self.dayImage

        bulletSheet = pygame.image.load(ASSETS_DIR / "Projectiles" / "bullets+plasma.png").convert_alpha()
        bulletFrame = bulletSheet.subsurface((8, 0, 8, 8))
        self.bulletImage = pygame.transform.scale(bulletFrame, BULLET_SIZE)

    def getCenter(self) -> pygame.Vector2:
        return self.position + pygame.Vector2(TURRET_SIZE[0] / 2, TURRET_SIZE[1] / 2)

    def getCannonTip(self) -> pygame.Vector2:
        return self.getCenter() + self.facing * CANNON_LENGTH

    def update(self, dt: float, enemies: list[Enemy], isDay: bool = True) -> None:
        self.image = self.dayImage if isDay else self.nightImage

        for bullet in self.bullets:
            bullet.update(dt)
        self.bullets = [bullet for bullet in self.bullets if not bullet.hit]

        if not self.isOperational():
            return

        target = self.attacker.findClosestTarget(self.getCenter(), enemies)
        if target is None:
            return

        direction = target.position - self.getCenter()
        if direction.length() > 0:
            self.facing = direction.normalize()

        damage = self.attacker.tryAttack(dt)
        if damage:
            bullet = Bullet(self.getCannonTip(), target, damage, BULLET_SPEED, self.bulletImage)
            self.bullets.append(bullet)

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        # L'image de base pointe vers la droite, on la tourne vers la cible.
        angle = math.degrees(math.atan2(-self.facing.y, self.facing.x))
        rotatedImage = pygame.transform.rotate(self.image, angle)
        rect = rotatedImage.get_rect(center=self.getCenter())
        position = camera.apply(pygame.Vector2(rect.topleft)) if camera else pygame.Vector2(rect.topleft)
        screen.blit(rotatedImage, position)

        for bullet in self.bullets:
            bullet.draw(screen, camera)

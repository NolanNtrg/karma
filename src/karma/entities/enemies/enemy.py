from pathlib import Path

import pygame

from karma.entities.buildings.base import Base
from karma.entities.buildings.wall import Wall
from karma.entities.enemies.attacker import Attacker
from karma.entities.sprite import SpriteAnimator


class Enemy(Attacker):
    # Ennemi qui avance vers la base et attaque les obstacles rencontrés.

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        target: pygame.Vector2,
        speed: float,
        attackDamage: int,
        attackInterval: float,
        spriteSheetPath: Path | None,
        idleFrameCoords: list[tuple[int, int]] | None = None,
        walkFrameCoords: list[tuple[int, int]] | None = None,
        attackRange: float = 4.0,
    ) -> None:
        super().__init__(position, health, attackRange, attackDamage, attackInterval)
        self.target: pygame.Vector2 = target
        self.speed: float = speed

        if spriteSheetPath is not None:
            assert idleFrameCoords is not None and walkFrameCoords is not None
            self.animator = SpriteAnimator(spriteSheetPath, idleFrameCoords, walkFrameCoords)

    def getCenter(self) -> pygame.Vector2:
        half_size = (SpriteAnimator.FRAME_SIZE * SpriteAnimator.SCALE) / 2
        return pygame.Vector2(self.position.x + half_size, self.position.y + half_size)

    def isInRangeOfBase(self, base: Base) -> bool:
        # vérifie si le centre de l'ennemi est à portée de la hitbox de la base
        attack_zone = base.rect.inflate(int(self.attackRange * 2), int(self.attackRange * 2))
        return attack_zone.collidepoint(self.getCenter())

    def getVelocity(self) -> pygame.Vector2:
        direction = self.target - self.position
        if direction.length_squared() == 0:
            return pygame.Vector2(0, 0)
        return direction.normalize() * self.speed

    def updateAnimation(self, dt: float, isMoving: bool, direction: pygame.Vector2) -> None:
        self.animator.update(dt, isMoving, direction)

    def update(self, dt: float, walls: list[Wall], base: Base) -> None:
        blockingWall = self.findClosestTarget(self.position, walls)
        if blockingWall is not None:
            damage = self.tryAttack(dt)
            if damage:
                blockingWall.takeDamage(damage)
            self.updateAnimation(dt, False, pygame.Vector2(0, 0))
            return

        # Attaque la base si elle est en vie et à portée
        if not base.isDestroyed() and self.isInRangeOfBase(base):
            damage = self.tryAttack(dt)
            if damage:
                base.takeDamage(damage)
            self.updateAnimation(dt, False, pygame.Vector2(0, 0))
            return

        # Avance vers la base si elle est encore active
        if not base.isDestroyed():
            velocity = self.getVelocity()
            self.position += velocity * dt
            self.updateAnimation(dt, True, velocity)
        else:
            self.updateAnimation(dt, False, pygame.Vector2(0, 0))

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        position = camera.apply(self.position) if camera else self.position
        screen.blit(self.animator.image, position)

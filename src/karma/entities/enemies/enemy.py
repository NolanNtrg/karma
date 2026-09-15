from pathlib import Path

import pygame

from karma.entities.enemies.attacker import Attacker
from karma.entities.buildings.wall import Wall
from karma.entities.buildings.base import Base


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
        frameSize: int = 16,
        scale: int = 2,
    ) -> None:
        # target est la position de la base.
        # speed est exprimée en pixels par milliseconde.
        super().__init__(position, health, attackRange, attackDamage, attackInterval)
        self.target: pygame.Vector2 = target
        self.speed: float = speed

        self.frameSize: int = frameSize
        self.scale: int = scale

        # None pour les ennemis qui gèrent leur propre rendu (voir ArmoredUnit).
        if spriteSheetPath is not None:
            assert idleFrameCoords is not None and walkFrameCoords is not None
            self.spriteSheet: pygame.Surface = pygame.image.load(spriteSheetPath).convert_alpha()
            self.idleFrames: list[pygame.Surface] = [self.getSprite(row, col) for row, col in idleFrameCoords]
            self.walkFrames: list[pygame.Surface] = [self.getSprite(row, col) for row, col in walkFrameCoords]

            self.imageIndex: float = 0.0
            self.flip: bool = False
            self.currentFrames: list[pygame.Surface] = self.idleFrames
            self.image: pygame.Surface = self.currentFrames[0]

    def getSprite(self, row: int, col: int) -> pygame.Surface:
        size = self.frameSize
        img = pygame.Surface((size, size), pygame.SRCALPHA)
        img.blit(self.spriteSheet, (0, 0), (col * size, row * size, size, size))
        return pygame.transform.scale_by(img, self.scale)

    def hasReachedTarget(self) -> bool:
        # Indique si l'ennemi est à portée de sa cible.
        return self.position.distance_to(self.target) <= self.attackRange

    def getVelocity(self) -> pygame.Vector2:
        # Retourne le déplacement vers la cible.
        direction = self.target - self.position
        if direction.length_squared() == 0:
            return pygame.Vector2(0, 0)
        return direction.normalize() * self.speed

    def updateAnimation(self, dt: float, isMoving: bool, direction: pygame.Vector2) -> None:
        # Choisit l'animation (marche/idle) et l'image courante.
        self.currentFrames = self.walkFrames if isMoving else self.idleFrames
        if direction.x < 0:
            self.flip = True
        elif direction.x > 0:
            self.flip = False

        self.imageIndex += dt * 0.007
        frame = self.currentFrames[int(self.imageIndex % len(self.currentFrames))]
        self.image = pygame.transform.flip(frame, self.flip, False)

    def update(self, dt: float, walls: list[Wall], base: Base) -> None:
        # Attaque un mur ou la base, sinon avance vers la base.
        blockingWall = self.findClosestTarget(self.position, walls)

        if blockingWall is not None:
            damage = self.tryAttack(dt)
            if damage:
                blockingWall.takeDamage(damage)
            self.updateAnimation(dt, False, pygame.Vector2(0, 0))
        elif self.hasReachedTarget():
            damage = self.tryAttack(dt)
            if damage:
                base.takeDamage(damage)
            self.updateAnimation(dt, False, pygame.Vector2(0, 0))
        else:
            velocity = self.getVelocity()
            self.position += velocity * dt
            self.updateAnimation(dt, True, velocity)

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        position = camera.apply(self.position) if camera else self.position
        screen.blit(self.image, position)

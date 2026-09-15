from pathlib import Path

import pygame
from karma.settings import ASSETS_DIR

from karma.entities.entity import Entity


class Player(Entity):

    # Constructeur
    def __init__(self, name: str, position: pygame.Vector2, speed: float, health: int = 100) -> None:
        super().__init__(position, health)
        self.name: str = name
        self.speed: float = speed

        spriteSheetPath: Path = ASSETS_DIR / "Soldiers" / "SquadLeader.png"
        self.spriteSheet: pygame.Surface = pygame.image.load(spriteSheetPath).convert_alpha()

        self.idleFrame: list[pygame.Surface] = [self.getSprite(0,0), self.getSprite(0,1)]
        self.movingFrames: list[pygame.Surface] = [self.getSprite(1,0), self.getSprite(1,1)]

        self.imageIndex: float = 0.0
        self.flip: bool = False
        self.currentFrame: list[pygame.Surface] = self.idleFrame
        self.image: pygame.Surface = self.currentFrame[0]

    def getDirection(self) -> pygame.Vector2:
        keys = pygame.key.get_pressed()
        dx: float = (keys[pygame.K_d] - keys[pygame.K_q])
        dy: float = (keys[pygame.K_s] - keys[pygame.K_z])
        direction: pygame.Vector2 = pygame.Vector2(dx, dy)

        if direction.length_squared() == 0:
            return direction

        return direction.normalize()

    def getSprite(self, row: int, col:int) -> pygame.Surface:
        img: pygame.Surface = pygame.Surface((16, 16), pygame.SRCALPHA)
        img.blit(self.spriteSheet, (0,0), (col*16, row*16, 16, 16))
        return pygame.transform.scale_by(img, 2)

    def update(self, dt: float) -> None:
        direction = self.getDirection()
        self.position += direction * self.speed * dt
        isMoving: bool = direction.length_squared() > 0 
        if isMoving:
            self.currentFrame = self.movingFrames
            if direction.x < 0:
                self.flip = True
            elif direction.x > 0:
                self.flip = False
        else:
            self.currentFrame = self.idleFrame

        self.imageIndex += dt * 0.007
        frame = self.currentFrame[int(self.imageIndex % len(self.currentFrame))]
        self.image = pygame.transform.flip(frame, self.flip, False)
    
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.position)
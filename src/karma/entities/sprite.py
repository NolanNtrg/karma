from pathlib import Path

import pygame


class SpriteAnimator:
    # Anime un sprite entre une pose immobile et une pose en mouvement.

    FRAME_SIZE = 16
    SCALE = 2

    # méthode statique car utilisée par des entités qui n'ont pas d'instance de SpriteAnimator
    @staticmethod
    def getSprite(spriteSheet: pygame.Surface, row: int, col: int) -> pygame.Surface:
        # Découpe une frame dans la sprite sheet et l'agrandit.
        frameSize = SpriteAnimator.FRAME_SIZE
        img = pygame.Surface((frameSize, frameSize), pygame.SRCALPHA)
        img.blit(spriteSheet, (0, 0), (col * frameSize, row * frameSize, frameSize, frameSize))
        return pygame.transform.scale_by(img, SpriteAnimator.SCALE)

    def __init__(
        self,
        spriteSheetPath: Path,
        idleFrameCoords: list[tuple[int, int]],
        walkFrameCoords: list[tuple[int, int]],
    ) -> None:
        self.spriteSheet: pygame.Surface = pygame.image.load(spriteSheetPath).convert_alpha()
        self.idleFrames: list[pygame.Surface] = [self.getSprite(self.spriteSheet, row, col) for row, col in idleFrameCoords]
        self.walkFrames: list[pygame.Surface] = [self.getSprite(self.spriteSheet, row, col) for row, col in walkFrameCoords]

        self.imageIndex: float = 0.0
        self.flip: bool = False
        self.currentFrames: list[pygame.Surface] = self.idleFrames
        self.image: pygame.Surface = self.currentFrames[0]

    def update(self, dt: float, isMoving: bool, direction: pygame.Vector2) -> None:
        self.currentFrames = self.walkFrames if isMoving else self.idleFrames
        if direction.x < 0:
            self.flip = True
        elif direction.x > 0:
            self.flip = False

        self.imageIndex += dt * 0.007
        frame = self.currentFrames[int(self.imageIndex % len(self.currentFrames))]
        self.image = pygame.transform.flip(frame, self.flip, False)

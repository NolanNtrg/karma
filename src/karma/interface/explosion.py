from pathlib import Path

import pygame

from karma.entities.sprite import SpriteAnimator
from karma.interface.frameSequencer import FrameSequencer


class ExplosionAnimation:
    # Joue une fois toutes les frames d'une feuille de sprites.

    FRAME_SIZE = 32

    def __init__(self, sprite_sheet_path: Path, position: pygame.Vector2, fps: float = 12.0) -> None:
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        columns = sprite_sheet.get_width() // self.FRAME_SIZE
        rows = sprite_sheet.get_height() // self.FRAME_SIZE

        # crée une liste de surfaces pour chaque frame de l'animation
        self.frames: list[pygame.Surface] = [
            SpriteAnimator.getSprite(sprite_sheet, row, column, self.FRAME_SIZE)
            for row in range(rows)
            for column in range(columns)
        ]

        self.position: pygame.Vector2 = pygame.Vector2(position)
        self.sequencer = FrameSequencer(len(self.frames), fps)

    def update(self, dt: float) -> bool:
        return self.sequencer.update(dt)

    def draw(self, screen: pygame.Surface, camera) -> None:
        position = camera.apply(self.position)
        frame = self.frames[self.sequencer.current_frame]
        rect = frame.get_rect(center=(round(position.x + 32), round(position.y + 32)))
        screen.blit(frame, rect)

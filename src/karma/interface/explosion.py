from pathlib import Path

import pygame


class ExplosionAnimation:
    FRAME_SIZE = 32
    SCALE = 2

    def __init__(self, sprite_sheet_path: Path, position: pygame.Vector2, fps: float = 12.0) -> None:
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        columns = sprite_sheet.get_width() // self.FRAME_SIZE
        rows = sprite_sheet.get_height() // self.FRAME_SIZE
        self.frames = []

        for row in range(rows):
            for column in range(columns):
                frame = pygame.Surface((self.FRAME_SIZE, self.FRAME_SIZE), pygame.SRCALPHA)
                frame.blit(
                    sprite_sheet,
                    (0, 0),
                    (column * self.FRAME_SIZE, row * self.FRAME_SIZE, self.FRAME_SIZE, self.FRAME_SIZE),
                )
                self.frames.append(pygame.transform.scale_by(frame, self.SCALE))

        self.position = pygame.Vector2(position)
        self.frame_duration = 1000.0 / fps
        self.elapsed = 0.0
        self.current_frame = 0
        self.finished = False

    def update(self, dt: float) -> bool:
        if self.finished:
            return True

        self.elapsed += dt
        while self.elapsed >= self.frame_duration:
            self.elapsed -= self.frame_duration
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.current_frame = len(self.frames) - 1
                self.finished = True
                break

        return self.finished

    def draw(self, screen: pygame.Surface, camera) -> None:
        position = camera.apply(self.position)
        frame = self.frames[self.current_frame]
        rect = frame.get_rect(center=(round(position.x + 32), round(position.y + 32)))
        screen.blit(frame, rect)
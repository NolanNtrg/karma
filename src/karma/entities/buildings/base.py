import pygame

from karma.entities.entity import Entity
from karma.settings import ASSETS_DIR

class Base(Entity):
    # Base du joueur

    def __init__(self, position: pygame.Vector2, health: int = 500) -> None:
        super().__init__(position, health)
        self.invincible: bool = False
        self.day_frames = []
        self.night_frames = []

        # Importation des images du jour et de la nuit
        for i in range(1, 5):
            img_day = pygame.image.load(ASSETS_DIR / "base" / "day" / f"idle_{i}.png").convert_alpha()
            self.day_frames.append(pygame.transform.scale(img_day, (64, 64)))
            img_night = pygame.image.load(ASSETS_DIR / "base" / "night" / f"idle_{i}.png").convert_alpha()
            self.night_frames.append(pygame.transform.scale(img_night, (64, 64)))
        self.imageIndex = 0.0
        self.image = self.day_frames[0]
        self.rect = pygame.Rect(int(self.position.x + 2), int(self.position.y + 10), 60, 50)

    def takeDamage(self, amount: int) -> None:
        if self.invincible:
            return
        super().takeDamage(amount)

    def update(self, dt: float, is_day: bool = True) -> None:
        frames = self.day_frames if is_day else self.night_frames
        self.imageIndex += dt * 0.006
        frame_idx = int(self.imageIndex) % len(frames)
        self.image = frames[frame_idx]

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        # Applique la caméra comme pour le joueur
        position = camera.apply(self.position)
        screen.blit(self.image, position)
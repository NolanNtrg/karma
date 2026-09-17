import pygame
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH


class BuildingMenu:
    def __init__(self) -> None:
        raw_image = pygame.image.load(ASSETS_DIR / "hud" / "menu_building.png").convert_alpha()

        self.image = pygame.transform.scale_by(raw_image, 0.8)

        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))

        self.isVisible: bool = False

    def draw(self, screen: pygame.Surface) -> None:
        if self.isVisible:
            screen.blit(self.image, self.rect)
    
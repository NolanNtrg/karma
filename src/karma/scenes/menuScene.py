import pygame

from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH

class MenuScene():

    def drawMenuScene(self) -> None:
        backgroundOriginal = pygame.image.load(ASSETS_DIR / "Main-Menu.jpg")
        background = pygame.transform.scale(backgroundOriginal, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(background, (0,0))
        self.main_menu.draw(self.screen)
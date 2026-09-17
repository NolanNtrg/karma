import pygame

from karma.enums import StateType
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH

class MenuScene:

    background = None
        
    @staticmethod
    def drawMenuScene(self, state: StateType) -> None:
        if MenuScene.background is None:
                backgroundOriginal = pygame.image.load(ASSETS_DIR / "Main-Menu.jpg").convert()
                MenuScene.background = pygame.transform.scale(backgroundOriginal, (SCREEN_WIDTH, SCREEN_HEIGHT))
                
        self.screen.blit(MenuScene.background, (0,0))
        if state == StateType.Menu:
            self.main_menu.draw(self.screen)
        elif state == StateType.GameOver:
            self.game_over_menu.draw(self.screen)
        else:
            self.credits_menu.draw(self.screen)
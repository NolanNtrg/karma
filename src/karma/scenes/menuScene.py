import pygame

from karma.enums import StateType, MusicType
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, SOUNDS_DIR

class MenuScene:

    background = None
    how_build_image = None
    how_karma_image = None
    @staticmethod
    def drawMenuScene(self, state: StateType) -> None:
        if state == StateType.HowToPlay:
            MenuScene.drawHowToPlayScene(self)
            return
        if MenuScene.background is None:
                backgroundOriginal = pygame.image.load(ASSETS_DIR / "Main-Menu.jpg").convert()
                MenuScene.background = pygame.transform.scale(backgroundOriginal, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(MenuScene.background, (0,0))
        if state == StateType.Menu:
            self.main_menu.draw(self.screen)
        elif state in (StateType.BadEnding, StateType.GoodEnding):
            self.game_over_menu.draw(self.screen)
        else:
            self.credits_menu.draw(self.screen)

    @staticmethod
    def drawHowToPlayScene(self) -> None:
        if MenuScene.how_build_image is None:
            build_orig = pygame.image.load(ASSETS_DIR / "menu-how-to-play" / "how-build.jpeg").convert()
            MenuScene.how_build_image = pygame.transform.scale(build_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
            karma_orig = pygame.image.load(ASSETS_DIR / "menu-how-to-play" / "how-karma.jpeg").convert()
            MenuScene.how_karma_image = pygame.transform.scale(karma_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
        current_img = MenuScene.how_build_image if self.how_to_play_index == 0 else MenuScene.how_karma_image
        self.screen.blit(current_img, (0, 0))
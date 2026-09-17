import pygame

from karma.enums import StateType, MusicType
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH, SOUNDS_DIR

class MenuScene:

    background = None
    how_build_image = None
    how_karma_image = None
    @staticmethod
    def drawMenuScene(game, state: StateType) -> None:
        if state == StateType.HowToPlay:
            MenuScene.drawHowToPlayScene(game)
            return
        if MenuScene.background is None:
                backgroundOriginal = pygame.image.load(ASSETS_DIR / "Main-Menu.jpg").convert()
                MenuScene.background = pygame.transform.scale(backgroundOriginal, (SCREEN_WIDTH, SCREEN_HEIGHT))
        game.screen.blit(MenuScene.background, (0,0))
        if state == StateType.Menu:
            game.main_menu.draw(game.screen)
        elif state in (StateType.BadEnding, StateType.GoodEnding):
            game.game_over_menu.draw(game.screen)
        else:
            game.credits_menu.draw(game.screen)

    @staticmethod
    def drawHowToPlayScene(game) -> None:
        if MenuScene.how_build_image is None:
            build_orig = pygame.image.load(ASSETS_DIR / "menu-how-to-play" / "how-build.jpeg").convert()
            MenuScene.how_build_image = pygame.transform.scale(build_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
            karma_orig = pygame.image.load(ASSETS_DIR / "menu-how-to-play" / "how-karma.jpeg").convert()
            MenuScene.how_karma_image = pygame.transform.scale(karma_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
        current_img = MenuScene.how_build_image if game.how_to_play_index == 0 else MenuScene.how_karma_image
        game.screen.blit(current_img, (0, 0))
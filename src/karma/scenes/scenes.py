import pygame

from karma.enums import StateType
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH
from karma.scenes.playScene import PlayScene
from karma.scenes.menuScene import MenuScene


class Scene:

    def updateScenes(self, dt: float) -> None:
        PlayScene.updatePlayScene(self, dt)

    def drawScenes(self) -> None:
        # Rendu graphique
        if self.state == StateType.Menu:
            MenuScene.drawMenuScene(self)
        else:
            PlayScene.drawPlayScene(self)

        pygame.display.flip()

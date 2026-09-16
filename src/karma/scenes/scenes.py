import pygame

from karma.enums import StateType
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH
from karma.scenes.playScene import PlayScene
from karma.scenes.menuScene import MenuScene


class Scene:

    def updateScenes(self, dt: float) -> None:
        if self.state == StateType.Play:
            PlayScene.updatePlayScene(self, dt)
        elif self.state == StateType.Cinematic:
            self.update_cinematic(dt)

    def drawScenes(self) -> None:
        # Rendu graphique
        if self.state == StateType.Menu or self.state == StateType.Credits:
            MenuScene.drawMenuScene(self, self.state)
        elif self.state == StateType.Cinematic:
            self.cinematic_player.draw(self.screen)
        elif self.state == StateType.Pause and self.paused_from_cinematic:
            self.cinematic_player.draw(self.screen)
            self.pause_menu.draw(self.screen)
        else:
            PlayScene.drawPlayScene(self)

        pygame.display.flip()

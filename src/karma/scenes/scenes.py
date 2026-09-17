import pygame

from karma.enums import StateType, MusicType
from karma.scenes.playScene import PlayScene
from karma.scenes.menuScene import MenuScene
from karma.settings import SOUNDS_DIR

class Scene:
    current_music: MusicType | None = None

    @staticmethod
    def playMusic(music: MusicType):
        if Scene.current_music == music:
            return

        music_files = {
            MusicType.Menu: SOUNDS_DIR / "MenuMusic.mp3",
            MusicType.Day: SOUNDS_DIR / "DayMusic.mp3",
            MusicType.Night: SOUNDS_DIR / "NightMusic.mp3",
        }
        path = music_files.get(music)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        Scene.current_music = music

    def updateScenes(self, dt: float) -> None:
        if self.state in (StateType.Menu, StateType.Credits, StateType.HowToPlay):
            Scene.playMusic(MusicType.Menu)
        elif self.state in (StateType.Play, StateType.Pause, StateType.Cinematic):
            track = MusicType.Day if self.cycle_system.isDay else MusicType.Night
            Scene.playMusic(track)

        if self.state == StateType.Play:
            PlayScene.updatePlayScene(self, dt)
        elif self.state == StateType.Pause and self.paused_from_explosion:
            self.update_explosion(dt)
        elif self.state == StateType.Cinematic:
            self.update_cinematic(dt)

    def drawScenes(self) -> None:
        # Rendu graphique
        if self.state in (StateType.Menu, StateType.Credits, StateType.BadEnding, StateType.GoodEnding, StateType.HowToPlay):
            MenuScene.drawMenuScene(self, self.state)
        elif self.state == StateType.Cinematic:
            self.cinematic_player.draw(self.screen)
        elif self.state == StateType.Pause and self.paused_from_explosion:
            PlayScene.drawPlayScene(self)
        elif self.state == StateType.Pause and self.paused_from_cinematic:
            self.cinematic_player.draw(self.screen)
            self.pause_menu.draw(self.screen)
        else:
            PlayScene.drawPlayScene(self)

        pygame.display.flip()

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

    @staticmethod
    def updateScenes(game, dt: float) -> None:
        if game.state in (StateType.Menu, StateType.Credits, StateType.HowToPlay):
            Scene.playMusic(MusicType.Menu)
        elif game.state in (StateType.Play, StateType.Pause, StateType.Cinematic):
            track = MusicType.Day if game.cycle_system.isDay else MusicType.Night
            Scene.playMusic(track)

        if game.state == StateType.Play:
            PlayScene.updatePlayScene(game, dt)
        elif game.state == StateType.Pause and game.paused_from_explosion:
            game.update_explosion(dt)
        elif game.state == StateType.Cinematic:
            game.update_cinematic(dt)

    @staticmethod
    def drawScenes(game) -> None:
        # Rendu graphique
        if game.state in (StateType.Menu, StateType.Credits, StateType.BadEnding, StateType.MidEnding, StateType.GoodEnding, StateType.HowToPlay):
            MenuScene.drawMenuScene(game, game.state)
        elif game.state == StateType.Cinematic:
            game.cinematic_player.draw(game.screen)
        elif game.state == StateType.Pause and game.paused_from_explosion:
            PlayScene.drawPlayScene(game)
        elif game.state == StateType.Pause and game.paused_from_cinematic:
            game.cinematic_player.draw(game.screen)
            game.pause_menu.draw(game.screen)
        else:
            PlayScene.drawPlayScene(game)

        pygame.display.flip()

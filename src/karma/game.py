import sys
import pygame

from karma.entities.player.player import Player
from karma.environment.map import MapManager
from karma.interface.menu import MainMenu, PauseMenu
from karma.settings import (
    ASSETS_DIR,
    COLOR_BG,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
)

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running: bool = True
        self.state: str = "MENU"  # États possibles : "MENU", "PLAY", "PAUSE"

        self.player = Player(name="Blanchon", position=pygame.Vector2(100, 100), speed=0.3)
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        self.map_manager = MapManager(ASSETS_DIR / "nightMap.tmx")

    def handle_events(self) -> None:
        # Gestion des entrées utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == "MENU":
                action = self.main_menu.handle_event(event)
                if action == "PLAY":
                    self.state = "PLAY"
                elif action == "QUIT":
                    self.running = False

            elif self.state == "PLAY":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "PAUSE"

            elif self.state == "PAUSE":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "PLAY"
                else:
                    action = self.pause_menu.handle_event(event)
                    if action == "RESUME":
                        self.state = "PLAY"
                    elif action == "MENU":
                        self.state = "MENU"
                    elif action == "QUIT":
                        self.running = False

    def update(self, dt: float) -> None:
        # Mise à jour de la physique et des entités (seulement quand on joue)
        if self.state == "PLAY":
            self.player.update(dt)

    def draw(self) -> None:
        # Rendu graphique
        self.screen.fill(COLOR_BG)

        if self.state == "MENU":
            self.main_menu.draw(self.screen)
        else:
            # En PLAY ou en PAUSE, le jeu reste visible en arrière-plan
            self.map_manager.render(self.screen)
            self.player.draw(self.screen, (255, 255, 255))

            if self.state == "PAUSE":
                self.pause_menu.draw(self.screen)

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self.handle_events()
            dt = self.clock.tick(FPS)
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()
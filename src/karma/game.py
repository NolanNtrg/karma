import sys 
import pygame 
from karma.interface.menu import Menu
from karma.entities.player.player import Player
from karma.settings import (
    COLOR_BG,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
)
from karma.environment.map import MapManager
from karma.settings import ASSETS_DIR

class Game:
    def __init__(self): 
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
        pygame.display.set_caption(TITLE) 
        self.clock = pygame.time.Clock()
        self.running: bool = True 
        self.state = "MENU" # Etat du menu, peut être "MENU", "PLAY"
        self.player = Player(name="Blanchon", position=pygame.Vector2(100, 100), speed=0.3)
        self.menu = Menu(title="Karma",title_color="white")
        self.map_manager = MapManager(ASSETS_DIR / "nightMap.tmx")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.state == "MENU":
                    action = self.menu.handle_event(event)
                    if action == "PLAY":
                        self.state = "PLAY"
                    elif action == "QUIT":
                        self.running = False


            dt = self.clock.tick(FPS)
            self.screen.fill(COLOR_BG)

            if self.state == "MENU":
                self.menu.draw(self.screen)
            elif self.state == "PLAY":
                self.map_manager.render(self.screen)
                self.player.update(dt)
                self.player.draw(self.screen, (255, 255, 255))

            pygame.display.flip()

        pygame.quit()
        sys.exit()
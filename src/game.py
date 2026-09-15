import sys 
import pygame 
from entities.player import Player
from settings import (
    COLOR_BG,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
)

class Game:
    def __init__(self): 
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
        pygame.display.set_caption(TITLE) 
        self.clock = pygame.time.Clock()
        self.player = Player(name="Blanchon", position=pygame.Vector2(100, 100), speed=0.3)
        self.running: bool = True 

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            dt = self.clock.tick(FPS)
            self.screen.fill(COLOR_BG)

            self.player.update(dt)
            self.player.draw(self.screen, (255, 255, 255))

            pygame.display.flip()

        pygame.quit()
        sys.exit()
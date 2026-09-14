import sys 
import pygame 
from src.settings import (
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
        self.running = True 

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(COLOR_BG)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
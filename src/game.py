import sys 
import pygame 
from interface.menu import Menu
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
        self.running: bool = True 
        self.state = "MENU" # Etat du menu, peut être "MENU", "PLAY"
        self.menu = Menu(title="Karma",title_color="white")

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


            self.screen.fill(COLOR_BG)

            if self.state == "MENU":
                self.menu.draw(self.screen)
            elif self.state == "PLAY":
                pass # mettre le dessin du jeu ici 

            pygame.display.flip()
            self.clock.tick(FPS)


        pygame.quit()
        sys.exit()
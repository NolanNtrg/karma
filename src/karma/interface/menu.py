import pygame
from interface.button import Button
from settings import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

class Menu: 
    def __init__(self, title,title_color):
        self.police_size = 60
        self.font = pygame.font.Font(None, self.police_size)
        self.title_menu = self.font.render(title,False, title_color) # transforme le texte en image
        self.text_menu = self.title_menu.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)) # centre le texte sur l'écran

        self.btn_play = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, 200, 60, "Jouer", "white", "blue")
        self.btn_quit = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 60, "Quitter", "white", "red")

    def draw(self, screen):
        screen.blit(self.title_menu, self.text_menu) # sert à superposer le texte sur l'écran
        self.btn_play.draw(screen)
        self.btn_quit.draw(screen)

    def handle_event(self, event):
        if self.btn_play.is_clicked(event):
            return "PLAY" 
        elif self.btn_quit.is_clicked(event):
            return "QUIT"
        else : 
            return None




import pygame

from karma.enums import StateType, ResolutionType
from karma.interface.button import Button
from karma.settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Menu:
    # Classe mère pour tous les menus du jeu
    def __init__(self, title: str, title_color: str = "white") -> None:
        self.font = pygame.font.Font(None, 60)
        self.title_surface = self.font.render(title, False, title_color)
        self.title_rect = self.title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.buttons: list[tuple[Button, str]] = []

    def add_button(self, text: str, action: str, bg_color: tuple) -> None:
        width, height = 200, 50 
        x = (SCREEN_WIDTH - width) // 2 # centre le bouton horizontalement
        button = Button(x, SCREEN_HEIGHT // 2 - 50 + 70 * len(self.buttons), width, height, text, "white", bg_color)
        self.buttons.append((button, action))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.title_surface, self.title_rect)
        for button, _ in self.buttons:
            button.draw(screen)

    def handle_event(self, event: pygame.event.Event) -> str | None:
        for button, action in self.buttons:
            if button.is_clicked(event):
                return action
        return None


class MainMenu(Menu):
    # Menu principal affiché au lancement du jeu
    def __init__(self) -> None:
        super().__init__(title="Karma", title_color="white")
        self.add_button("Jouer", StateType.Play, "blue")
        self.add_button("Quitter", StateType.Quit, "red")


class PauseMenu(Menu):
    # Menu affiché lorsque le jeu est en pause
    def __init__(self) -> None:
        super().__init__(title="PAUSE", title_color="white")
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.set_alpha(140)  # ~55% d'opacité (ajuste entre 100 et 180 selon le résultat voulu)
        self.overlay.fill((0, 0, 0))
        
        self.add_button("Reprendre", StateType.Play, (40, 140, 60))
        self.add_button("Menu Principal", StateType.Menu, (50, 90, 180))
        self.add_button("Plein écran", ResolutionType.Fullscreen, (255, 90, 90))
        self.add_button("Quitter", StateType.Quit, (180, 40, 40))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.overlay, (0, 0))
        super().draw(screen)
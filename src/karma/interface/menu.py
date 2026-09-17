from typing import Any
import pygame

from karma.enums import StateType, ResolutionType, VolumeAction
from karma.interface.button import Button
from karma.settings import SCREEN_HEIGHT, SCREEN_WIDTH, ASSETS_DIR
from karma.systems.scoreManager import ScoreManager

class Menu:
    # Classe mère pour tous les menus du jeu
    def __init__(self, title: str = "", title_color: str = "white") -> None:
        self.font = pygame.font.Font(ASSETS_DIR / "fonts" / "Pixelify_Sans" / "static" / "PixelifySans-Bold.ttf", 30)
        self.title_surface = self.font.render(title, False, title_color)
        self.title_rect = self.title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.buttons: list[tuple[Button, Any]] = []
        self.texts: list[tuple[pygame.Surface, pygame.Rect]] = []

    def add_button(self, text: str, action: Any, oneButton: bool = False) -> Button:
        width, height = 300, 110
        x = (SCREEN_WIDTH - width) // 2 # centre le bouton horizontalement
        if oneButton:
            button = Button(x, SCREEN_HEIGHT - 140, width, height, text, "white")
        else:
            button = Button(x, 210 + 85 * len(self.buttons), width, height, text, "white")
        self.buttons.append((button, action))
        return button

    def add_text(self, text: str) -> None:
        surface = self.font.render(text, False, "white")
        y = 250 + len(self.texts) * 50
        rect = surface.get_rect(centerx=SCREEN_WIDTH // 2, top=y)
        self.texts.append((surface, rect))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.title_surface, self.title_rect)
        for button, _ in self.buttons:
            button.draw(screen)
        for surface, rect in self.texts:
            screen.blit(surface,rect)

    def handle_event(self, event: pygame.event.Event) -> Any:
        for button, action in self.buttons:
            if button.is_clicked(event):
                return action
        return None


class MainMenu(Menu):
    # Menu principal affiché au lancement du jeu
    def __init__(self, initial_volume: float = 1.0) -> None:
        super().__init__(title_color="white")
        self.add_button("Jouer", StateType.Play)
        vol_text = f"Volume : {int(initial_volume * 100)}%" if initial_volume > 0 else "Volume : Muet"
        self.volume_button = self.add_button(vol_text, VolumeAction.Cycle)
        self.add_button("Plein écran", ResolutionType.Fullscreen)
        self.add_button("Crédits", StateType.Credits)
        self.add_button("Quitter", StateType.Quit)

    def update_volume_text(self, volume: float) -> None:
        text = f"Volume : {int(volume * 100)}%" if volume > 0 else "Volume : Muet"
        self.volume_button.set_text(text)

class PauseMenu(Menu):
    # Menu affiché lorsque le jeu est en pause
    def __init__(self, initial_volume: float = 1.0) -> None:
        super().__init__(title="PAUSE", title_color="white")
        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.overlay.set_alpha(140)
        self.overlay.fill((0, 0, 0))
        
        self.add_button("Reprendre", StateType.Play)
        vol_text = f"Volume : {int(initial_volume * 100)}%" if initial_volume > 0 else "Volume : Muet"
        self.volume_button = self.add_button(vol_text, VolumeAction.Cycle)
        self.add_button("Menu Principal", StateType.Menu)
        self.add_button("Plein écran", ResolutionType.Fullscreen)
        self.add_button("Quitter", StateType.Quit)

    def update_volume_text(self, volume: float) -> None:
        text = f"Volume : {int(volume * 100)}%" if volume > 0 else "Volume : Muet"
        self.volume_button.set_text(text)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.overlay, (0, 0))
        super().draw(screen)

class CreditsMenu(Menu):
    def __init__(self) -> None:
        super().__init__(title_color="white")
        self.add_text("Menus, joueur, système de ressources créés par Nolan")
        self.add_text("Map, sound design, cinématiques et lore créés par Macéo")
        self.add_text("Assets, bâtiments, caméra créés par Enzo")
        self.add_text("Base, architecture, ennemis créés par Gabriel")
        self.add_text("Cycle d'éclipse, musiques, placement des bâtiments créés par Paul")
        self.add_text("Merci d'avoir joué !")
        self.add_button("Retour", StateType.Menu, True)

class GameOverMenu(Menu):
    def __init__(self) -> None:
        super().__init__()
        score: int = int(ScoreManager.calculateScore())
        self.add_button("Recommencer", StateType.Play)
        self.add_text("Score : " + str(score))
        self.add_button("Quitter", StateType.Quit, True)
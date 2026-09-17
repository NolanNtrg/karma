import pygame

from karma.settings import ASSETS_DIR, SOUNDS_DIR

class Button : 

    click_sound = None

    def __init__(self, x, y, width, height, text,color, font_size=25):
        if Button.click_sound is None:
            Button.click_sound = pygame.mixer.Sound(SOUNDS_DIR / "minecraft-click.mp3")
        self.background = pygame.image.load(ASSETS_DIR / "Button_Background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (width, height))
        self.rect = self.background.get_rect(topleft=(x, y))
        # hitbox réduit pour la hitbox
        self.hitbox = self.rect.inflate(-int(width * 0.12), -int(height * 0.5))
        self.text = text
        self.font = pygame.font.Font(ASSETS_DIR / "fonts" / "Pixelify_Sans" / "static" / "PixelifySans-Bold.ttf", font_size)
        self.color = color  # Color for the text
        self.mouse_pos = pygame.mouse.get_pos()

        self.text_surface = self.font.render(self.text,False, self.color) # transforme le texte en image
        self.text_rect = self.text_surface.get_rect(center=self.rect.center) # centre le texte sur le rectangle

    def set_text(self, text: str) -> None:
        self.text = text
        self.text_surface = self.font.render(self.text, False, self.color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.background, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hitbox.collidepoint(event.pos): # on vérifie si le clic est dans la zone visible du bouton
                Button.click_sound.play()
                return True
        return False
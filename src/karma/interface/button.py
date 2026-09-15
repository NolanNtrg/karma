import pygame

class Button : 
    def __init__(self, x, y, width, height, text,color,bg_color, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.color = color  # Color for the text
        self.bg_color = bg_color  # Color for the button background
        self.mouse_pos = pygame.mouse.get_pos()

        self.text_surface = self.font.render(self.text,False, self.color) # transforme le texte en image
        self.text_rect = self.text_surface.get_rect(center=self.rect.center) # centre le texte sur le rectangle


    def draw(self, screen):
        
        pygame.draw.rect(screen, self.bg_color, self.rect) # dessine le bouton avec la couleur de fond
        screen.blit(self.text_surface, self.text_rect) # sert à superposer le texte sur le rectangle en fond

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos) # on vérifie si le clic est dans le rectangle du bouton
        return False
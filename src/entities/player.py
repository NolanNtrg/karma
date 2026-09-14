import pygame;
import src.entities;

class Player():
    # Déclaration des variables de classes
    health: int = 100
    
    # Constructeur
    def __init__(self, name: str, position: pygame.Vector2):
        # Déclatation des variables d'instances
        self.name: str = "Blanchon"


    # Handler du mouvement du player
    def inputHandler(self) -> type:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            self.x -= 0.3 * dt
        if keys[pygame.K_d]:
            self.x += 0.3 * dt
        if keys[pygame.K_a]:
            self.y -= 0.3 * dt
        if keys[pygame.K_q]:
            self.y += 0.3 * dt
    
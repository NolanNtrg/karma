import pygame;

class Player():
    # Déclaration des variables de classes
    health: int = 100
    
    # Constructeur
    def __init__(self, name: str, position: pygame.Vector2):
        # Déclatation des variables d'instances
        self.name: str = name
        self.position: pygame.Vector2 = position

    
    def draw(self, screen: pygame.Surface, color: tuple) -> None:
        # Rectangle pour le joueur
        pygame.draw.rect(screen, color, (*self.position, 32, 32))

    # Handler du mouvement du player
    def inputHandler(self, screen: pygame.Surface, dt: int) -> type:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.position.x -= 0.3 * dt
            self.draw(screen, (255, 0, 0))
        elif keys[pygame.K_d]:
            self.position.x += 0.3 * dt
            self.draw(screen, (255, 255, 0))
        elif keys[pygame.K_z]:
            self.position.y -= 0.3 * dt
            self.draw(screen, (0, 255, 0))
        elif keys[pygame.K_s]:
            self.position.y += 0.3 * dt
            self.draw(screen, (0, 0, 255))
        else:
            self.draw(screen, (255, 255, 255))


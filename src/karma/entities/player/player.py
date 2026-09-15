import pygame

from karma.entities.core.entity import Entity


class Player(Entity):
    # Constructeur
    def __init__(self, name: str, position: pygame.Vector2, speed: float, health: int = 100) -> None:
        super().__init__(position, health)
        self.name = name
        self.speed = speed

    # Récupère la direction du joueur et sort un vecteur normalisé de sa direction
    def getDirection(self) -> pygame.Vector2:
        keys = pygame.key.get_pressed()
        dx: float = (keys[pygame.K_d] - keys[pygame.K_q])
        dy: float = (keys[pygame.K_s] - keys[pygame.K_z])
        direction: pygame.Vector2 = pygame.Vector2(dx, dy)

        if direction.length_squared() == 0:
            return direction

        return direction.normalize()

    def update(self, dt: float) -> None:
        direction = self.getDirection()
        self.position += direction * self.speed * dt

    def draw(self, screen: pygame.Surface, color: tuple) -> None:
        # Rectangle pour le joueur
        rect = pygame.Rect(self.position.x, self.position.y, 32, 32)
        pygame.draw.rect(screen, color, rect)

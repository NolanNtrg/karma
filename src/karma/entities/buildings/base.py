import pygame

from karma.entities.entity import Entity


class Base(Entity):
    # Représente la base du joueur

    RADIUS: int = 20

    def __init__(self, position: pygame.Vector2, health: int) -> None:
        super().__init__(position, health)

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        # Placeholder simple en attendant un sprite de vaisseau.
        position = camera.apply(self.position) if camera else self.position
        pygame.draw.circle(screen, (80, 200, 255), position, self.RADIUS)
        pygame.draw.circle(screen, (10, 40, 60), position, self.RADIUS, width=2)

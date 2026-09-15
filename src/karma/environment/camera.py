import pygame


class Camera:
    # Suit une cible et calcule le décalage à appliquer au rendu

    def __init__(self, screen_width: int, screen_height: int, map_width: float | None = None, map_height: float | None = None) -> None:
        self.width: int = screen_width
        self.height: int = screen_height
        self.map_width: float | None = map_width
        self.map_height: float | None = map_height
        self.offset: pygame.Vector2 = pygame.Vector2(0, 0)

    def update(self, target_position: pygame.Vector2) -> None:
        x = target_position.x - self.width / 2
        y = target_position.y - self.height / 2

        if self.map_width is not None:
            x = max(0, min(x, max(0, self.map_width - self.width)))
        if self.map_height is not None:
            y = max(0, min(y, max(0, self.map_height - self.height)))

        self.offset.update(x, y)

    def apply(self, position: pygame.Vector2) -> pygame.Vector2:
        return position - self.offset

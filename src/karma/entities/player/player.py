import pygame
from karma.settings import ASSETS_DIR

from karma.entities.entity import Entity
from karma.entities.sprite import SpriteAnimator


class Player(Entity):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    # Constructeur
    def __init__(self, name: str, position: pygame.Vector2, speed: float, health: int = 100) -> None:
        if self._initialized:
            return
        super().__init__(position, health)
        self.name: str = name
        self.speed: float = speed

        self.animator = SpriteAnimator(
                ASSETS_DIR / "Soldiers" / "SquadLeader.png",
                idleFrameCoords=[(0, 0), (0, 1)],
                walkFrameCoords=[(1, 0), (1, 1)],
            )
        return self.instance


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
        self.animator.update(dt, direction.length_squared() > 0, direction)

    def getCenter(self) -> pygame.Vector2:
        return self.position + pygame.Vector2(self.animator.image.get_size()) / 2

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        position = camera.apply(self.position) if camera else self.position
        screen.blit(self.animator.image, position)

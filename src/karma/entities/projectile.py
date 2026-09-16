import pygame

_SPEED = 0.6  # pixels par ms


class Projectile:
    # Effet visuel d'une tourelle vers sa cible (les dégâts sont déjà appliqués par la tourelle)

    def __init__(self, position: pygame.Vector2, targetPosition: pygame.Vector2, frames: list[pygame.Surface]) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(position)
        self.targetPosition: pygame.Vector2 = pygame.Vector2(targetPosition)
        self.frames: list[pygame.Surface] = frames
        self.imageIndex: float = 0.0
        self.reached: bool = False

    def update(self, dt: float) -> None:
        direction = self.targetPosition - self.position
        distance = direction.length()
        if distance <= _SPEED * dt:
            self.reached = True
            return
        self.position += direction.normalize() * _SPEED * dt
        self.imageIndex += dt * 0.02

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        position = camera.apply(self.position) if camera else self.position
        frame = self.frames[int(self.imageIndex) % len(self.frames)]
        screen.blit(frame, frame.get_rect(center=(int(position.x), int(position.y))))

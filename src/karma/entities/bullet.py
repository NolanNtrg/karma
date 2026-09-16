import pygame

from karma.entities.enemies.enemy import Enemy


class Bullet:
    # Projectile qui vole vers un ennemi et lui inflige des dégâts à l'impact.

    def __init__(self, position: pygame.Vector2, target: Enemy, damage: int, speed: float, image: pygame.Surface) -> None:
        self.position: pygame.Vector2 = pygame.Vector2(position)
        self.target: Enemy = target
        self.damage: int = damage
        self.speed: float = speed
        self.image: pygame.Surface = image
        self.hit: bool = False

    def update(self, dt: float) -> None:
        if self.target.isDestroyed():
            self.hit = True
            return

        direction = self.target.position - self.position
        step = self.speed * dt

        if direction.length() <= step:
            self.target.takeDamage(self.damage)
            self.hit = True
            return

        self.position += direction.normalize() * step

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        position = camera.apply(self.position) if camera else self.position
        screen.blit(self.image, position)

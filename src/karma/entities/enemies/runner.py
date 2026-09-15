import pygame

from karma.entities.enemies.enemy import Enemy
from karma.settings import ASSETS_DIR


class Runner(Enemy):
    # Coureur : ennemi rapide et fragile, faibles dégâts.

    def __init__(self, position: pygame.Vector2, target: pygame.Vector2) -> None:
        super().__init__(
            position,
            health=100,
            target=target,
            speed=32 / 1000,
            attackDamage=70,
            attackInterval=1000.0,
            spriteSheetPath=ASSETS_DIR / "Robots" / "Spider.png",
            idleFrameCoords=[(0, 0), (0, 1)],
            walkFrameCoords=[(1, 0), (1, 1), (1, 2), (1, 3)],
        )

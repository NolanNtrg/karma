import pygame

from karma.entities.enemies.enemy import Enemy
from karma.settings import ASSETS_DIR


class Prowler(Enemy):
    # Rôdeur : ennemi standard, équilibré entre vie et dégâts.

    def __init__(self, position: pygame.Vector2, target: pygame.Vector2) -> None:
        super().__init__(
            position,
            health=250,
            target=target,
            speed=24 / 1000,
            attackDamage=245,
            attackInterval=1000.0,
            spriteSheetPath=ASSETS_DIR / "Robots" / "Scarab.png",
            idleFrameCoords=[(0, 0), (0, 1)],
            walkFrameCoords=[(1, 0), (1, 1), (1, 2), (1, 3)],
        )

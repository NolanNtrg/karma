import pygame

from karma.entities.enemies.enemy import Enemy
from karma.settings import (ASSETS_DIR,
    PROWLER_ATTACK_DAMAGE,
    PROWLER_ATTACK_INTERVAL,
    PROWLER_HEALTH,
    PROWLER_SPEED,
)


class Prowler(Enemy):
    # Rôdeur : ennemi standard, équilibré entre vie et dégâts.

    def __init__(self, position: pygame.Vector2, target: pygame.Vector2) -> None:
        super().__init__(
            position,
            health=PROWLER_HEALTH,
            target=target,
            speed=PROWLER_SPEED,
            attackDamage=PROWLER_ATTACK_DAMAGE,
            attackInterval=PROWLER_ATTACK_INTERVAL,
            spriteSheetPath=ASSETS_DIR / "Robots" / "Scarab.png",
            idleFrameCoords=[(0, 0), (0, 1)],
            walkFrameCoords=[(1, 0), (1, 1), (1, 2), (1, 3)],
        )

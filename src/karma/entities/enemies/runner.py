import pygame

from karma.entities.enemies.enemy import Enemy
from karma.settings import (
    ASSETS_DIR,
    RUNNER_ATTACK_DAMAGE,
    RUNNER_ATTACK_INTERVAL,
    RUNNER_HEALTH,
    RUNNER_SPEED,
)


class Runner(Enemy):
    # Coureur : ennemi rapide et fragile, faibles dégâts.

    def __init__(self, position: pygame.Vector2, target: pygame.Vector2) -> None:
        super().__init__(
            position,
            health=RUNNER_HEALTH,
            target=target,
            speed=RUNNER_SPEED,
            attackDamage=RUNNER_ATTACK_DAMAGE,
            attackInterval=RUNNER_ATTACK_INTERVAL,
            spriteSheetPath=ASSETS_DIR / "Robots" / "Spider.png",
            idleFrameCoords=[(0, 0), (0, 1)],
            walkFrameCoords=[(1, 0), (1, 1), (1, 2), (1, 3)],
        )

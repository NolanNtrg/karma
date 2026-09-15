import random

import pygame

from karma.entities.enemies.armored_unit import ArmoredUnit
from karma.entities.enemies.enemy import Enemy
from karma.entities.enemies.prowler import Prowler
from karma.entities.enemies.runner import Runner

ENEMY_TYPES: list[type[Enemy]] = [Prowler, Runner, ArmoredUnit]


class EnemySpawner:
    # Fait apparaître des ennemis sur les bords de la carte pendant la nuit.

    def __init__(self, mapWidth: float, mapHeight: float, spawnInterval: float) -> None:
        self.mapWidth: float = mapWidth
        self.mapHeight: float = mapHeight
        self.spawnInterval: float = spawnInterval
        self.timeSinceLastSpawn: float = 0.0

    def getRandomEdgePosition(self) -> pygame.Vector2:
        # Choisit un point aléatoire sur un des quatre bords de la carte.
        side = random.choice(("top", "bottom", "left", "right"))
        if side == "top":
            return pygame.Vector2(random.uniform(0, self.mapWidth), 0)
        if side == "bottom":
            return pygame.Vector2(random.uniform(0, self.mapWidth), self.mapHeight)
        if side == "left":
            return pygame.Vector2(0, random.uniform(0, self.mapHeight))
        return pygame.Vector2(self.mapWidth, random.uniform(0, self.mapHeight))

    def trySpawn(self, dt: float, isNight: bool, target: pygame.Vector2) -> Enemy | None:
        # Retourne un nouvel ennemi si le délai est écoulé et qu'il fait nuit.
        if not isNight:
            self.timeSinceLastSpawn = 0.0
            return None

        self.timeSinceLastSpawn += dt
        if self.timeSinceLastSpawn < self.spawnInterval:
            return None

        self.timeSinceLastSpawn = 0.0
        enemyClass = random.choice(ENEMY_TYPES)
        return enemyClass(self.getRandomEdgePosition(), target)

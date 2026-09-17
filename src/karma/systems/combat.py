import pygame

from karma.entities.buildings.base import Base
from karma.entities.buildings.building import Building
from karma.entities.buildings.wall import Wall
from karma.entities.enemies.enemy import Enemy
from karma.entities.enemies.spawner import EnemySpawner
from karma.enums import RessourceType
from karma.environment.camera import Camera
from karma.systems.resourceManager import RessourceManager
from karma.settings import (
    ENEMY_DAY_DIFFICULTY_FLOOR,
    ENEMY_DAY_DIFFICULTY_STEP,
    ENEMY_SPAWN_INTERVAL,
    ENEMY_SPAWN_INTERVAL_MIN,
    KARMA_MAX,
    KARMA_SPAWN_INFLUENCE,
)


class CombatSystem:
    # Gestion des combats

    def __init__(self, mapWidth: float, mapHeight: float, spawnInterval: float = ENEMY_SPAWN_INTERVAL) -> None:
        self.enemies: list[Enemy] = []
        self.baseSpawnInterval: float = spawnInterval
        self.enemySpawner = EnemySpawner(mapWidth, mapHeight, spawnInterval)

    def computeSpawnInterval(self, currentDay: int) -> float:
        # Le délai de base diminue avec les jours, puis le karma l'ajuste selon sa valeur
        dayFactor = max(ENEMY_DAY_DIFFICULTY_FLOOR, 1.0 - (currentDay - 1) * ENEMY_DAY_DIFFICULTY_STEP)
        karmaRatio = RessourceManager().getStock(RessourceType.Karma) / KARMA_MAX
        karmaFactor = 1.0 + karmaRatio * KARMA_SPAWN_INFLUENCE
        return max(ENEMY_SPAWN_INTERVAL_MIN, self.baseSpawnInterval * dayFactor * karmaFactor)

    def update(self, dt: float, isDay: bool, base: Base, walls: list[Wall], buildings: list[Building], currentDay: int = 1) -> None:
        # Apparition d'un ennemi la nuit si le délai est écoulé
        if not isDay:
            self.enemySpawner.spawnInterval = self.computeSpawnInterval(currentDay)
            target = pygame.Vector2(base.rect.center)
            newEnemy = self.enemySpawner.trySpawn(dt, True, target)
            if newEnemy is not None:
                self.enemies.append(newEnemy)
        else:
            self.enemySpawner.timeSinceLastSpawn = 0.0

        # Mise à jour des ennemis et de leurs attaques
        for enemy in self.enemies:
            enemy.update(dt, walls, buildings, base)

        # Nettoyage des ennemis éliminés
        self.enemies = [enemy for enemy in self.enemies if not enemy.isDestroyed()]

    def draw(self, surface: pygame.Surface, camera: Camera | None = None) -> None:
        for enemy in self.enemies:
            enemy.draw(surface, camera)

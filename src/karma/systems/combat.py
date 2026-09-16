import pygame

from karma.entities.buildings.base import Base
from karma.entities.buildings.wall import Wall
from karma.entities.enemies.enemy import Enemy
from karma.entities.enemies.spawner import EnemySpawner
from karma.environment.camera import Camera
from karma.settings import ENEMY_SPAWN_INTERVAL


class CombatSystem:
    # Gestion des combats

    def __init__(self, mapWidth: float, mapHeight: float, spawnInterval: float = ENEMY_SPAWN_INTERVAL) -> None:
        self.enemies: list[Enemy] = []
        self.enemySpawner = EnemySpawner(mapWidth, mapHeight, spawnInterval)

    def update(self, dt: float, isDay: bool, base: Base, walls: list[Wall]) -> None:
        # Apparition d'un ennemi la nuit si le délai est écoulé
        if not isDay:
            target = pygame.Vector2(base.rect.center)
            newEnemy = self.enemySpawner.trySpawn(dt, True, target)
            if newEnemy is not None:
                self.enemies.append(newEnemy)
        else:
            self.enemySpawner.timeSinceLastSpawn = 0.0

        # Mise à jour des ennemis et de leurs attaques
        for enemy in self.enemies:
            enemy.update(dt, walls, base)

        # Nettoyage des ennemis éliminés
        self.enemies = [enemy for enemy in self.enemies if not enemy.isDestroyed()]

    def draw(self, surface: pygame.Surface, camera: Camera | None = None) -> None:
        for enemy in self.enemies:
            enemy.draw(surface, camera)

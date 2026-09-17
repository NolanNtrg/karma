import random

import pygame

from karma.entities.buildings.base import Base
from karma.enums import RessourceType
from karma.systems.resourceManager import RessourceManager
from karma.settings import KARMA_MAX, KARMA_MIN
from karma.systems.combat import CombatSystem
from karma.systems.cycle import CycleSystem

SPAWN_WAVE_KEYS: dict[int, int] = {pygame.K_j: 25}


class CheatSystem:
    # Raccourcis de debug (G, H, J, K, L, M) pour tester rapidement le jeu

    def __init__(self, base: Base, cycle_system: CycleSystem, combat_system: CombatSystem, rm: RessourceManager) -> None:
        self.base = base
        self.cycle_system = cycle_system
        self.combat_system = combat_system
        self.rm = rm
        self.godmode: bool = False

    def handleKey(self, key: int) -> None:
        if key == pygame.K_g:
            self.toggleGodmode()
        elif key == pygame.K_h:
            self.skipPhase()
        elif key in SPAWN_WAVE_KEYS:
            self.spawnEnemies(SPAWN_WAVE_KEYS[key])
        elif key == pygame.K_k:
            self.maxResources()
        elif key == pygame.K_l:
            self.rm.setStock(RessourceType.Karma, KARMA_MAX)
        elif key == pygame.K_m:
            self.rm.setStock(RessourceType.Karma, KARMA_MIN)

    def toggleGodmode(self) -> None:
        # Le vaisseau ne prend plus de dégâts
        self.godmode = not self.godmode
        self.base.invincible = self.godmode

    def skipPhase(self) -> None:
        # Passe directement à la phase suivante (jour/nuit)
        self.cycle_system.cycleTimer = self.cycle_system.currentDuration()

    def spawnEnemies(self, count: int) -> None:
        target = pygame.Vector2(self.base.rect.center)
        spawner = self.combat_system.enemySpawner
        for _ in range(count):
            enemyClass = random.choice(spawner.ENEMY_TYPES)
            self.combat_system.enemies.append(enemyClass(spawner.getRandomEdgePosition(), target))

    def maxResources(self) -> None:
        self.rm.setStock(RessourceType.Energy, 9999)
        self.rm.setStock(RessourceType.RawMaterial, 9999)

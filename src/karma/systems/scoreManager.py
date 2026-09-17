import pygame

from karma.settings import INITIAL_SCORE
from karma.systems.resourceManager import RessourceManager, RessourceType
from karma.entities.bullet import Bullet
from karma.systems.cycle import CycleSystem

class ScoreManager: 

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        # Si l'instance n'existe pas encore, on la crée
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, initialScore: int = INITIAL_SCORE) -> None:
        if self._initialized :
            return
        self.score: float = initialScore
        self._initialized = True

    @staticmethod
    def calculateScore() -> float:
        karma: float = RessourceManager().getStock(RessourceType.Karma)
        totalEnemiesKilled: int = Bullet.enemies_killed
        cycleSystem = CycleSystem()
        numberDays: int = cycleSystem.currentDay
        factor = -2 if karma < 0 else 1

        score: float = totalEnemiesKilled * numberDays + factor * karma
        return int(score)

    @staticmethod
    def resetScore() -> None:
        Bullet.enemies_killed = 0
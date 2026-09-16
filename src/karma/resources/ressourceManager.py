from karma.settings import (
    RAW_MATERIAL_START,
    ENERGY_START,
    KARMA_START,
    KARMA_MIN,
    KARMA_MAX
)
from karma.enums import RessourceType
    
class RessourceManager:

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        # Si l'instance n'existe pas encore, on la crée
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, initialEnergy: float = ENERGY_START, initialRawMaterial: float = RAW_MATERIAL_START, initialKarma: float = KARMA_START) -> None:
        if self._initialized :
            return
        self.stocks: dict[RessourceType, float] = {
            RessourceType.Energy: initialEnergy,
            RessourceType.RawMaterial: initialRawMaterial,
            RessourceType.Karma: initialKarma
        }
        self._initialized = True

    def getStock(self, ressourceType: RessourceType) -> float:
        return self.stocks.get(ressourceType, 0)

    def hasEnough(self, ressourceType: RessourceType, amount: float) -> bool:
        if amount < 0:
            raise ValueError("Compared resources should be positive")
        return self.getStock(ressourceType) >= amount

    def add(self, ressourceType: RessourceType, amount: float) -> bool:
        if amount < 0:
            raise ValueError("Added resources should be positive")
        elif ressourceType == RessourceType.Karma and self.stocks[ressourceType] + amount >= KARMA_MAX:
            self.stocks[ressourceType] = KARMA_MAX
            return True
        else:
            self.stocks[ressourceType] += amount
            return True


    def consume(self, ressourceType: RessourceType, amount: float) -> bool:
        if amount < 0:
            raise ValueError("Consumed resources should be positive")
        elif ressourceType == RessourceType.Karma and self.stocks[ressourceType] - amount <= KARMA_MIN:
            self.stocks[ressourceType] = KARMA_MIN
            return True
        elif self.stocks[ressourceType] - amount < 0 and ressourceType != RessourceType.Karma:
            return False
        else:
            self.stocks[ressourceType] -= amount
            return True

    def applyKarmaDelta(self, delta: float) -> None:
        # Applique un delta de karma signé (positif ou négatif) en une seule méthode.
        if delta > 0:
            self.add(RessourceType.Karma, delta)
        elif delta < 0:
            self.consume(RessourceType.Karma, -delta)
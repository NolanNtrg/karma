from karma.settings import (
    RAW_MATERIAL_START,
    ENERGY_START,
    KARMA_START,
    KARMA_MIN,
    KARMA_MAX
)
from karma.enums import RessourceType
    
class RessourceManager:

    def __init__(self, initialEnergy: int = ENERGY_START, initialRawMaterial: int = RAW_MATERIAL_START, initialKarma: int = KARMA_START) -> None:
        self.stocks: dict[RessourceType, int] = {
            RessourceType.Energy: initialEnergy,
            RessourceType.RawMaterial: initialRawMaterial,
            RessourceType.Karma: initialKarma
        }

    def getStock(self, ressourceType: RessourceType) -> int:
        return self.stocks.get(ressourceType, 0)

    def hasEnough(self, ressourceType: RessourceType, amount: int) -> bool:
        if amount < 0:
            raise ValueError("Compared resources should be positive")
        return self.getStock(ressourceType) >= amount
            
    def add(self, ressourceType: RessourceType, amount: int) -> bool:
        if amount < 0:
            raise ValueError("Added resources should be positive")
        elif ressourceType == RessourceType.Karma and self.stocks[ressourceType] + amount >= KARMA_MAX:
            self.stocks[ressourceType] = KARMA_MAX
            return True
        else:
            self.stocks[ressourceType] += amount
            return True


    def consume(self, ressourceType: RessourceType, amount: int) -> bool:
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
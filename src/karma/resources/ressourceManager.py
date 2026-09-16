from karma.settings import (
    RAW_MATERIAL_START,
    ENERGY_START,
    KARMA_START,
    KARMA_MIN,
    KARMA_MAX
)
from karma.enums import RessourceType
    
class RessourceManager:

    def __init__(self, initialEnergy: int = ENERGY_START, initialRawMaterial: int = RAW_MATERIAL_START, initialKarma: float = KARMA_START) -> None:
        self.stocks: dict[RessourceType, float] = {
            RessourceType.Energy: initialEnergy,
            RessourceType.RawMaterial: initialRawMaterial,
            RessourceType.Karma: initialKarma
        }

    def getStock(self, ressourceType: RessourceType) -> float:
        return self.stocks.get(ressourceType, 0)

    def applyKarmaDelta(self, delta: float) -> None:
        # En float car le karma s'accumule par petites fractions à chaque frame
        newValue = self.stocks[RessourceType.Karma] + delta
        self.stocks[RessourceType.Karma] = max(KARMA_MIN, min(KARMA_MAX, newValue))

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
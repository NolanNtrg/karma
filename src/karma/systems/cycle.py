from karma.settings import DAY_DURATION, NIGHT_DURATION

class CycleSystem:
    # Gestion du temps et du cycle jour / nuit.

    _instance = None
    
    def __new__(cls, *args, **kwargs):
        # Si l'instance n'existe pas encore, on la crée (singleton)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, dayDuration: float = DAY_DURATION, nightDuration: float = NIGHT_DURATION) -> None:
        if self._initialized :
            return
        self.isDay: bool = True
        self.dayDuration: float = dayDuration
        self.nightDuration: float = nightDuration
        self.cycleTimer: float = 0.0
        self.currentDay: int = 1
        self._initialized = True
    
    def currentDuration(self) -> float:
        return self.dayDuration if self.isDay else self.nightDuration

    def update(self, dt: float) -> bool:
        # Retourne True si un changement de phase (jour <-> nuit) a eu lieu, et sinon retourne False.
        self.cycleTimer += dt
        if self.isDay and self.cycleTimer >= self.dayDuration:
            self.isDay = False
            self.cycleTimer = 0.0
            return True
        elif not self.isDay and self.cycleTimer >= self.nightDuration:
            self.isDay = True
            self.cycleTimer = 0.0
            self.currentDay += 1
            return True
        return False
    
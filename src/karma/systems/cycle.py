class CycleSystem:
    # Gestion du temps et du cycle jour / nuit.

    def __init__(self, dayDuration: float = 4000.0, nightDuration: float = 4000.0) -> None:
        self.isDay: bool = True
        self.dayDuration: float = dayDuration
        self.nightDuration: float = nightDuration
        self.cycleTimer: float = 0.0
        self.currentDay: int = 1

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

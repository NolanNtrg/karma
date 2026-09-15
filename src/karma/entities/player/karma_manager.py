from typing import Sequence

from karma.entities.buildings.building import Building
from karma.settings import KARMA_MAX, KARMA_MIN, KARMA_START


class KarmaManager:
    # Gère la jauge de karma selon les bâtiments actifs

    def __init__(self) -> None:
        self.karma: float = KARMA_START

    def update(self, dt: float, buildings: Sequence[Building]) -> None:
        # dt est exprimé en millisecondes.
        # buildings contient les bâtiments placés sur la carte.
        totalImpact: float = sum(building.getKarmaImpact(dt) for building in buildings)
        self.karma = max(KARMA_MIN, min(KARMA_MAX, self.karma + totalImpact))

    def isClean(self) -> bool:
        # Vrai si la jauge de karma est globalement positive
        return self.karma > 0

    def isDirty(self) -> bool:
        # Vrai si la jauge de karma est globalement négative
        return self.karma < 0

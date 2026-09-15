import pygame

from karma.entities.core.entity import Entity


class Building(Entity):
    # Classe mère de tout bâtiment constructible sur un socle : possède un coût
    # de construction en Énergie et un effet continu sur la jauge de karma
    # (positif si propre, négatif si sale, nul si neutre comme la Tourelle ou le Mur)

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        karmaImpact: float = 0.0,
    ) -> None:
        super().__init__(position, health)
        self.energyCost = energyCost
        self.karmaImpact = karmaImpact
        self.isActive = True

    def activate(self) -> None:
        # Rend le bâtiment fonctionnel (reprend son effet karma et sa production)
        self.isActive = True

    def deactivate(self) -> None:
        # Suspend le bâtiment sans le détruire (plus d'effet karma ni de production)
        self.isActive = False

    def isOperational(self) -> bool:
        # Vrai si le bâtiment est actif et n'a pas été détruit
        return self.isActive and not self.isDestroyed()

    def isClean(self) -> bool:
        # Vrai pour les variantes propres qui font monter le karma (ex : panneau solaire)
        return self.karmaImpact > 0

    def isDirty(self) -> bool:
        # Vrai pour les variantes sales qui font baisser le karma (ex : centrale à charbon)
        return self.karmaImpact < 0

    def getKarmaImpact(self, dt: float) -> float:
        # Effet sur la jauge de karma pour cette frame, 0 si inactif ou détruit
        # dt : temps écoulé depuis la dernière frame, en millisecondes
        if not self.isOperational():
            return 0.0
        return self.karmaImpact * dt

    def canAfford(self, availableEnergy: int) -> bool:
        # Vrai si le stock d'Énergie du joueur permet de construire ce bâtiment
        return availableEnergy >= self.energyCost

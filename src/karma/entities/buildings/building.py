import pygame

from karma.entities.entity import Entity


class Building(Entity):
    # Base des bâtiments constructibles avec un coût et un effet sur le karma.

    # Couleur de substitution utilisée tant qu'un bâtiment n'a pas de sprite dédié
    COLOR: tuple[int, int, int] = (150, 150, 150)
    SIZE: tuple[int, int] = (32, 32)

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        karmaImpact: float = 0.0,
    ) -> None:
        # Appel direct nécessaire à cause de l'héritage multiple de Turret.
        Entity.__init__(self, position, health)
        self.energyCost: int = energyCost
        self.karmaImpact: float = karmaImpact
        self.isActive: bool = True

    def activate(self) -> None:
        self.isActive = True

    def deactivate(self) -> None:
        # Désactive le bâtiment sans le détruire.
        self.isActive = False

    def isOperational(self) -> bool:
        # Indique si le bâtiment peut fonctionner.
        return self.isActive and not self.isDestroyed()

    def isClean(self) -> bool:
        # Indique si le bâtiment augmente le karma
        return self.karmaImpact > 0

    def isDirty(self) -> bool:
        # Indique si le bâtiment diminue le karma
        return self.karmaImpact < 0

    def getKarmaImpact(self, dt: float) -> float:
        # Calcule l'effet du bâtiment sur le karma pour cette frame.
        # dt est converti en minutes car karmaImpact est exprimé par minute.
        if not self.isOperational():
            return 0.0
        return self.karmaImpact * dt / 60000.0

    def canAfford(self, availableEnergy: int) -> bool:
        # Indique si le joueur peut payer le bâtiment.
        return availableEnergy >= self.energyCost

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        # Rendu par défaut (rectangle coloré) pour les bâtiments sans sprite dédié
        position = camera.apply(self.position) if camera else self.position
        rect = pygame.Rect(int(position.x), int(position.y), *self.SIZE)
        pygame.draw.rect(screen, self.COLOR, rect)
        pygame.draw.rect(screen, (20, 20, 20), rect, 2)

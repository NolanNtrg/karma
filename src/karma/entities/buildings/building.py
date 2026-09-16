import pygame

from karma.entities.entity import Entity
from karma.environment.camera import Camera


class Building(Entity):
    # Base des bâtiments constructibles avec un coût et un effet sur le karma.

    ANIMATION_SPEED: float = 0.006

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        karmaImpact: float = 0.0,
    ) -> None:
        super().__init__(position, health)
        self.energyCost: int = energyCost
        self.karmaImpact: float = karmaImpact
        self.isActive: bool = True

        self.dayFrames: list[pygame.Surface] = []
        self.nightFrames: list[pygame.Surface] = []
        self.imageIndex: float = 0.0
        self.image: pygame.Surface | None = None

    def setFrames(self, dayFrames: list[pygame.Surface], nightFrames: list[pygame.Surface]) -> None:
        # Enregistre les frames jour/nuit et affiche la première frame de jour.
        self.dayFrames = dayFrames
        self.nightFrames = nightFrames
        self.image = self.dayFrames[0]

    def updateSprite(self, dt: float, isDay: bool) -> None:
        # Anime le sprite courant et bascule entre les frames jour et nuit.
        frames = self.dayFrames if isDay else self.nightFrames
        if not frames:
            return
        self.imageIndex += dt * self.ANIMATION_SPEED
        self.image = frames[int(self.imageIndex) % len(frames)]

    def draw(self, screen: pygame.Surface, camera: Camera | None = None) -> None:
        # Affiche le sprite courant à la position du bâtiment, en tenant compte de la caméra.
        if self.image is None:
            return
        position = camera.apply(self.position) if camera else self.position
        screen.blit(self.image, position)

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
        # Calcule l'effet du bâtiment sur le karma pour cette frame
        if not self.isOperational():
            return 0.0
        # (dt converti en minutes car karmaImpact est exprimé par minute.)
        return self.karmaImpact * dt / 60000.0

    def canAfford(self, availableEnergy: int) -> bool:
        # Indique si le joueur peut payer le bâtiment.
        return availableEnergy >= self.energyCost

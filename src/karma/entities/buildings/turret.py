import pygame

from karma.entities.buildings.building import Building
from karma.entities.enemies.attacker import Attacker
from karma.entities.enemies.enemy import Enemy
from karma.settings import ASSETS_DIR

_BARREL_SIZE = (22, 8)

# Sur le sprite d'origine (449px de large), le canon ne pivote pas depuis son centre :
# le bloc de fixation est vers la gauche, le bout du canon vers la droite
_BARREL_PIVOT_FRACTION = 110 / 449
_BARREL_MUZZLE_FRACTION = 445 / 449


class Turret(Building, Attacker):
    # Tourelle statique qui attaque les ennemis proches

    def __init__(
        self,
        position: pygame.Vector2,
        health: int,
        energyCost: int,
        attackRange: float,
        attackDamage: int,
        attackInterval: float,
    ) -> None:
        Building.__init__(self, position, health, energyCost, karmaImpact=0.0)
        Attacker.__init__(self, position, health, attackRange, attackDamage, attackInterval)
        self.facingLeft: bool = False

        baseImg = pygame.image.load(ASSETS_DIR / "turrets" / "turret_day_base.png").convert_alpha()
        barrelImg = pygame.image.load(ASSETS_DIR / "turrets" / "turret_day_barrel.png").convert_alpha()
        self.baseImage = pygame.transform.scale(baseImg, self.SIZE)
        self.barrelImage = pygame.transform.scale(barrelImg, _BARREL_SIZE)
        self.barrelImageFlipped = pygame.transform.flip(self.barrelImage, True, False)

    def update(self, dt: float, enemies: list[Enemy]) -> Enemy | None:
        # Retourne la cible touchée si un tir vient de partir, sinon None
        if not self.isOperational():
            return None
        target = self.findClosestTarget(self.position, enemies)
        if target is None:
            return None

        self.facingLeft = target.position.x < self.position.x
        damage = self.tryAttack(dt)
        if not damage:
            return None

        target.takeDamage(damage)
        return target

    def getMuzzlePosition(self) -> pygame.Vector2:
        # Position (en coordonnées monde) du bout du canon, d'où partent les projectiles
        centerX = self.position.x + self.SIZE[0] / 2
        centerY = self.position.y + self.SIZE[1] / 2
        offset = (_BARREL_MUZZLE_FRACTION - _BARREL_PIVOT_FRACTION) * self.barrelImage.get_width()
        if self.facingLeft:
            return pygame.Vector2(centerX - offset, centerY)
        return pygame.Vector2(centerX + offset, centerY)

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        position = camera.apply(self.position) if camera else self.position
        screen.blit(self.baseImage, position)

        centerX = position.x + self.SIZE[0] / 2
        centerY = position.y + self.SIZE[1] / 2
        if self.facingLeft:
            barrel = self.barrelImageFlipped
            pivotX = (1 - _BARREL_PIVOT_FRACTION) * barrel.get_width()
        else:
            barrel = self.barrelImage
            pivotX = _BARREL_PIVOT_FRACTION * barrel.get_width()

        screen.blit(barrel, (centerX - pivotX, centerY - barrel.get_height() / 2))

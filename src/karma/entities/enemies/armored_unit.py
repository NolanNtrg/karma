import pygame

from karma.entities.enemies.enemy import Enemy
from karma.entities.sprite import SpriteAnimator
from karma.settings import ARMORED_UNIT_ATTACK_DAMAGE, ARMORED_UNIT_ATTACK_INTERVAL, ARMORED_UNIT_HEALTH, ARMORED_UNIT_SPEED, ASSETS_DIR


class ArmoredUnit(Enemy):
    # le centipède est puissant et résistant mais lent
    # l'image est un asset avec plusieurs directions mais on ne garde que ouest pour simplifier

    # ces valeurs fixent les lignes gardées dans le sprite sheet
    HEAD_ROW, BODY_ROW, TAIL_ROW, TAIL_COLUMN, FRAME_COUNT = 0, 9, 16, 0, 4

    SEGMENT_SPACING, ANIMATION_SPEED, PHASE_OFFSET = 13.0, 0.006, 120.0

    def __init__(self, position: pygame.Vector2, target: pygame.Vector2) -> None:
        super().__init__(
            position,
            health=ARMORED_UNIT_HEALTH,
            target=target,
            speed=ARMORED_UNIT_SPEED,
            attackDamage=ARMORED_UNIT_ATTACK_DAMAGE,
            attackInterval=ARMORED_UNIT_ATTACK_INTERVAL,
            spriteSheetPath=None,
        )
        self.spriteSheet = pygame.image.load(ASSETS_DIR / "Robots" / "Centipede.png").convert_alpha()
        self.segmentCount = 5
        self.animationTime = 0.0
        direction = target - position
        # on normalise la direction pour que la vitesse soit constante
        self.heading = direction.normalize() if direction.length_squared() > 0 else pygame.Vector2(0, 0)

    # override getCenter car contrairement aux autres ennemis, self.position est déjà
    # le centre de la tête (voir draw) et non le coin supérieur gauche d'un sprite
    def getCenter(self) -> pygame.Vector2:
        # la tête
        return self.getSegmentPosition(0)

    def getSegmentPosition(self, index: int) -> pygame.Vector2:
        return self.position - self.heading * self.SEGMENT_SPACING * index

    # une balle peut toucher n'importe quel segment du centipède, pas seulement la tête
    def getHitPoints(self) -> list[pygame.Vector2]:
        return [self.getSegmentPosition(index) for index in range(self.segmentCount)]

    # override updateAnimation juste pour MaJ la direction de l'ennemi
    def updateAnimation(self, dt: float, isMoving: bool, direction: pygame.Vector2) -> None:
        if isMoving and direction.length_squared() > 0:
            self.heading = direction.normalize()
        self.animationTime += dt

    # override draw pour dessiner le centipède en segments
    def draw(self, screen: pygame.Surface, camera=None) -> None:
        flip = self.heading.x < 0

         # queue d'abord, tête dessinée par-dessus
        for index in reversed(range(self.segmentCount)):
            # boucle sur les segments de la queue (4) à la tête (0) 
            # pour permettre à la tête de se draw au dessus des autres segments
            if index == self.segmentCount - 1:
                image = SpriteAnimator.getSprite(self.spriteSheet, self.TAIL_ROW, self.TAIL_COLUMN)
            else:
                # animation de vague dans le corps du centipède (déphase les segments pour que la vague se propage)
                frame = int((self.animationTime + index * self.PHASE_OFFSET) * self.ANIMATION_SPEED) % self.FRAME_COUNT
                image = SpriteAnimator.getSprite(self.spriteSheet, self.HEAD_ROW if index == 0 else self.BODY_ROW, frame)
            image = pygame.transform.flip(image, flip, False)

            # calcule la position du segment en fonction de l'index et de l'espacement
            position = self.getSegmentPosition(index)
            # on pose en prenant en compte adaptation au scroll camera
            position = camera.apply(position) if camera else position
            screen.blit(image, position - pygame.Vector2(image.get_size()) / 2)

import pygame

from karma.entities.enemies.enemy import Enemy
from karma.entities.sprite import SpriteAnimator
from karma.settings import ASSETS_DIR

# Centipede est un asset avec plusieurs directions mais on ne garde que ouest pour simplifier

# ces valeurs fixent les lignes gardées dans le sprite sheet 
HEAD_ROW, BODY_ROW, TAIL_ROW, TAIL_COLUMN, FRAME_COUNT = 0, 9, 16, 0, 4

SEGMENT_SPACING, ANIMATION_SPEED, PHASE_OFFSET = 13.0, 0.006, 120.0


class ArmoredUnit(Enemy):
    # le centipède est puissant et résistant mais lent

    def __init__(self, position: pygame.Vector2, target: pygame.Vector2) -> None:
        super().__init__(
            position, 
            health=6700, 
            target=target, 
            speed=16 / 1000,
            attackDamage=680, 
            attackInterval=1000.0, 
            spriteSheetPath=None,
        )
        self.spriteSheet = pygame.image.load(ASSETS_DIR / "Robots" / "Centipede.png").convert_alpha()
        self.segmentCount = 5
        self.animationTime = 0.0
        direction = target - position
        self.heading = direction.normalize() if direction.length_squared() > 0 else pygame.Vector2(1, 0)

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
                image = SpriteAnimator.getSprite(self.spriteSheet, TAIL_ROW, TAIL_COLUMN)
            else:
                frame = int((self.animationTime + index * PHASE_OFFSET) * ANIMATION_SPEED) % FRAME_COUNT
                image = SpriteAnimator.getSprite(self.spriteSheet, HEAD_ROW if index == 0 else BODY_ROW, frame)
            image = pygame.transform.flip(image, flip, False)

            # calcule la position du segment en fonction de l'index et de l'espacement
            position = self.position - self.heading * SEGMENT_SPACING * index
            # adaptation au scroll camera
            position = camera.apply(position) if camera else position
            screen.blit(image, position - pygame.Vector2(image.get_size()) / 2)

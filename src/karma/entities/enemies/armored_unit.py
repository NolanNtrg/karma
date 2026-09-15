import math

import pygame

from karma.entities.enemies.enemy import Enemy
from karma.settings import ASSETS_DIR

# Lignes 0-7 de Centipede.png : tête à 8 directions, la pince pointe dans le
# sens du déplacement, tous les 45° dans le sens antihoraire en partant de l'Est.
HEAD_FRAME_COUNT = 4
# Lignes 8-15 : segment de corps, seules 4 directions cardinales sont dessinées
# (les diagonales sont approximées par la direction cardinale dominante).
BODY_ROW_BY_DIRECTION: dict[str, int] = {"E": 9, "N": 10, "W": 11, "S": 8}
BODY_FRAME_COUNT = 4
# Ligne 16 : bout de queue sans pince. Les 8 colonnes ne sont pas une
# animation dans le temps mais un dégradé de lumière selon la direction (comme
# la tête) : on choisit une frame fixe selon le cap, sans la faire défiler.
TAIL_ROW = 16
TAIL_DIRECTION_COUNT = 8

SEGMENT_SPACING = 13.0
WALK_ANIMATION_SPEED = 0.006
SEGMENT_PHASE_OFFSET = 120.0


class ArmoredUnit(Enemy):
    # Blindé : ennemi lent avec énormément de vie et de dégâts, corps de
    # centipède à plusieurs segments qui suivent la tête en ligne droite.

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
        self.spriteSheet: pygame.Surface = pygame.image.load(ASSETS_DIR / "Robots" / "Centipede.png").convert_alpha()
        self.segmentCount: int = 5  # tête + 3 corps + queue
        self.animationTime: float = 0.0

        initialDirection = target - position
        self.heading: pygame.Vector2 = (
            initialDirection.normalize() if initialDirection.length_squared() > 0 else pygame.Vector2(1, 0)
        )

    def getDirectionBucket(self, heading: pygame.Vector2, bucketCount: int) -> int:
        # atan2(-y, x) : la coordonnée écran a l'axe Y inversé par rapport au
        # sens trigonométrique utilisé par la feuille de sprites.
        angleDegrees = math.degrees(math.atan2(-heading.y, heading.x)) % 360
        bucketSize = 360 / bucketCount
        return round(angleDegrees / bucketSize) % bucketCount

    def getBodyDirectionRow(self, heading: pygame.Vector2) -> int:
        # Pas de frame diagonale pour le corps : on garde l'axe dominant.
        if abs(heading.x) >= abs(heading.y):
            direction = "E" if heading.x >= 0 else "W"
        else:
            direction = "S" if heading.y >= 0 else "N"
        return BODY_ROW_BY_DIRECTION[direction]

    def updateAnimation(self, dt: float, isMoving: bool, direction: pygame.Vector2) -> None:
        # Garde le dernier cap connu pendant les phases d'attaque/arrêt.
        if isMoving and direction.length_squared() > 0:
            self.heading = direction.normalize()
        self.animationTime += dt

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        headRow = self.getDirectionBucket(self.heading, 8)
        bodyRow = self.getBodyDirectionRow(self.heading)
        tailColumn = self.getDirectionBucket(self.heading, TAIL_DIRECTION_COUNT)

        # De la queue vers la tête pour que la tête se dessine par-dessus.
        for index in reversed(range(self.segmentCount)):
            segmentPosition = self.position - self.heading * SEGMENT_SPACING * index

            if index == 0:
                phase = self.animationTime + index * SEGMENT_PHASE_OFFSET
                frame = int(phase * WALK_ANIMATION_SPEED) % HEAD_FRAME_COUNT
                image = self.getSprite(headRow, frame)
            elif index == self.segmentCount - 1:
                image = self.getSprite(TAIL_ROW, tailColumn)
            else:
                phase = self.animationTime + index * SEGMENT_PHASE_OFFSET
                frame = int(phase * WALK_ANIMATION_SPEED) % BODY_FRAME_COUNT
                image = self.getSprite(bodyRow, frame)

            drawPosition = camera.apply(segmentPosition) if camera else segmentPosition
            drawPosition -= pygame.Vector2(image.get_size()) / 2
            screen.blit(image, drawPosition)

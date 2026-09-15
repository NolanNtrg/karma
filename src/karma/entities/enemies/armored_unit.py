import pygame

from karma.entities.enemies.enemy import Enemy
from karma.settings import ASSETS_DIR

# Centipede.png n'a que 4 orientations dessinées par section (E, N, W, S) :
# les diagonales sont approximées par la direction cardinale la plus proche.
# Lignes 0-7 : tête, une orientation toutes les 2 lignes (les lignes impaires
# ne sont pas utilisées, elles couvrent les diagonales qu'on ignore ici).
HEAD_ROWS = {"E": 0, "N": 2, "W": 4, "S": 6}
HEAD_FRAME_COUNT = 4
# Lignes 8-15 : segment de corps.
BODY_ROWS = {"E": 9, "N": 10, "W": 11, "S": 8}
BODY_FRAME_COUNT = 4
# Ligne 16 : bout de queue sans pince, une frame fixe par direction (pas
# d'animation de marche sur la queue).
TAIL_ROW = 16
TAIL_COLUMNS = {"E": 0, "N": 2, "W": 4, "S": 6}

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

    def getCardinalDirection(self, heading: pygame.Vector2) -> str:
        # Pas de frame diagonale : on garde l'axe dominant (le plus grand des
        # deux déplacements, horizontal ou vertical) et son sens.
        if abs(heading.x) >= abs(heading.y):
            return "E" if heading.x >= 0 else "W"
        return "S" if heading.y >= 0 else "N"

    def updateAnimation(self, dt: float, isMoving: bool, direction: pygame.Vector2) -> None:
        # Garde le dernier cap connu pendant les phases d'attaque/arrêt.
        if isMoving and direction.length_squared() > 0:
            self.heading = direction.normalize()
        self.animationTime += dt

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        direction = self.getCardinalDirection(self.heading)
        headRow = HEAD_ROWS[direction]
        bodyRow = BODY_ROWS[direction]
        tailColumn = TAIL_COLUMNS[direction]

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

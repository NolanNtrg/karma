import pygame

from karma.entities.buildings.building import Building
from karma.entities.sprite import SpriteAnimator
from karma.settings import ASSETS_DIR

TILESET_DIR = ASSETS_DIR / "Robot Warfare Asset Pack 22-11-24" / "Tileset"
WALL_TILE_ROW = 2  # ligne 3 du tileset (première ligne = 1)
WALL_TILE_COL = 6  # colonne 7 du tileset (première colonne = 1)


class Wall(Building):
    # Mur de défense qui canalise les ennemis.

    def __init__(self, position: pygame.Vector2, health: int, energyCost: int) -> None:
        super().__init__(position, health, energyCost, karmaImpact=0.0)

        dayTileset = pygame.image.load(TILESET_DIR / "tilesetDay.png").convert_alpha()
        nightTileset = pygame.image.load(TILESET_DIR / "tilesetNight.png").convert_alpha()
        self.dayImage = SpriteAnimator.getSprite(dayTileset, WALL_TILE_ROW, WALL_TILE_COL)
        self.nightImage = SpriteAnimator.getSprite(nightTileset, WALL_TILE_ROW, WALL_TILE_COL)
        self.image = self.dayImage

    def update(self, isDay: bool) -> None:
        self.image = self.dayImage if isDay else self.nightImage

    def draw(self, screen: pygame.Surface, camera=None) -> None:
        position = camera.apply(self.position) if camera else self.position
        screen.blit(self.image, position)

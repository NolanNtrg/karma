from pathlib import Path

import pygame

from karma.entities.buildings.building import Building
from karma.entities.sprite import SpriteAnimator
from karma.settings import ASSETS_DIR


class Wall(Building):
    # Mur de défense qui canalise les ennemis.

    TILESET_DIR: Path = ASSETS_DIR / "Robot Warfare Asset Pack 22-11-24" / "Tileset"
    WALL_TILE_ROW: int = 2  # ligne 3 du tileset
    WALL_TILE_COL: int = 6  # col 7 du tileset

    def __init__(self, position: pygame.Vector2, health: int, energyCost: int) -> None:
        super().__init__(position, health, energyCost, karmaImpact=0.0)

        dayTileset = pygame.image.load(self.TILESET_DIR / "tilesetDay.png").convert_alpha()
        nightTileset = pygame.image.load(self.TILESET_DIR / "tilesetNight.png").convert_alpha()
        # une seule case du tileset, découpée pour représenter le mur
        dayTile = SpriteAnimator.getSprite(dayTileset, self.WALL_TILE_ROW, self.WALL_TILE_COL)
        nightTile = SpriteAnimator.getSprite(nightTileset, self.WALL_TILE_ROW, self.WALL_TILE_COL)
        self.setFrames([dayTile], [nightTile])

    def update(self, isDay: bool) -> None:
        self.updateSprite(0.0, isDay)

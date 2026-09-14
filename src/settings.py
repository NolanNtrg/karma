from pathlib import Path

BASE_DIR: str = Path(__file__).resolve().parent.parent

ASSETS_DIR: str = BASE_DIR / "assets"
MAPS_DIR: str = ASSETS_DIR / "maps"
SPRITES_DIR: str = ASSETS_DIR / "sprites"
SOUNDS_DIR: str = ASSETS_DIR / "sounds"

SCREEN_WIDTH: int = 1024
SCREEN_HEIGHT: int = 768
FPS: int = 60
TITLE: str = "Karma"

COLOR_BG: tuple[int, int, int] = (20, 20, 25)
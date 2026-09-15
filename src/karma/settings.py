from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR: Path = BASE_DIR / "assets"
MAPS_DIR: Path = ASSETS_DIR / "maps"
SPRITES_DIR: Path = ASSETS_DIR / "sprites"
SOUNDS_DIR: Path = ASSETS_DIR / "sounds"

SCREEN_WIDTH: int = 1024
SCREEN_HEIGHT: int = 768
FPS: int = 60
TITLE: str = "Karma"

# Facteur de zoom de la caméra (1.0 de base, grandi avec la valeur)
CAMERA_ZOOM: float = 2

COLOR_BG: tuple[int, int, int] = (20, 20, 25)

KARMA_START: float = 0.0
KARMA_MIN: float = -1000.0
KARMA_MAX: float = 1000.0

ENERGY_START = 100
RAW_MATERIAL_START = 500

BASE_HEALTH: int = 1000

# Délai en millisecondes entre deux apparitions d'ennemis pendant la nuit
ENEMY_SPAWN_INTERVAL: float = 1500.0

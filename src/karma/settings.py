from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR: Path = BASE_DIR / "assets"
MAPS_DIR: Path = ASSETS_DIR / "maps"
SPRITES_DIR: Path = ASSETS_DIR / "sprites"
SOUNDS_DIR: Path = ASSETS_DIR / "sounds"
VIDEO_DIR: Path = ASSETS_DIR / "video"

SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 720
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

# délai en ms entre deux apparitions d'ennemis
ENEMY_SPAWN_INTERVAL: float = 1500.0
# dlai minimum autorisé (pas d'exceptions)
ENEMY_SPAWN_INTERVAL_MIN: float = 300.0
# Réduction du délai de spawn par jour écoulé (33% par jour)
ENEMY_DAY_DIFFICULTY_STEP: float = 0.33
# Le délai ne descend jamais sous ce ratio du délai de base à cause des jours seuls
ENEMY_DAY_DIFFICULTY_FLOOR: float = 0.4
# influence du karma sur le délai de spawn
KARMA_SPAWN_INFLUENCE: float = 0.5

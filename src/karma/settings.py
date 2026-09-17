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
DEFAULT_VOLUME: float = 1.0

# Facteur de zoom de la caméra (1.0 de base, grandi avec la valeur)
CAMERA_ZOOM: float = 2

COLOR_BG: tuple[int, int, int] = (20, 20, 25)

KARMA_START: float = 0.0
KARMA_MIN: float = -1000.0
KARMA_MAX: float = 1000.0

ENERGY_START = 100
RAW_MATERIAL_START = 2000

BASE_HEALTH: int = 1000

# durée du jour et de la nuit en ms (1 min chacun)
DAY_DURATION: float = 60000.0
NIGHT_DURATION: float = 60000.0

# -ennemis/difficulté-
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

# -bâtiments-
# tourelle : défense active, payée en Énergie
TURRET_HEALTH: int = 100
TURRET_COST: int = 100  # Énergie
TURRET_ATTACK_RANGE: float = 350.0
TURRET_ATTACK_DAMAGE: int = 30
TURRET_ATTACK_INTERVAL: float = 600.0  # ms entre deux tirs

# centrale à charbon : production continue (jour+nuit) mais baisse le karma
COAL_PLANT_HEALTH: int = 200
COAL_PLANT_COST: int = 300  # Matière première
COAL_PLANT_PRODUCTION_AMOUNT: int = 10  # Énergie par tick -> 5 Énergie/s
COAL_PLANT_PRODUCTION_INTERVAL: float = 2000.0  # ms entre deux ticks

# panneau solaire : production plus faible et limitée au jour mais augmente le karma
SOLAR_PANEL_HEALTH: int = 150
SOLAR_PANEL_COST: int = 300  # Matière première
SOLAR_PANEL_PRODUCTION_AMOUNT: int = 6  # Énergie par tick -> 3 Énergie/s
SOLAR_PANEL_PRODUCTION_INTERVAL: float = 2000.0  # ms entre deux ticks

# -ennemis-
# coureur : rapide et fragile, dégâts faibles
RUNNER_HEALTH: int = 60
RUNNER_SPEED: float = 40 / 1000  # pixels par ms
RUNNER_ATTACK_DAMAGE: int = 40
RUNNER_ATTACK_INTERVAL: float = 1000.0

# rôdeur : standard, équilibré entre vie et dégâts
PROWLER_HEALTH: int = 220
PROWLER_SPEED: float = 24 / 1000
PROWLER_ATTACK_DAMAGE: int = 90
PROWLER_ATTACK_INTERVAL: float = 1000.0

# centipède : lent mais résistant et inflige beaucoup de dégats
ARMORED_UNIT_HEALTH: int = 500
ARMORED_UNIT_SPEED: float = 10 / 1000
ARMORED_UNIT_ATTACK_DAMAGE: int = 160
ARMORED_UNIT_ATTACK_INTERVAL: float = 1000.0

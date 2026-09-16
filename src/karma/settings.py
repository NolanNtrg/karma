from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

ASSETS_DIR: Path = BASE_DIR / "assets"
MAPS_DIR: Path = ASSETS_DIR / "maps"
SPRITES_DIR: Path = ASSETS_DIR / "sprites"
SOUNDS_DIR: Path = ASSETS_DIR / "sounds"

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

# Délai en millisecondes entre deux apparitions d'ennemis pendant la nuit
ENEMY_SPAWN_INTERVAL: float = 1500.0

# Taux de karma fixe (par minute) appliqué à tout bâtiment propre/sale
KARMA_RATE_CLEAN: float = 100.0
KARMA_RATE_DIRTY: float = -100.0

# Distance (en pixels, espace monde) à laquelle un slot de construction devient interactif
BUILD_INTERACTION_RANGE: float = 48.0

# Producteurs d'énergie
SOLAR_PANEL_COST: int = 70
SOLAR_PANEL_HEALTH: int = 250
SOLAR_PANEL_PRODUCTION_AMOUNT: int = 15
SOLAR_PANEL_PRODUCTION_INTERVAL: float = 1000.0

COAL_PLANT_COST: int = 60
COAL_PLANT_HEALTH: int = 600
COAL_PLANT_PRODUCTION_AMOUNT: int = 35
COAL_PLANT_PRODUCTION_INTERVAL: float = 1000.0

# Amélioration "rapide" : achat unique, pas de consommation continue ensuite
SOLAR_UPGRADE_ENERGY_COST: int = 250
SOLAR_UPGRADE_RAW_MATERIAL_COST: int = 20
SOLAR_UPGRADE_PRODUCTION_AMOUNT: int = 150
SOLAR_UPGRADE_PRODUCTION_INTERVAL: float = 4000.0

COAL_UPGRADE_ENERGY_COST: int = 300
COAL_UPGRADE_RAW_MATERIAL_COST: int = 20
COAL_UPGRADE_PRODUCTION_AMOUNT: int = 220
COAL_UPGRADE_PRODUCTION_INTERVAL: float = 2000.0

# Défenses
WALL_COST: int = 40
WALL_HEALTH: int = 800

TURRET_COST: int = 200
TURRET_HEALTH: int = 350
TURRET_DAMAGE: int = 90
TURRET_ATTACK_INTERVAL: float = 700.0
TURRET_RANGE: float = 150.0

from enum import Enum, auto

class ResolutionType(Enum):
    Base = auto()
    Fullscreen = auto()

class VolumeAction(Enum):
    Cycle = auto()

class RessourceType(Enum):
    Energy = auto()
    RawMaterial = auto()
    Karma = auto()

class StateType(Enum):
    Menu = auto()
    Play = auto()
    Pause = auto()
    Credits = auto()
    Quit = auto()
    Cinematic = auto()
    GameOver = auto()
    BadEnding = auto()
    GoodEnding = auto()
    HowToPlay = auto()
class BuildingType(Enum):
    Turret = auto()
    CoalPlant = auto()
    SolarPanel = auto()
    Wall = auto()
    Plantation = auto()
    Driller = auto()

class MusicType(Enum):
    Menu =  auto()
    Night =  auto()
    Day =  auto()

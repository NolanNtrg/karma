from enum import Enum, auto

class ResolutionType(Enum):
    Base = auto()
    Fullscreen = auto()

class RessourceType(Enum):
    Energy = auto()
    RawMaterial = auto()
    Karma = auto()

class StateType(Enum):
    Menu = auto()
    Play = auto()
    Pause = auto()
    Quit = auto()
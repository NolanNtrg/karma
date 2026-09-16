import sys
import pygame

from karma.scenes.scenes import Scene
from karma.enums import ResolutionType, StateType
from karma.entities.buildings.base import Base
from karma.entities.player.player import Player
from karma.environment.camera import Camera
from karma.environment.map import MapManager
from karma.interface.buildMenu import BuildMenu
from karma.interface.menu import MainMenu, PauseMenu
from karma.interface.hud import HUD
from karma.resources.ressourceManager import RessourceManager
from karma.systems import BuildingSystem, CombatSystem, CycleSystem
from karma.settings import (
    ASSETS_DIR,
    BASE_HEALTH,
    BUILD_INTERACTION_RANGE,
    CAMERA_ZOOM,
    ENEMY_SPAWN_INTERVAL,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    SOUNDS_DIR
)

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running: bool = True
        self.state: StateType = StateType.Menu  # États possibles : "MENU", "PLAY", "PAUSE"
        self.resolution: ResolutionType = ResolutionType.Base # États possibles : "BASE", "FULLSCREEN"

        self.player = Player(name="Blanchon", position=pygame.Vector2(100, 100), speed=0.3)
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()

        # gestion de la map
        self.dayMap = MapManager(ASSETS_DIR / "dayMap.tmx")
        self.nightMap = MapManager(ASSETS_DIR / "nightMap.tmx")
        v_slot = self.dayMap.get_vaisseau_slot()
        v_pos = pygame.Vector2(v_slot.x, v_slot.y)
        self.player.position = pygame.Vector2(v_slot.x + 16, v_slot.y + 80)
        self.base = Base(position=v_pos, health=BASE_HEALTH)

        self.currentMap = self.dayMap  # Commence avec la carte de jour

        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, CAMERA_ZOOM, self.currentMap.width, self.currentMap.height)
        # Surface de jeu utilisée avant l'agrandissement à l'écran.
        self.game_surface = pygame.Surface((round(self.camera.width), round(self.camera.height)))

        self.resource_manager = RessourceManager()
        # Les slots sont identiques sur les deux maps, dayMap suffit
        self.building_system = BuildingSystem(self.dayMap)

        # Systèmes
        self.combat_system = CombatSystem(self.currentMap.width, self.currentMap.height, ENEMY_SPAWN_INTERVAL)
        self.cycle_system = CycleSystem(dayDuration=4000.0, nightDuration=4000.0)

        self.hud = HUD()
        self.build_menu = BuildMenu()

        pygame.mixer.music.load(SOUNDS_DIR / "Menu-Music.mp3")
        pygame.mixer.music.play()

    def handle_events(self) -> None:
        # Gestion des entrées utilisateur
        for event in pygame.event.get():
            if self.state == StateType.Menu:
                self.menu_handle_events(event)
            elif self.state == StateType.Play:
                self.play_handle_events(event)
            elif self.state == StateType.Pause:
                self.pause_handle_events(event)
            elif event.type == pygame.QUIT:
                self.running = False

    def menu_handle_events(self, event: pygame.event.Event) -> None:
        action = self.main_menu.handle_event(event)
        if action == ResolutionType.Fullscreen or action == ResolutionType.Base:
            self.resolution = action
            pygame.display.toggle_fullscreen()
        elif action == StateType.Play:
             self.state = StateType.Play
        elif action == StateType.Quit:
             self.running = False

    def play_handle_events(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            if self.building_system.isMenuOpen():
                self.building_system.closeMenu()
            else:
                self.state = StateType.Pause
            return

        if event.key == pygame.K_e:
            self.building_system.interact(self.player.getCenter(), BUILD_INTERACTION_RANGE, self.resource_manager, self.base.rect)
            return

        if self.building_system.isMenuOpen() and pygame.K_1 <= event.key <= pygame.K_9:
            key = event.key - pygame.K_1 + 1
            self.building_system.build(key, self.resource_manager)

    def pause_handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = StateType.Play
        else:
            action = self.pause_menu.handle_event(event)
            if action == ResolutionType.Fullscreen or action == ResolutionType.Base:
                self.resolution = action
                pygame.display.toggle_fullscreen()
            elif action == StateType.Quit:
                self.running = False
            elif action == StateType.Play or action == StateType.Menu:
                self.state = action

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS)
            self.handle_events()
            Scene.updateScenes(self, dt)
            Scene.drawScenes(self)

        pygame.quit()
        sys.exit()
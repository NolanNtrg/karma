import sys
import pygame

from karma.scenes.scenes import Scene
from karma.enums import ResolutionType, StateType, BuildingType, VolumeAction
from karma.entities.buildings.base import Base
from karma.entities.buildings.building import Building
from karma.entities.buildings.wall import Wall
from karma.entities.player.player import Player
from karma.environment.camera import Camera
from karma.environment.map import MapManager
from karma.interface.menu import MainMenu, PauseMenu, CreditsMenu
from karma.interface.hud import HUD
from karma.interface.cinematic import CinematicAction, CinematicPlayer
from karma.systems import CheatSystem, CombatSystem, CycleSystem
from karma.systems.buildings import BuildingsSystem
from karma.systems.resourceManager import RessourceManager
from karma.interface.buildingMenu import BuildingMenu
from karma.settings import (
    ASSETS_DIR,
    BASE_HEALTH,
    CAMERA_ZOOM,
    DEFAULT_VOLUME,
    ENEMY_SPAWN_INTERVAL,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    SOUNDS_DIR,
    VIDEO_DIR,
)

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running: bool = True
        self.state: StateType = StateType.Menu  # États possibles : "MENU", "PLAY", "PAUSE", "CINEMATIC"
        self.resolution: ResolutionType = ResolutionType.Base # États possibles : "BASE", "FULLSCREEN"
        self.volume: float = DEFAULT_VOLUME
        pygame.mixer.music.set_volume(self.volume)
        self.cinematic_player: CinematicPlayer | None = None
        self.cinematic_return_state: StateType = StateType.Menu
        self.paused_from_cinematic: bool = False
        self.game_over: bool = False
        self.final_karma: float | None = None

        self.player = Player(name="Blanchon", position=pygame.Vector2(100, 100), speed=0.3)
        self.main_menu = MainMenu(self.volume)
        self.pause_menu = PauseMenu(self.volume)
        self.credits_menu = CreditsMenu()

        # gestion de la map
        self.dayMap = MapManager(ASSETS_DIR / "dayMap.tmx")
        self.nightMap = MapManager(ASSETS_DIR / "nightMap.tmx")
        v_slot = self.dayMap.get_vaisseau_slot()
        v_pos = pygame.Vector2(v_slot.x, v_slot.y)
        self.player.position = pygame.Vector2(v_slot.x + 16, v_slot.y + 80)
        self.base = Base(position=v_pos, health=BASE_HEALTH)

        self.currentMap = self.dayMap  # Commence avec la carte de jour

        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, CAMERA_ZOOM, self.currentMap.width, self.currentMap.height)
        # la caméra suit le joueur
        self.camera.update(self.player.getCenter())
        # Surface de jeu utilisée avant l'agrandissement à l'écran.
        self.game_surface = pygame.Surface((round(self.camera.width), round(self.camera.height)))

        # self.buildings sera rempli par le futur système de construction/placement
        self.buildings: list[Building] = []
        self.walls: list[Wall] = []

        # Systèmes
        self.combat_system = CombatSystem(self.currentMap.width, self.currentMap.height, ENEMY_SPAWN_INTERVAL)
        self.cycle_system = CycleSystem(dayDuration=8000.0, nightDuration=8000.0)
        self.building_system = BuildingsSystem()

        self.hud = HUD()
        self.building_menu = BuildingMenu()
        self.rm = RessourceManager()  # Le gestionnaire de ressources
        self.cheat_system = CheatSystem(self.base, self.cycle_system, self.combat_system, self.rm)

    def handle_events(self) -> None:
        # Gestion des entrées utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == StateType.Menu:
                self.menu_handle_events(event)
            elif self.state == StateType.Play:
                self.play_handle_events(event)
            elif self.state == StateType.Pause:
                self.pause_handle_events(event)
            elif self.state == StateType.Credits:
                self.credits_handle_events(event)
                
            
            elif event.type == pygame.QUIT:
                self.running = False
            elif self.state == StateType.Cinematic:
                self.cinematic_handle_events(event)

    def cycle_volume(self) -> None:
        levels = [1.0, 0.75, 0.5, 0.25, 0.0]
        current = round(self.volume, 2)
        try:
            idx = levels.index(current)
            next_idx = (idx + 1) % len(levels)
        except ValueError:
            next_idx = 0
        self.volume = levels[next_idx]
        pygame.mixer.music.set_volume(self.volume)
        self.main_menu.update_volume_text(self.volume)
        self.pause_menu.update_volume_text(self.volume)

    def menu_handle_events(self, event: pygame.event.Event) -> None:
        action = self.main_menu.handle_event(event)
        if action == StateType.Quit:
            self.running = False
        elif action == VolumeAction.Cycle:
            self.cycle_volume()
        elif action == ResolutionType.Fullscreen or action == ResolutionType.Base:
            self.resolution = action
            pygame.display.toggle_fullscreen()
        elif action == StateType.Play:
            self.state = action
            self.start_cinematic(VIDEO_DIR / "Vidéo Intro", StateType.Play)
            pygame.mixer.music.load(SOUNDS_DIR / "Menu-Music.mp3")
            pygame.mixer.music.play(-1)
        elif action == StateType.Credits:
            self.state = action
        elif action == StateType.Quit:
            self.running = False

    def play_handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = StateType.Pause
            elif event.key == pygame.K_3:  # Appuyer sur 3 pour construire une tourelle 
                new_building = self.building_system.build(BuildingType.Turret, self.rm, amount=100)
                if new_building:
                    self.buildings.append(new_building)
            elif event.key == pygame.K_1:  # Appuyer sur 1 pour construire une centrale a charbon  
                new_building = self.building_system.build(BuildingType.CoalPlant, self.rm, amount=300)
                if new_building:
                    self.buildings.append(new_building)
            elif event.key == pygame.K_2:  # Appuyer sur 2 pour construire un panneau solaire
                new_building = self.building_system.build(BuildingType.SolarPanel, self.rm, amount=300)
                if new_building:
                    self.buildings.append(new_building)
            else:
                self.cheat_system.handleKey(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # position de la souris convertit en coord
            self.player.shoot(self.camera.screenToWorld(pygame.Vector2(event.pos)))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused_from_cinematic = False
            self.state = StateType.Pause

    def pause_handle_events(self, event: pygame.event.Event) -> None:
        if self.paused_from_cinematic:
            self.cinematic_pause_handle_events(event)
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = StateType.Play
        else:
            action = self.pause_menu.handle_event(event)
            if action == ResolutionType.Fullscreen or action == ResolutionType.Base:
                self.resolution = action
                pygame.display.toggle_fullscreen()
            elif action == VolumeAction.Cycle:
                self.cycle_volume()
            elif action == StateType.Quit:
                self.running = False
            elif action == StateType.Play or action == StateType.Menu:
                self.state = action

    def credits_handle_events(self, event: pygame.event.Event) -> None:
        action = self.credits_menu.handle_event(event)
        if action == StateType.Menu:
            self.state = action

    def start_cinematic(self, directory, return_state: StateType) -> None:
        self.cinematic_player = CinematicPlayer(
            directory,
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            fps=10.0,
        )
        self.cinematic_return_state = return_state
        self.paused_from_cinematic = False
        self.state = StateType.Cinematic

    def update_cinematic(self, dt: float) -> None:
        if self.cinematic_player is not None and self.cinematic_player.update(dt):
            self.finish_cinematic()

    def cinematic_handle_events(self, event: pygame.event.Event) -> None:
        action = self.cinematic_player.handle_event(event)
        if action == CinematicAction.Skip:
            self.finish_cinematic()
        elif action == CinematicAction.Pause:
            self.paused_from_cinematic = True
            self.state = StateType.Pause

    def cinematic_pause_handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused_from_cinematic = False
            self.state = StateType.Cinematic
            self.cinematic_player.resume()
            return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        action = self.pause_menu.handle_event(event)
        if action == ResolutionType.Fullscreen or action == ResolutionType.Base:
            self.resolution = action
            pygame.display.toggle_fullscreen()
        elif action == VolumeAction.Cycle:
            self.cycle_volume()
        elif action == StateType.Play:
            self.paused_from_cinematic = False
            self.state = StateType.Cinematic
            self.cinematic_player.resume()
        elif action == StateType.Menu:
            self.finish_cinematic()
            self.state = StateType.Menu
        elif action == StateType.Quit:
            self.running = False

    def finish_cinematic(self) -> None:
        self.cinematic_player = None
        self.paused_from_cinematic = False
        self.state = self.cinematic_return_state

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS)
            self.handle_events()
            Scene.updateScenes(self, dt)
            Scene.drawScenes(self)

        pygame.quit()
        sys.exit()
import sys
import pygame

from karma.scenes.scenes import Scene
from karma.enums import ResolutionType, StateType, BuildingType
from karma.entities.buildings.base import Base
from karma.entities.buildings.building import Building
from karma.entities.buildings.wall import Wall
from karma.entities.player.player import Player
from karma.environment.camera import Camera
from karma.environment.map import MapManager
from karma.interface.menu import MainMenu, PauseMenu, CreditsMenu, GameOverMenu
from karma.enums import RessourceType
from karma.interface.hud import HUD
from karma.interface.cinematic import CinematicAction, CinematicPlayer
from karma.interface.explosion import ExplosionAnimation
from karma.systems import CombatSystem, CycleSystem
from karma.systems.buildings import BuildingsSystem
from karma.resources.ressourceManager import RessourceManager
from karma.interface.buildingMenu import BuildingMenu
from karma.settings import (
    ASSETS_DIR,
    BASE_HEALTH,
    CAMERA_ZOOM,
    ENEMY_SPAWN_INTERVAL,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    SOUNDS_DIR,
    VIDEO_DIR,
    ENERGY_START,
    RAW_MATERIAL_START,
    KARMA_START,
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
        self.cinematic_player: CinematicPlayer | None = None
        self.explosion: ExplosionAnimation | None = None
        self.cinematic_return_state: StateType = StateType.Menu
        self.paused_from_cinematic: bool = False
        self.paused_from_explosion: bool = False

        self.player = Player(name="Blanchon", position=pygame.Vector2(100, 100), speed=0.3)
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        self.credits_menu = CreditsMenu()
        self.game_over_menu = GameOverMenu()

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
        self.cycle_system = CycleSystem(dayDuration=8000.0, nightDuration=32000.0)
        self.building_system = BuildingsSystem()

        self.hud = HUD()
        self.building_menu = BuildingMenu()
        self.rm = RessourceManager()  # Le gestionnaire de ressources

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
            elif self.state == StateType.GameOver:
                self.game_over_handle_events(event)
            elif self.state == StateType.Cinematic:
                self.cinematic_handle_events(event)

    def menu_handle_events(self, event: pygame.event.Event) -> None:
        action = self.main_menu.handle_event(event)
        if action == StateType.Quit:
            self.running = False
        if action == ResolutionType.Fullscreen or action == ResolutionType.Base:
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
        if self.paused_from_explosion:
            return

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

    def credits_handle_events(self, event: pygame.event.Event) -> None:
        action = self.credits_menu.handle_event(event)
        if action == StateType.Menu:
            self.state = action

    def game_over_handle_events(self, event: pygame.event.Event) -> None:
        action = self.game_over_menu.handle_event(event)
        if action == StateType.Play:
            self.reset_game()
            self.start_cinematic(VIDEO_DIR / "Vidéo Intro", StateType.Play)
            pygame.mixer.music.load(SOUNDS_DIR / "Menu-Music.mp3")
            pygame.mixer.music.play(-1)
        elif action == StateType.Quit:
            self.running = False

    def reset_game(self) -> None:
        v_slot = self.dayMap.get_vaisseau_slot()
        v_pos = pygame.Vector2(v_slot.x, v_slot.y)
        self.player.position = pygame.Vector2(v_slot.x + 16, v_slot.y + 80)
        self.player.health = self.player.max_health
        self.player.timeSinceLastAttack = self.player.ATTACK_INTERVAL
        self.player.muzzleFlashTimer = 0.0
        self.player.shooter.bullets.clear()
        self.base = Base(position=v_pos, health=BASE_HEALTH)
        self.currentMap = self.dayMap
        self.buildings.clear()
        self.walls.clear()
        self.combat_system.enemies.clear()
        self.combat_system.enemySpawner.timeSinceLastSpawn = 0.0
        self.cycle_system.isDay = True
        self.cycle_system.cycleTimer = 0.0
        self.cycle_system.currentDay = 1
        self.building_system.currentSlot = None
        self.building_system.dictOccupedSlot.clear()
        self.rm.stocks.update({
            RessourceType.Energy: ENERGY_START,
            RessourceType.RawMaterial: RAW_MATERIAL_START,
            RessourceType.Karma: KARMA_START,
        })
        self.paused_from_cinematic = False
        self.paused_from_explosion = False
        self.cinematic_player = None

    def start_bad_ending(self) -> None:
        pygame.mixer.music.stop()
        self.building_menu.isVisible = False
        self.start_cinematic(VIDEO_DIR / "Vidéo Fin Eclipse", StateType.GameOver)

    def start_explosion(self) -> None:
        self.explosion = ExplosionAnimation(
            ASSETS_DIR / "Effects" / "big-explosion.png",
            self.base.position,
        )
        self.paused_from_explosion = True
        self.state = StateType.Pause

    def update_explosion(self, dt: float) -> None:
        if self.explosion is not None and self.explosion.update(dt):
            self.explosion = None
            self.paused_from_explosion = False
            self.start_bad_ending()

    def start_cinematic(self, directory, return_state: StateType) -> None:
        self.cinematic_player = CinematicPlayer(
            directory,
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            fps=10.0,
        )
        self.cinematic_return_state = return_state
        self.paused_from_cinematic = False
        self.paused_from_explosion = False
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
        self.explosion = None
        self.paused_from_cinematic = False
        self.paused_from_explosion = False
        self.state = self.cinematic_return_state

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS)
            self.handle_events()
            Scene.updateScenes(self, dt)
            Scene.drawScenes(self)

        pygame.quit()
        sys.exit()
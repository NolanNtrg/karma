import sys
from pathlib import Path

import pygame

from karma.scenes.scenes import Scene
from karma.systems.scoreManager import ScoreManager
from karma.enums import ResolutionType, StateType, BuildingType, VolumeAction
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
from karma.systems.buildings import BuildingsSystem
from karma.systems.resourceManager import RessourceManager
from karma.systems.cheats import CheatSystem
from karma.systems.cycle import CycleSystem
from karma.systems.combat import CombatSystem
from karma.interface.buildingMenu import BuildingMenu
from karma.settings import (
    ASSETS_DIR,
    BASE_HEALTH,
    CAMERA_ZOOM,
    DAY_DURATION,
    DEFAULT_VOLUME,
    ENEMY_SPAWN_INTERVAL,
    FPS,
    NIGHT_DURATION,
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

    # variables globales 
    lobotomy_sound = None
    explosion_sound = None

    def __init__(self) -> None:
        # Initialisation de Pygame et de la fenêtre du jeu
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
        self.next_cinematic_player: CinematicPlayer | None = None
        self.explosion: ExplosionAnimation | None = None
        self.cinematic_return_state: StateType = StateType.Menu
        self.paused_from_cinematic: bool = False
        self.paused_from_explosion: bool = False

       # Initialisation des composants du jeu
        self.player = Player(name="Blanchon", position=pygame.Vector2(100, 100), speed=0.3)
        self.main_menu = MainMenu(self.volume)
        self.pause_menu = PauseMenu(self.volume)
        self.credits_menu = CreditsMenu()
        self.game_over_menu = GameOverMenu()
        self.how_to_play_index: int = 0
        self.how_to_play_return_state: StateType = StateType.Menu 

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
        self.cycle_system = CycleSystem(dayDuration=DAY_DURATION, nightDuration=NIGHT_DURATION)
        self.building_system = BuildingsSystem()

        self.hud = HUD()
        self.building_menu = BuildingMenu()
        self.rm = RessourceManager()  # Le gestionnaire de ressources
        self.cheat_system = CheatSystem(self.base, self.cycle_system, self.combat_system, self.rm)

        if Game.lobotomy_sound is None:
            Game.lobotomy_sound = pygame.mixer.Sound(SOUNDS_DIR / "LOBOTOMY.mp3")
        if Game.explosion_sound is None:
            Game.explosion_sound = pygame.mixer.Sound(SOUNDS_DIR / "explosion.mp3")

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
            elif self.state == StateType.HowToPlay:
                self.how_to_play_handle_events(event)
            elif self.state in (StateType.BadEnding, StateType.MidEnding, StateType.GoodEnding):
                self.game_over_handle_events(event)
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
        elif action == StateType.Credits:
            self.state = action
        elif action == StateType.HowToPlay:
            self.how_to_play_index = 0
            self.how_to_play_return_state = StateType.Menu
            self.state = action
        elif action == StateType.Quit:
            self.running = False

    def play_handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = StateType.Pause
            elif event.key == pygame.K_1:
                new_building = self.building_system.build(BuildingType.Driller, self.rm)
                if new_building:
                    self.buildings.append(new_building)
            elif event.key == pygame.K_2:
                new_building = self.building_system.build(BuildingType.Plantation, self.rm)
                if new_building:
                    self.buildings.append(new_building)
            elif event.key == pygame.K_5: 
                new_building = self.building_system.build(BuildingType.Turret, self.rm)
                if new_building:
                    self.buildings.append(new_building)
            elif event.key == pygame.K_4: 
                new_building = self.building_system.build(BuildingType.CoalPlant, self.rm)
                if new_building:
                    self.buildings.append(new_building)
            elif event.key == pygame.K_3:
                new_building = self.building_system.build(BuildingType.SolarPanel, self.rm)
                if new_building:
                    self.buildings.append(new_building)
            elif event.key == pygame.K_6: 
                Game.lobotomy_sound.play()
            else:
                self.cheat_system.handleKey(event.key)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.paused_from_cinematic = False
            self.state = StateType.Pause
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            world_position = self.camera.screenToWorld(pygame.Vector2(event.pos))
            forbidden_rects = [self.base.rect] + [slot["rect"] for slot in self.currentMap.get_build_slots()]
            new_wall = self.building_system.buildWallAt(world_position, self.rm, forbidden_rects)
            if new_wall:
                self.walls.append(new_wall)

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
            elif action == VolumeAction.Cycle:
                self.cycle_volume()
            elif action == StateType.HowToPlay:                     # <-- AJOUTER CES 4 LIGNES
                self.how_to_play_index = 0
                self.how_to_play_return_state = StateType.Pause
                self.state = action
            elif action == StateType.Quit:
                self.running = False
            elif action == StateType.Play or action == StateType.Menu:
                self.state = action

    def credits_handle_events(self, event: pygame.event.Event) -> None:
        action = self.credits_menu.handle_event(event)
        if action == StateType.Menu:
            self.state = action

    def how_to_play_handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = self.how_to_play_return_state
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.how_to_play_index == 0:
                self.how_to_play_index = 1
            else:
                self.state = self.how_to_play_return_state

    def game_over_handle_events(self, event: pygame.event.Event) -> None:
        action = self.game_over_menu.handle_event(event)
        if action == StateType.Play:
            self.reset_game()
            self.start_cinematic(VIDEO_DIR / "Vidéo Intro", StateType.Play)
        elif action == StateType.Quit:
            self.running = False

    def reset_game(self) -> None:
        ScoreManager.resetScore()
        v_slot = self.dayMap.get_vaisseau_slot()
        v_pos = pygame.Vector2(v_slot.x, v_slot.y)
        self.player.position = pygame.Vector2(v_slot.x + 16, v_slot.y + 80)
        self.player.health = self.player.max_health
        self.player.timeSinceLastAttack = self.player.ATTACK_INTERVAL
        self.player.muzzleFlashTimer = 0.0
        self.player.shooter.bullets.clear()
        self.base = Base(position=v_pos, health=BASE_HEALTH)
        self.cheat_system.base = self.base
        self.cheat_system.godmode = False
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
        self.building_system.occupiedWallCells.clear()
        self.rm.stocks.update({
            RessourceType.Energy: ENERGY_START,
            RessourceType.RawMaterial: RAW_MATERIAL_START,
            RessourceType.Karma: KARMA_START,
        })
        self.paused_from_cinematic = False
        self.paused_from_explosion = False
        self.cinematic_player = None
        self.next_cinematic_player = None

    def start_bad_ending(self) -> None:
        self.game_over_menu = GameOverMenu()
        pygame.mixer.music.stop()
        self.building_menu.isVisible = False
        self.start_cinematic(VIDEO_DIR / "Vidéo Bad Ending", StateType.BadEnding)
        self.state = StateType.BadEnding

    def start_good_ending(self) -> None:
        self.game_over_menu = GameOverMenu()
        pygame.mixer.music.stop()
        self.building_menu.isVisible = False
        self.start_cinematic(VIDEO_DIR / "Vidéo Fin Eclipse", StateType.GoodEnding)
        self.next_cinematic_player = CinematicPlayer(
            VIDEO_DIR / "Vidéo Good Ending",
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            fps=10.0,
        )
        self.state = StateType.GoodEnding

    def start_mid_ending(self) -> None:
        self.game_over_menu = GameOverMenu()
        pygame.mixer.music.stop()
        self.building_menu.isVisible = False
        self.start_cinematic(VIDEO_DIR / "Vidéo Mid Ending", StateType.MidEnding)
        self.state = StateType.MidEnding

    def start_explosion(self) -> None:
        self.explosion = ExplosionAnimation(
            ASSETS_DIR / "Effects" / "big-explosion.png",
            self.base.position,
        )
        Game.explosion_sound.play()
        self.paused_from_explosion = True
        self.state = StateType.Pause

    def update_explosion(self, dt: float) -> None:
        if self.explosion is not None and self.explosion.update(dt):
            self.explosion = None
            self.paused_from_explosion = False
            self.start_bad_ending()

    def start_cinematic(self, directory: Path, return_state: StateType) -> None:
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
            if self.next_cinematic_player is not None:
                self.cinematic_player = self.next_cinematic_player
                self.next_cinematic_player = None
                self.cinematic_player.resume()
            else:
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
        self.next_cinematic_player = None
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
import sys
import pygame

from karma.enums import ResolutionType, StateType
from karma.entities.buildings.base import Base
from karma.entities.buildings.building import Building
from karma.entities.buildings.wall import Wall
from karma.entities.enemies.enemy import Enemy
from karma.entities.enemies.spawner import EnemySpawner
from karma.entities.player.player import Player
from karma.environment.camera import Camera
from karma.environment.map import MapManager
from karma.interface.menu import MainMenu, PauseMenu
from karma.interface.hud import HUD
from karma.settings import (
    ASSETS_DIR,
    BASE_HEALTH,
    CAMERA_ZOOM,
    COLOR_BG,
    ENEMY_SPAWN_INTERVAL,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
)

class Game:
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

        # self.buildings sera rempli par le futur système de construction/placement
        self.buildings: list[Building] = []
        self.walls: list[Wall] = []

        # gestion des ennemis
        self.enemies: list[Enemy] = []
        self.enemySpawner = EnemySpawner(self.currentMap.width, self.currentMap.height, ENEMY_SPAWN_INTERVAL)

        self.hud = HUD()

        self.isDay = True
        self.dayDuration = 4000 # mettre 2 min dans le futur
        self.nightDuration = 4000 # pareil mais 1 min
        self.cycleTimer = 0.0
        self.currentDay = 1

    def handle_events(self) -> None:
        # Gestion des entrées utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == StateType.Menu:
                action = self.main_menu.handle_event(event)
                if action == StateType.Play:
                    self.state = StateType.Play
                elif action == StateType.Quit:
                    self.running = False

            elif self.state == StateType.Play:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = StateType.Pause

            elif self.state == StateType.Pause:
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
                    

    def update(self, dt: float) -> None:
        # Mise à jour de la physique et des entités (seulement quand on joue)
        if self.state == StateType.Play:
            self.player.update(dt)
            self.base.update(dt, self.isDay)
            self.camera.update(self.player.getCenter())

            newEnemy = self.enemySpawner.trySpawn(dt, not self.isDay, self.base.position)
            if newEnemy is not None:
                self.enemies.append(newEnemy)

            for enemy in self.enemies:
                enemy.update(dt, self.walls, self.base)
            self.enemies = [enemy for enemy in self.enemies if not enemy.isDestroyed()]

            self.cycleTimer += dt
            if self.isDay and self.cycleTimer >= self.dayDuration:
                self.isDay = False
                self.currentMap = self.nightMap
                self.cycleTimer = 0.0   
            elif not self.isDay and self.cycleTimer >= self.nightDuration:
                self.isDay = True
                self.currentMap = self.dayMap
                self.cycleTimer = 0.0
                self.currentDay += 1 # on passe au jour suivant

    def draw(self) -> None:
        # Rendu graphique

        if self.state == StateType.Menu:
            self.screen.fill(COLOR_BG)
            self.main_menu.draw(self.screen)
        else:
            # En PLAY ou en PAUSE, le jeu reste visible en arrière-plan.
            # On dessine la carte du cycle jour/nuit courante sur la surface
            # zoomée, puis on l'étire vers l'écran.
            self.game_surface.fill(COLOR_BG)
            self.currentMap.render(self.game_surface, self.camera)
            self.base.draw(self.game_surface, self.camera)
            for enemy in self.enemies:
                enemy.draw(self.game_surface, self.camera)
            self.player.draw(self.game_surface, self.camera)
            pygame.transform.scale(self.game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT), self.screen)

            duration = self.dayDuration if self.isDay else self.nightDuration
            self.hud.draw(self.screen, self.currentDay, self.isDay, self.cycleTimer, duration)

            if self.state == StateType.Pause:
                self.pause_menu.draw(self.screen)

        pygame.display.flip()

    def run(self) -> None:
        while self.running:
            self.handle_events()
            dt = self.clock.tick(FPS)

            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()
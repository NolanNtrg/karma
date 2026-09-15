import sys
import pygame

from karma.entities.buildings.base import Base
from karma.entities.buildings.building import Building
from karma.entities.buildings.wall import Wall
from karma.entities.enemies.enemy import Enemy
from karma.entities.enemies.spawner import EnemySpawner
from karma.entities.player.player import Player
from karma.environment.camera import Camera
from karma.environment.map import MapManager
from karma.interface.menu import MainMenu, PauseMenu
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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running: bool = True
        self.state: str = "MENU"  # États possibles : "MENU", "PLAY", "PAUSE"

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

        self.isDay = True
        self.dayDuration = 4000 # mettre 2 min dans le futur
        self.nightDuration = 4000 # pareil mais 1 min
        self.cycleTimer = 0.0

        self.sunImg =  pygame.transform.scale_by(pygame.image.load(ASSETS_DIR / "soleil.png").convert_alpha(), 3)
        self.moonImg = pygame.transform.scale_by(pygame.image.load(ASSETS_DIR / "eclipseTotale.png").convert_alpha(), 3)

    def handle_events(self) -> None:
        # Gestion des entrées utilisateur
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if self.state == "MENU":
                action = self.main_menu.handle_event(event)
                if action == "PLAY":
                    self.state = "PLAY"
                elif action == "QUIT":
                    self.running = False

            elif self.state == "PLAY":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "PAUSE"

            elif self.state == "PAUSE":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "PLAY"
                else:
                    action = self.pause_menu.handle_event(event)
                    if action == "RESUME":
                        self.state = "PLAY"
                    elif action == "MENU":
                        self.state = "MENU"
                    elif action == "QUIT":
                        self.running = False

    def update(self, dt: float) -> None:
        # Mise à jour de la physique et des entités (seulement quand on joue)
        if self.state == "PLAY":
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

    def draw(self) -> None:
        # Rendu graphique
        self.screen.fill(COLOR_BG)

        if self.state == "MENU":
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

            icon = self.sunImg if self.isDay else self.moonImg
            self.screen.blit(icon, (20,20))

            if self.state == "PAUSE":
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
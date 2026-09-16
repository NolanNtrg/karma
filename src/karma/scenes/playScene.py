import pygame

from karma.enums import StateType
from karma.settings import ASSETS_DIR, COLOR_BG, SCREEN_HEIGHT, SCREEN_WIDTH, SOUNDS_DIR
from karma.entities.buildings.turret import Turret

class PlayScene:

    def updatePlayScene(self, dt: float) -> None:
        if self.state != StateType.Play:
            return
        self.player.update(dt, self.combat_system.enemies, self.camera)
        self.base.update(dt, self.cycle_system.isDay)
        self.camera.update(self.player.getCenter())

        self.combat_system.update(dt, self.cycle_system.isDay, self.base, self.walls)

        for building in self.buildings : 
            if isinstance(building, Turret):
                building.update(dt, self.combat_system.enemies, self.cycle_system.isDay)

        build_slots = self.currentMap.get_build_slots()
        self.building_system.update(self.player, build_slots)

        if self.cycle_system.update(dt):
            self.currentMap = self.dayMap if self.cycle_system.isDay else self.nightMap
            if self.cycle_system.isDay:
                self.combat_system.enemies.clear()
                pygame.mixer.music.load(SOUNDS_DIR / "Menu-Music.mp3")
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.load(SOUNDS_DIR / "BadAtmosphere.wav")
                pygame.mixer.music.play(-1)

    def drawPlayScene(self) -> None:
        self.game_surface.fill(COLOR_BG)
        self.currentMap.render(self.game_surface, self.camera)
        self.base.draw(self.game_surface, self.camera)

        for building in self.buildings:
                building.draw(self.game_surface, self.camera)
                
        self.combat_system.draw(self.game_surface, self.camera)
        self.player.draw(self.game_surface, self.camera)
        pygame.transform.scale(self.game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT), self.screen)

        self.hud.draw(
            self.screen,
            self.cycle_system.currentDay,
            self.cycle_system.isDay,
            self.cycle_system.cycleTimer,
            self.cycle_system.currentDuration(),
            self.base.health,
            self.base.max_health,
        )

        if self.state == StateType.Pause:
            self.pause_menu.draw(self.screen)
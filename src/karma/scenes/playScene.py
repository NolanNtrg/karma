import pygame

from karma.enums import StateType
from karma.settings import ASSETS_DIR, BUILD_INTERACTION_RANGE, SCREEN_HEIGHT, SCREEN_WIDTH

class PlayScene():

    def updatePlayScene(self, dt: float):
        if self.state != StateType.Play:
            return
        self.player.update(dt)
        self.base.update(dt, self.cycle_system.isDay)
        self.camera.update(self.player.getCenter())

        self.combat_system.update(dt, self.cycle_system.isDay, self.base, self.building_system.getWalls())
        self.building_system.update(dt, self.cycle_system.isDay, self.resource_manager, self.combat_system.enemies)
        self.building_system.closeMenuIfOutOfRange(self.player.getCenter(), BUILD_INTERACTION_RANGE)

        if self.cycle_system.update(dt):
            self.currentMap = self.dayMap if self.cycle_system.isDay else self.nightMap


    def drawPlayScene(self) -> None:
        self.currentMap.render(self.game_surface, self.camera)
        self.base.draw(self.game_surface, self.camera)
        self.building_system.draw(self.game_surface, self.camera)
        self.combat_system.draw(self.game_surface, self.camera)
        self.player.draw(self.game_surface, self.camera)
        self.build_menu.drawWorld(self.game_surface, self.camera, self.building_system, self.player.getCenter(), BUILD_INTERACTION_RANGE)
        pygame.transform.scale(self.game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT), self.screen)

        self.hud.draw(
            self.screen,
            self.cycle_system.currentDay,
            self.cycle_system.isDay,
            self.cycle_system.cycleTimer,
            self.cycle_system.currentDuration(),
            self.resource_manager,
        )
        self.build_menu.drawPanel(self.screen, self.building_system, self.resource_manager)

        if self.state == StateType.Pause:
            self.pause_menu.draw(self.screen)
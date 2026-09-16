import pygame

from karma.enums import StateType
from karma.settings import ASSETS_DIR, SCREEN_HEIGHT, SCREEN_WIDTH

class PlayScene():

    def updatePlayScene(self, dt: float):
        if self.state != StateType.Play:
            return
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
        
    def drawPlayScene(self) -> None:
        # En PLAY ou en PAUSE, le jeu reste visible en arrière-plan.
        # On dessine la carte du cycle jour/nuit courante sur la surface
        # zoomée, puis on l'étire vers l'écran.
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
import pygame

from karma.enums import RessourceType, StateType
from karma.entities.buildings.turret import Turret
from karma.settings import (ASSETS_DIR,COLOR_BG,SCREEN_HEIGHT,SCREEN_WIDTH,SOUNDS_DIR,VIDEO_DIR,)
from karma.entities.buildings.energy_producer import EnergyProducer
from karma.entities.buildings.solar_panel import SolarPanel

class PlayScene:

    def updatePlayScene(self, dt: float) -> None:
        if self.state != StateType.Play:
            return
        self.player.update(
            dt,
            self.combat_system.enemies,
            self.camera,
            (self.currentMap.width, self.currentMap.height),
        )
        self.base.update(dt, self.cycle_system.isDay)
        self.camera.update(self.player.getCenter())

        self.combat_system.update(dt, self.cycle_system.isDay, self.base, self.walls, self.cycle_system.currentDay)

        for building in self.buildings :
            if isinstance(building, Turret):
                building.update(dt, self.combat_system.enemies, self.camera, self.cycle_system.isDay)
            elif isinstance(building, EnergyProducer):
                building.update(dt, self.cycle_system.isDay)
                if isinstance(building, SolarPanel) and not self.cycle_system.isDay:
                    continue
                energy = building.tryProduce(dt)
                if energy > 0:
                    self.rm.add(RessourceType.Energy, energy)

        karmaDelta = sum(building.getKarmaImpact(dt) for building in self.buildings)
        self.rm.applyKarmaDelta(karmaDelta)

        if self.base.isDestroyed() and not self.game_over:
            self.game_over = True
            self.final_karma = self.rm.getStock(RessourceType.Karma)

        build_slots = self.currentMap.get_build_slots()
        self.building_system.update(self.player, build_slots)

        slot = self.building_system.currentSlot
        if slot is not None and self.building_system.isSlotFree(slot["id"]):
            self.building_menu.isVisible= True
        else:
            self.building_menu.isVisible = False
            
        if self.cycle_system.update(dt):
            self.currentMap = self.dayMap if self.cycle_system.isDay else self.nightMap
            if self.cycle_system.isDay:
                self.combat_system.enemies.clear()
                pygame.mixer.music.load(SOUNDS_DIR / "Menu-Music.mp3")
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.load(SOUNDS_DIR / "BadAtmosphere.wav")
                pygame.mixer.music.play(-1)

            cinematic_directory = (
                VIDEO_DIR / "Vidéo Fin Eclipse"
                if self.cycle_system.isDay
                else VIDEO_DIR / "Vidéo Début Eclipse"
            )
            self.start_cinematic(cinematic_directory, StateType.Play)

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

        self.building_menu.draw(self.screen)

        if self.state == StateType.Pause:
            self.pause_menu.draw(self.screen)
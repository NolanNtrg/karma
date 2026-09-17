import pygame

from karma.enums import StateType
from karma.entities.buildings.turret import Turret
from karma.settings import (ASSETS_DIR,BASE_NIGHT_HEAL,COLOR_BG,SCREEN_HEIGHT,SCREEN_WIDTH,SOUNDS_DIR,VIDEO_DIR,)
from karma.entities.buildings.ressourcesProducer import RessourcesProducer


class PlayScene:

    @staticmethod
    def updatePlayScene(self, dt: float) -> None:
        if self.state != StateType.Play:
            return
        self.player.update(
            dt,
            self.combat_system.enemies,
            self.camera,
            (self.dayMap.width, self.dayMap.height),
        )
        # si la souris est cliquée OU maintenu, on fait tirer le joueur vers la position de la souris
        if pygame.mouse.get_pressed()[0]:
            self.player.shoot(self.camera.screenToWorld(pygame.Vector2(pygame.mouse.get_pos())))
        self.base.update(dt, self.cycle_system.isDay)
        self.camera.update(self.player.getCenter())

        self.combat_system.update(dt, self.cycle_system.isDay, self.base, self.walls, self.buildings, self.cycle_system.currentDay)

        self.building_system.removeDestroyed(self.walls)

        # mise à jour des bâtiments, suppression de ceux détruits
        self.buildings = [building for building in self.buildings if not building.isDestroyed()]

        # mise à jour des murs
        self.walls = [wall for wall in self.walls if not wall.isDestroyed()]

        if self.base.isDestroyed():
            self.start_explosion()
            return

        for building in self.buildings:
            if isinstance(building, Turret):
                building.update(dt, self.combat_system.enemies, self.camera, self.cycle_system.isDay)
            elif isinstance(building, RessourcesProducer):
                building.update(dt, self.cycle_system.isDay)
                if building.requiresDaylight and not self.cycle_system.isDay:
                    continue
                produced = building.tryProduce(dt)
                if produced > 0:
                    self.rm.add(building.resourceType, produced)

        for wall in self.walls:
            wall.update(self.cycle_system.isDay)

        karmaDelta = sum(building.getKarmaImpact(dt) for building in self.buildings)
        self.rm.applyKarmaDelta(karmaDelta)

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
                self.base.heal(BASE_NIGHT_HEAL)
                if self.cycle_system.currentDay >= 4:
                    self.start_good_ending()
                    return
                pygame.mixer.music.load(SOUNDS_DIR / "DayMusic.mp3")
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.load(SOUNDS_DIR / "NightMusic.mp3")
                pygame.mixer.music.play(-1)

            cinematic_directory = (
                VIDEO_DIR / "Vidéo Fin Eclipse"
                if self.cycle_system.isDay
                else VIDEO_DIR / "Vidéo Début Eclipse"
            )
            self.start_cinematic(cinematic_directory, StateType.Play)

    def drawPlayScene(self) -> None:
        self.currentMap.render(self.game_surface, self.camera)
        if not self.paused_from_explosion:
            self.base.draw(self.game_surface, self.camera)

        for building in self.buildings:
                building.draw(self.game_surface, self.camera)

        for wall in self.walls:
                wall.draw(self.game_surface, self.camera)

        self.combat_system.draw(self.game_surface, self.camera)
        self.player.draw(self.game_surface, self.camera)
        if self.paused_from_explosion and self.explosion is not None:
            self.explosion.draw(self.game_surface, self.camera)
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

        if self.cheat_system.godmode:
            text = self.hud.fontTimer.render("GODMODE", False, "yellow")
            self.screen.blit(text, (20, 90))

        self.building_menu.draw(self.screen)

        if self.state == StateType.Pause and not self.paused_from_explosion:
            self.pause_menu.draw(self.screen)
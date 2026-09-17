import pygame

from karma.enums import StateType, RessourceType
from karma.entities.buildings.turret import Turret
from karma.settings import (SCREEN_HEIGHT,SCREEN_WIDTH,SOUNDS_DIR,VIDEO_DIR, BASE_NIGHT_HEAL)
from karma.entities.buildings.ressourcesProducer import RessourcesProducer
from karma.entities.buildings.solar_panel import SolarPanel

class PlayScene:

    @staticmethod
    def updatePlayScene(game, dt: float) -> None:
        if game.state != StateType.Play:
            return
        game.player.update(
            dt,
            game.combat_system.enemies,
            game.camera,
            (game.dayMap.width, game.dayMap.height),
        )
        if pygame.mouse.get_pressed()[0]:
            game.player.shoot(game.camera.screenToWorld(pygame.Vector2(pygame.mouse.get_pos())))
        game.base.update(dt, game.cycle_system.isDay)
        game.camera.update(game.player.getCenter())

        game.combat_system.update(dt, game.cycle_system.isDay, game.base, game.walls, game.buildings, game.cycle_system.currentDay)

        game.building_system.removeDestroyed(game.walls)

        # mise à jour des bâtiments, suppression de ceux détruits
        game.buildings = [building for building in game.buildings if not building.isDestroyed()]

        # mise à jour des murs
        game.walls = [wall for wall in game.walls if not wall.isDestroyed()]

        if game.base.isDestroyed():
            game.start_explosion()
            return

        for building in game.buildings:
            if isinstance(building, Turret):
                building.update(dt, game.combat_system.enemies, game.camera, game.cycle_system.isDay)
            elif isinstance(building, RessourcesProducer):
                building.update(dt, game.cycle_system.isDay)
                if building.requiresDaylight and not game.cycle_system.isDay:
                    continue
                produced = building.tryProduce(dt)
                if produced > 0:
                    game.rm.add(building.resourceType, produced)

        for wall in game.walls:
            wall.update(game.cycle_system.isDay)

        karmaDelta = sum(building.getKarmaImpact(dt) for building in game.buildings)
        game.rm.applyKarmaDelta(karmaDelta)

        build_slots = game.currentMap.get_build_slots()
        game.building_system.update(game.player, build_slots)

        slot = game.building_system.currentSlot
        if slot is not None and game.building_system.isSlotFree(slot["id"]):
            game.building_menu.isVisible= True
        else:
            game.building_menu.isVisible = False
            
        if game.cycle_system.update(dt):
            game.currentMap = game.dayMap if game.cycle_system.isDay else game.nightMap
            if game.cycle_system.isDay:
                game.combat_system.enemies.clear()
                game.base.heal(BASE_NIGHT_HEAL)
                if game.cycle_system.currentDay >= 4:
                    if game.rm.getStock(RessourceType.Karma) >= 0:
                        game.start_good_ending()
                    else:
                        game.start_mid_ending()
                    return
                pygame.mixer.music.load(SOUNDS_DIR / "DayMusic.mp3")
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.load(SOUNDS_DIR / "NightMusic.mp3")
                pygame.mixer.music.play(-1)

            cinematic_directory = (
                VIDEO_DIR / "Vidéo Fin Eclipse"
                if game.cycle_system.isDay
                else VIDEO_DIR / "Vidéo Début Eclipse"
            )
            game.start_cinematic(cinematic_directory, StateType.Play)

    @staticmethod
    def drawPlayScene(game) -> None:
        game.currentMap.render(game.game_surface, game.camera)
        if not game.paused_from_explosion:
            game.base.draw(game.game_surface, game.camera)

        for building in game.buildings:
                building.draw(game.game_surface, game.camera)

        for wall in game.walls:
                wall.draw(game.game_surface, game.camera)

        game.combat_system.draw(game.game_surface, game.camera)
        game.player.draw(game.game_surface, game.camera)
        if game.paused_from_explosion and game.explosion is not None:
            game.explosion.draw(game.game_surface, game.camera)
        pygame.transform.scale(game.game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT), game.screen)

        game.hud.draw(
            game.screen,
            game.cycle_system.currentDay,
            game.cycle_system.isDay,
            game.cycle_system.cycleTimer,
            game.cycle_system.currentDuration(),
            game.base.health,
            game.base.max_health,
        )

        if game.cheat_system.godmode:   
            text = game.hud.fontTimer.render("GODMODE", False, "yellow")
            game.screen.blit(text, (20, 90))

        game.building_menu.draw(game.screen)

        if game.state == StateType.Pause and not game.paused_from_explosion:
            game.pause_menu.draw(game.screen)
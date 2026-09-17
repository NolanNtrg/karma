import pygame
from karma.entities.buildings.building import Building
from karma.entities.player.player import Player
from karma.enums import RessourceType
from karma.systems.resourceManager import RessourceManager
from karma.entities.buildings.turret import Turret
from karma.entities.buildings.coal_plant import CoalPlant
from karma.entities.buildings.solar_panel import SolarPanel
from karma.entities.buildings.plantation import Plantation
from karma.entities.buildings.driller import Driller
from karma.enums import BuildingType
from karma.settings import (
    COAL_PLANT_COST,
    COAL_PLANT_HEALTH,
    COAL_PLANT_PRODUCTION_AMOUNT,
    COAL_PLANT_PRODUCTION_INTERVAL,
    DRILLER_COST,
    DRILLER_HEALTH,
    DRILLER_PRODUCTION_AMOUNT,
    DRILLER_PRODUCTION_INTERVAL,
    PLANTATION_COST,
    PLANTATION_HEALTH,
    PLANTATION_PRODUCTION_AMOUNT,
    PLANTATION_PRODUCTION_INTERVAL,
    SOLAR_PANEL_COST,
    SOLAR_PANEL_HEALTH,
    SOLAR_PANEL_PRODUCTION_AMOUNT,
    SOLAR_PANEL_PRODUCTION_INTERVAL,
    TURRET_ATTACK_DAMAGE,
    TURRET_ATTACK_INTERVAL,
    TURRET_ATTACK_RANGE,
    TURRET_COST,
    TURRET_HEALTH,
)

BUILDING_COSTS: dict[BuildingType, int] = {
    BuildingType.Turret: TURRET_COST,
    BuildingType.CoalPlant: COAL_PLANT_COST,
    BuildingType.SolarPanel: SOLAR_PANEL_COST,
    BuildingType.Plantation: PLANTATION_COST,
    BuildingType.Driller: DRILLER_COST,
}



class BuildingsSystem:
    def __init__(self) :
        self.currentSlot : dict | None = None
        self.dictOccupedSlot : dict[int, Building] = {}

    def isSlotFree(self, slotId):
        return slotId not in self.dictOccupedSlot

    def update(self, player : Player, buildSlots : list[dict]) :
        playerCenter = player.getCenter()

        foundSlot = None
        for slot in buildSlots : 
            if slot["rect"].collidepoint(playerCenter.x,playerCenter.y) : 
                foundSlot = slot
                break

        if foundSlot != self.currentSlot :
            self.currentSlot = foundSlot

            if self.currentSlot is not None:
                slot_id = self.currentSlot["id"]
                slot_name = self.currentSlot["name"]

                if self.isSlotFree(slot_id):
                    print(f"[BUILD] {slot_name} est LIBRE. Prêt pour construire un bâtiment !")
                else:
                    building = self.dictOccupedSlot[slot_id]
                    print(f"[BUILD] {slot_name} est OCCUPÉ par {building.__class__.__name__} (HP: {building.health}).")
            else:
                print("[BUILD] Le joueur est sorti de la zone de construction.")

    def build(self, building_type: BuildingType, ressource_manager: RessourceManager):
        if self.currentSlot is not None:
            if self.isSlotFree(self.currentSlot["id"]):
                cost_type = RessourceType.Energy if building_type == BuildingType.Turret else RessourceType.RawMaterial
                cost = BUILDING_COSTS[building_type]

                if ressource_manager.hasEnough(cost_type, cost):
                    ressource_manager.consume(cost_type, cost)
                    slot_center = self.currentSlot["rect"].center
                    position = pygame.Vector2(slot_center[0] - 32, slot_center[1] - 32)

                    # crée le bâtiment en fonction du type choisi
                    if building_type == BuildingType.Turret:
                        building = Turret(
                            position,
                            health=TURRET_HEALTH,
                            energyCost=TURRET_COST,
                            attackRange=TURRET_ATTACK_RANGE,
                            attackDamage=TURRET_ATTACK_DAMAGE,
                            attackInterval=TURRET_ATTACK_INTERVAL,
                        )
                    elif building_type == BuildingType.CoalPlant:
                        building = CoalPlant(
                            position,
                            health=COAL_PLANT_HEALTH,
                            energyCost=COAL_PLANT_COST,
                            productionAmount=COAL_PLANT_PRODUCTION_AMOUNT,
                            productionInterval=COAL_PLANT_PRODUCTION_INTERVAL,
                        )
                    elif building_type == BuildingType.SolarPanel:
                        building = SolarPanel(
                            position,
                            health=SOLAR_PANEL_HEALTH,
                            energyCost=SOLAR_PANEL_COST,
                            productionAmount=SOLAR_PANEL_PRODUCTION_AMOUNT,
                            productionInterval=SOLAR_PANEL_PRODUCTION_INTERVAL,
                        )
                    elif building_type == BuildingType.Plantation:
                        building = Plantation(
                            position,
                            health=PLANTATION_HEALTH,
                            energyCost=PLANTATION_COST,
                            productionAmount=PLANTATION_PRODUCTION_AMOUNT,
                            productionInterval=PLANTATION_PRODUCTION_INTERVAL,
                        )
                    elif building_type == BuildingType.Driller:
                        building = Driller(
                            position,
                            health=DRILLER_HEALTH,
                            energyCost=DRILLER_COST,
                            productionAmount=DRILLER_PRODUCTION_AMOUNT,
                            productionInterval=DRILLER_PRODUCTION_INTERVAL,
                        )

                    self.dictOccupedSlot[self.currentSlot["id"]] = building
                    return building


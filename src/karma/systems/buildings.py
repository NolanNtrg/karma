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

    def build(self, building_type: BuildingType, ressource_manager: RessourceManager, amount: int):
        if self.currentSlot is not None:
            if self.isSlotFree(self.currentSlot["id"]):
                cost_type = RessourceType.Energy if building_type == BuildingType.Turret else RessourceType.RawMaterial

                if ressource_manager.hasEnough(cost_type, amount):
                    ressource_manager.consume(cost_type, amount)
                    slot_center = self.currentSlot["rect"].center
                    position = pygame.Vector2(slot_center[0] - 32, slot_center[1] - 32)

                    if building_type == BuildingType.Turret: 
                        building = Turret(position, health=100, energyCost=10, attackRange=150.0, attackDamage=25, attackInterval=1000.0)
                    elif building_type == BuildingType.CoalPlant: 
                        building = CoalPlant(position, health=200, energyCost=100, productionAmount=25, productionInterval=2000.0)
                    elif building_type == BuildingType.SolarPanel: 
                        building = SolarPanel(position, health=150, energyCost=100, productionAmount=10, productionInterval=2000.0)
                    elif building_type == BuildingType.Plantation:
                        building = Plantation(position, health=150, energyCost=100, productionAmount=10, productionInterval=2000.0)
                    elif building_type == BuildingType.Driller:
                        building = Driller(position, health=200, energyCost=100, productionAmount=25, productionInterval=2000.0)

                    self.dictOccupedSlot[self.currentSlot["id"]] = building
                    return building
                


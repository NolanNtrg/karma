import pygame
from karma.entities.buildings.building import Building
from karma.entities.player.player import Player
from karma.enums import RessourceType
from karma.resources.ressourceManager import RessourceManager
from karma.entities.buildings.turret import Turret

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

    def build(self,building_type : Building, ressource_manager : RessourceManager , amount : int) :
        print("etape 1")
        if self.currentSlot != None :
            print("etape 2")
            if self.isSlotFree(self.currentSlot["id"]) :
                print("etape 3")
                if ressource_manager.hasEnough(RessourceType.RawMaterial, amount):
                    print("etape 4")
                    print(ressource_manager.getStock(RessourceType.RawMaterial))
                    ressource_manager.consume(RessourceType.RawMaterial, amount)
                    print(ressource_manager.getStock(RessourceType.RawMaterial))
                    position = pygame.Vector2(self.currentSlot["rect"].x, self.currentSlot["rect"].y)
                    
                    # se servir de building_type après pour faire des ifs pour chaque building au cas par cas

                    turret = Turret(position,health=100,energyCost=10,attackRange=150.0,attackDamage=25,attackInterval=1000.0)

                    self.dictOccupedSlot[self.currentSlot["id"]] = turret
                    return turret
                


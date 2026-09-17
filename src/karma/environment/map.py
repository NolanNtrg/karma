from pathlib import Path

import pygame
from pytmx import TiledObject
from pytmx.util_pygame import load_pygame

from karma.environment.camera import Camera


class MapManager:
    def __init__(self, filename: Path) -> None:
        # load_pygame convertit automatiquement les tuiles en surfaces Pygame
        self.tmx_data = load_pygame(filename)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

    def render(self, screen: pygame.Surface, camera: Camera | None = None) -> None:
        for layer in self.tmx_data.visible_layers:
            # On ne dessine que les calques de tuiles standards
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        position = pygame.Vector2(x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                        if camera:
                            position = camera.apply(position)
                        screen.blit(tile, position)


    def get_vaisseau_slot(self) -> TiledObject:
        return self.tmx_data.get_object_by_name("vaisseau")

    def get_build_slots(self) -> list[dict]:
        # retourne la liste des slots en rectangle
        slots = []
        try : 
            layer = self.tmx_data.get_layer_by_name("BuildSlots")
            for buildSlot in layer:
                if getattr(buildSlot, "type", None) == "built_slot" :
                    slots.append({
                        "id" : buildSlot.id,
                        "name" : buildSlot.name,
                        "rect": pygame.Rect(round(buildSlot.x),round(buildSlot.y),round(buildSlot.width),round(buildSlot.height))
                    })
        except :
            pass
        return slots
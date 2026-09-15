import pygame
from pytmx.util_pygame import load_pygame

class MapManager:
    def __init__(self, filename):
        # load_pygame convertit automatiquement les tuiles en surfaces Pygame
        self.tmx_data = load_pygame(filename)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

    def render(self, screen, camera=None):
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
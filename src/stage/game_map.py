import array

import numpy as np
from tcod.console import Console

import src.stage.tile_types as tile_types


class GameMap:
    """Klass för att representera spel kartan"""
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.visible_floor, order="F")

        self.tiles[30, 20] = tile_types.visible_wall

    def in_bounds(self, x: int, y: int) -> bool:
        """Återvänder sant ifall koordinaten är inom kartan"""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        for (i, row) in enumerate(self.tiles):
            for (j, tile) in enumerate(row):
                tile.render(console, i, j)

    def get_tile(self, x, y):
        return self.tiles[x, y]


from typing import Iterable

import numpy as np
from tcod.console import Console

import stage.tile_types as tile_types


class GameMap:
    """Klass för att representera spel kartan"""

    def __init__(self, width: int, height: int, entities: Iterable["Entity"] = ()):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.transparent_tiles = np.full((width, height), fill_value=False, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

        self.entities = set(entities)

    def in_bounds(self, x: int, y: int) -> bool:
        """Återvänder sant ifall koordinaten är inom kartan"""
        return 0 < x < self.width and 0 < y < self.height

    def render(self, console: Console) -> None:
        """Metod för att gå igenom alla tiles och sedan rendera varje tile"""
        # TODO: Kolla över metoden igen och se om det finns något bättre sätt, det funkar iallafall
        for (x, row) in enumerate(self.tiles):
            for (y, tile) in enumerate(row):
                if self.visible[x, y]:
                    tile.visible = True
                    if tile.type == tile_types.types_of_tiles["floor"]:
                        tile.color = tile_types.floor_color
                    elif tile.type == tile_types.types_of_tiles["wall"]:
                        tile.color = tile_types.wall_color
                    tile.render(console, x, y)
                elif self.explored[x, y]:
                    tile.seen = True
                    tile.color = tile_types.seen_color
                    tile.render(console, x, y)

        for entity in self.entities:
            try:
                if (
                    self.visible[entity.x, entity.y]
                    and not self.tiles[entity.x, entity.y] == tile_types.wall
                    and self.in_bounds(entity.x, entity.y)
                ):
                    entity.render(console, entity.x, entity.y)
            except IndexError:
                print("IndexError: ", entity.x, entity.y)
                continue

    def get_tile(self, x, y):
        return self.tiles[x, y]

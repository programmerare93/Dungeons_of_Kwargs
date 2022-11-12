import numpy as np
from tcod.console import Console
import random


import stage.tile_types as tile_types

from typing import Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.engine import Engine

from creature.entity import Entity


class GameMap:
    """Klass för att representera spel kartan"""

    def __init__(self, width: int, height: int, entities: Iterable["Entity"] = ()):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")
        self.entities = set(entities)

    def in_bounds(self, x: int, y: int) -> bool:
        """Återvänder sant ifall koordinaten är inom kartan"""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_blocked(self, x, y) -> bool:
        try:
            if (
                not self.get_tile(x + 1, y).transparent
                and not self.get_tile(x - 1, y).transparent
                and not self.get_tile(x, y + 1).transparent
                and not self.get_tile(x + 1, y + 1).transparent
                and not self.get_tile(x - 1, y + 1).transparent
                and not self.get_tile(x, y - 1).transparent
                and not self.get_tile(x + 1, y - 1).transparent
                and not self.get_tile(x - -1, y - 1).transparent
            ):
                return True
            else:
                return False
        except IndexError:
            return True

    def render(self, console: Console) -> None:
        """Metod för att gå igenom alla tiles och sedan rendera varje tile"""
        # TODO: Kolla över metoden igen och se om det finns något bättre sätt, det funkar iallafall
        for (x, row) in enumerate(self.tiles):
            for (y, tile) in enumerate(row):
                if self.visible[x, y] and not self.is_blocked(x, y):
                    if self.get_tile(x, y).transparent:
                        tile.visible = True
                    if tile.type == tile_types.types_of_tiles["floor"]:
                        tile.color = tile_types.floor_color
                    elif tile.type == tile_types.types_of_tiles["wall"]:
                        tile.color = tile_types.wall_color
                    tile.render(console, x, y)
                elif self.explored[x, y] and not self.is_blocked(x, y):
                    tile.seen = True
                    tile.color = tile_types.seen_color
                    tile.render(console, x, y)

        for entity in self.entities:
            try:
                if (
                    self.visible[entity.x, entity.y]
                    and not self.is_blocked(entity.x, entity.y)
                    and not self.tiles[entity.x, entity.y] == tile_types.wall
                ):
                    entity.render(console, entity.x, entity.y)
            except IndexError:
                continue

    def get_tile(self, x, y):
        return self.tiles[x, y]

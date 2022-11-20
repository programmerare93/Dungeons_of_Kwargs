from typing import Iterable, Set

import numpy as np
from tcod.console import Console
import tcod.path

import stage.tile_types as tile_types
from creature.entity import Entity


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

    def calculate_distance(self, x1, y1, x2, y2):
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

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
                    elif tile.type == tile_types.types_of_tiles["trap"]:
                        if tile.hasBeenActivated:
                            tile.color = (255, 0, 0)
                        else:
                            tile.color = tile_types.trap_color
                    elif tile_types == tile_types.types_of_tiles["stair"]:
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

    def entity_at_location(self, x: int, y: int) -> Set[Entity]:
        return {entity for entity in self.entities if entity.x == x and entity.y == y}

    def get_tile(self, x, y):
        return self.tiles[x, y]

    def generate_pathfinding_map(self):
        """Genererar en pathfinding map som används för att hitta vägen till spelaren"""
        self.pathfinding_map = np.full(
            (self.width, self.height), fill_value=0, order="F"
        )
        for (x, row) in enumerate(self.tiles):
            for (y, tile) in enumerate(row):
                if tile.transparent:
                    self.pathfinding_map[x, y] = 1

    def pathfinding(self, x1, y1, x2, y2):
        """Tar emot två koordinater och returnerar en lista med koordinater som spelaren ska följa för att komma till målet"""
        path = tcod.path.AStar(self.pathfinding_map)
        return path.get_path(x1, y1, x2, y2)

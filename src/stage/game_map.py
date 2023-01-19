from typing import Iterable, Set, List, Tuple

import numpy as np
from tcod.console import Console
import tcod.path

import stage.tile_types as tile_types
from creature.entity import Entity
from window.color import *


class GameMap:
    """Klass för att representera spel kartan"""

    def __init__(self, width: int, height: int, entities: List[Entity] = ()):
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.transparent_tiles = np.full((width, height), fill_value=False, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

        self.entities = entities
        self.difficulty = 1

    def in_bounds(self, x: int, y: int) -> bool:
        """Återvänder sant ifall koordinaten är inom kartan"""
        return 0 < x < self.width and 0 < y < self.height

    def calculate_distance(self, x1, y1, x2, y2) -> int:
        """Beräknar avståndet mellan två koordinater med hjälp av pythagoras sats"""
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def render(self, console: Console) -> None:
        """Metod för att gå igenom alla tiles och sedan rendera varje tile"""
        for (x, row) in enumerate(self.tiles):
            for (y, tile) in enumerate(row):
                if self.visible[x, y]:  # Varje tile som är synlig renderas
                    tile.visible = True
                    if tile.type == tile_types.types_of_tiles["floor"]:
                        tile.color = all_wall_colors[self.difficulty - 2]
                    elif tile.type == tile_types.types_of_tiles["wall"]:
                        tile.color = all_wall_colors[self.difficulty - 2]
                    elif tile.type == tile_types.types_of_tiles["stair"]:
                        tile.color = tile_types.wall_color
                    elif tile.type == tile_types.types_of_tiles["trap"]:
                        if tile.hasBeenActivated:
                            tile.color = red
                        else:
                            tile.color = tile_types.trap_color

                    tile.render(console, x, y)
                elif self.explored[
                    x, y
                ]:  # Varje tile som spelaren har varit nära renderas med en annan färg
                    tile.seen = True
                    tile.color = all_seen_colors[self.difficulty - 2]
                    tile.render(console, x, y)

        for entity in self.entities:  # Renderar alla entities om de är synliga
            if (
                self.visible[entity.x, entity.y]
                and not self.tiles[entity.x, entity.y] == tile_types.wall
                and self.in_bounds(entity.x, entity.y)
            ):
                entity.render(console, entity.x, entity.y)

    def entity_at_location(
        self, x: int, y: int
    ) -> List[Entity]:  # Ger en lista med alla entities som finns på en viss koordinat
        return [entity for entity in self.entities if entity.x == x and entity.y == y]

    def monster_or_chest_at_location(
        self, x: int, y: int
    ) -> List[
        Entity
    ]:  # Ger en lista med alla entities som finns på en viss koordinat utom spelaren
        return [
            entity
            for entity in self.entities
            if entity.x == x and entity.y == y and entity.char != "@"
        ]

    def get_tile(self, x, y) -> Iterable:  # Returnerar en tile på en viss koordinat
        return self.tiles[x, y]

    def generate_pathfinding_map(self) -> None:
        """Genererar en pathfinding map som används för att hitta vägen till spelaren"""
        self.pathfinding_map = np.full(
            (self.width, self.height), fill_value=0, order="F"
        )
        for (x, row) in enumerate(self.tiles):
            for (y, tile) in enumerate(row):
                if tile.type in (
                    tile_types.types_of_tiles["floor"],
                    tile_types.types_of_tiles["trap"],
                ) and not self.monster_or_chest_at_location(x, y):
                    self.pathfinding_map[x, y] = 1

    def pathfinding(self, x1, y1, x2, y2) -> List[Tuple[int, int]]:
        """Tar emot två koordinater och returnerar en lista med koordinater (Tuples) som ett monster ska följa för att komma till spelaren"""
        path = tcod.path.AStar(self.pathfinding_map)
        return path.get_path(x1, y1, x2, y2)

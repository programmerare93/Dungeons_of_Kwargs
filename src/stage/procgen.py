from __future__ import annotations

import random
import numpy as np

import tcod

import stage.tile_types as tile_types
from creature.entity import Entity, generate_monsters
from creature.items import potions
from stage.game_map import GameMap
from stage.rooms import Room


class Generator:
    def __init__(
        self,
        max_rooms: int,
        map_width: int,
        map_height: int,
        player: Entity,
        min_width=4,
        min_height=4,
    ):
        self.player = player
        self.dungeon = GameMap(map_width, map_height, entities=[player])
        self.room_list = []
        self.max_rooms = max_rooms
        self.difficulty = 1
        self.max_monsters_per_room = 1
        self.map_width = map_width
        self.map_height = map_height

        self.max_width = 14
        self.min_width = 6
        self.max_height = 14
        self.min_height = 6

    def create_tunnel(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        """
        Metod för att skapa en tunnel mellan två punkter med hjälp av tcods bresenham algoritm
        Tar in en start punkt och slut punkt i formen av en tuple med två heltal (x, y)
        Återvänder inget
        """
        x1, y1 = start
        x2, y2 = end
        if random.randint(0, 1):
            # Rör sig horisontellt sen vertikalt
            corner_x, corner_y = x2, y1
        else:
            # Rör sig vertikalt sen horisontellt
            corner_x, corner_y = x1, y2

        for (x, y) in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
            self.dungeon.tiles[x, y] = tile_types.floor

        for (x, y) in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
            self.dungeon.tiles[x, y] = tile_types.floor

    def generate_dungeon(self):
        """
        Metod för att skapa själva kartan
        Tar inte in något
        Återvänder inget
        """
        # Återställer alla eventuella gamla nivåer
        for (x, row) in enumerate(self.dungeon.tiles):
            for (y, value) in enumerate(row):
                self.dungeon.tiles[x, y] = tile_types.wall
        self.dungeon.explored = np.full(
            (self.map_width, self.map_height), fill_value=False, order="F"
        )
        self.dungeon.transparent_tiles = np.full(
            (self.map_width, self.map_height), fill_value=False, order="F"
        )

        self.dungeon.entities = [self.player]

        self.room_list.clear()

        for _ in range(self.max_rooms):
            width = random.randint(self.min_width, self.max_width)
            height = random.randint(self.min_height, self.max_height)

            x = random.randint(1, self.map_width - width - 1)
            y = random.randint(1, self.map_height - height - 1)

            new_room = Room(x, y, width, height)

            # Kommer att gå igenom alla rum i room_list
            # och kollar ifall någon överlappar med det nya rummet
            if any(new_room.intersects(other_room) for other_room in self.room_list):
                continue  # Starta om ifall det överlappade

            self.dungeon.tiles[new_room.inner] = tile_types.floor

            if len(self.room_list) == 0:
                self.player.x, self.player.y = new_room.center
            else:
                self.create_tunnel(self.room_list[-1].center, new_room.center)

            self.room_list.append(new_room)

        # Tar bort första rummet som alternativ
        available_stair_rooms = self.room_list
        available_stair_rooms.pop(0)
        # Gör om ett slumpmässigt rum till rummet med trappan i
        stair_room = random.choice(available_stair_rooms)
        self.dungeon.tiles[stair_room.center] = tile_types.stair_case

        for (x, row) in enumerate(self.dungeon.tiles):
            for (y, value) in enumerate(row):
                if self.dungeon.tiles[x, y] == tile_types.floor:
                    if random.randint(0, 50) == 25:
                        self.dungeon.tiles[x, y] = tile_types.Trap(
                            tile_types.trap_color, difficulty=self.difficulty
                        )

        # Potions generation
        for room in self.room_list[1::]:
            if random.random() < 0.25:  # 25% chans att ett rum innehåller en potion
                x = random.randint(room.center[0] - (room.width // 2), room.center[0] + (room.width // 2))
                y = random.randint(room.center[1] - (room.height // 2), room.center[1] + (room.height // 2))
                self.dungeon.tiles[x, y] = random.choice(potions)

        # Monster generation
        for room in self.room_list[1::]:
            for _ in range(random.randint(0, self.max_monsters_per_room)):
                generate_monsters(room, self.dungeon)

        self.dungeon.generate_pathfinding_map()

    def get_dungeon(self):
        return self.dungeon

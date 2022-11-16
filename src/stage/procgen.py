from __future__ import annotations

import random
from typing import Iterator, List, Tuple

import tcod

import stage.tile_types as tile_types
from creature.entity import Entity, generate_monsters
from stage.game_map import GameMap
from stage.rooms import *


def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[slice, slice]]:
    """Återvänder en L-formad tunnel mellan de två punkterna"""
    x1, y1 = start
    x2, y2 = end
    if random.randint(0, 1) == 1:  # 50% chans
        # Rör sig horisontellt sen vertikalt
        corner_x, corner_y = x2, y1
    else:
        # Rör sig vertikalt sen horisontellt
        corner_x, corner_y = x1, y2

    # los står för lign of sight, bresenham står för bresenhams linjealgoritm
    for (x, y) in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y

    for (x, y) in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    """Genererar en ny dungeon nivå"""
    dungeon = GameMap(map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    for room in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        # 'any' återvänder sant om något värde är sant i det givna itererbara objektet
        # kommer att gå igenom alla andra rum och se om de överlappar med det nya
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # Rummet överlappar ett annat rum så vi försöker igen
        # Rummet var giltigt

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # Det här kommer vara första rummet spelaren startar i
            player.x, player.y = new_room.center
        else:  # Resten
            # Gräver en tunnel mellan detta rum och den förra (därmed rooms[-1])
            for (x, y) in tunnel_between(rooms[-1].center, new_room.center):
                if random.randint(1, 30) == 10:
                    dungeon.tiles[x, y] = tile_types.trap
                else:
                    dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)

    for room in rooms[1::]:
        generate_monsters(room, dungeon)

    return dungeon

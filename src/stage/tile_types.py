from typing import Tuple

from tcod import Console


class Tile:
    walkable: bool
    visible: bool
    transparent: bool
    seen: bool
    color: Tuple[int, int, int]
    char: str

    def __init__(self,
                 walkable: bool,
                 visible: bool,
                 transparent: bool,
                 seen: bool,
                 color: Tuple[int, int, int],
                 char: str):
        self.walkable = walkable
        self.visible = visible
        self.transparent = transparent
        self.seen = seen
        self.color = color
        self.char = char

    def render(self, console: Console, x: int, y: int):
        if self.visible:
            console.print(x, y, self.char, self.color)
        elif self.seen:
            console.print(x, y, self.char, self.color)
        else:
            console.print(x, y, self.char, (0, 0, 0))


class Floor(Tile):
    def __init__(self, color):
        self.walkable = True
        self.visible = False
        self.transparent = True
        self.seen = False
        self.color = color
        self.char = '.'


class Wall(Tile):
    def __init__(self, color):
        self.walkable = False
        self.visible = False
        self.transparent = False
        self.seen = False
        self.color = color
        self.char = '#'


seen_color = (55, 55, 55)
floor_color = (155, 200, 255)
wall_color = (255, 255, 255)

visible_floor = Floor(floor_color)
visible_floor.visible = True

floor = Floor(floor_color)

seen_floor = Floor(seen_color)
seen_floor.seen = True

visible_wall = Wall(wall_color)
visible_wall.visible = True

wall = Wall(wall_color)

seen_wall = Wall(seen_floor)
seen_wall.seen = True

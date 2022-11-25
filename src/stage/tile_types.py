from typing import Tuple

from tcod import Console


class Tile:
    type: int
    walkable: bool
    visible: bool
    transparent: bool
    seen: bool
    color: Tuple[int, int, int]
    char: str
    has_monster: bool

    def __init__(
        self,
        walkable: bool,
        visible: bool,
        transparent: bool,
        seen: bool,
        color: Tuple[int, int, int],
        char: str,
    ):
        self.walkable = walkable
        self.visible = visible
        self.transparent = transparent
        self.seen = seen
        self.color = color
        self.char = char

    def render(self, console: Console, x: int, y: int):
        console.print(x, y, self.char, self.color)


class Floor(Tile):
    def __init__(self, color):
        self.walkable = True
        self.visible = False
        self.transparent = True
        self.seen = False
        self.color = color
        self.char = "."
        self.type = 0
        self.has_monster = False


class Wall(Tile):
    def __init__(self, color):
        self.walkable = False
        self.visible = False
        self.transparent = False
        self.seen = False
        self.color = color
        self.char = "#"
        self.type = 1
        self.has_monster = False


# Vi har inget specifikt objekt för att kopiera för Trap
# då det resulterar i att all fällor har samma svårighet
class Trap(Tile):
    def __init__(self, color, difficulty):
        self.walkable = True
        self.visible = False
        self.transparent = True
        self.seen = False
        self.color = color
        self.char = "."
        self.type = 2
        self.has_monster = False
        self.difficulty = difficulty
        self.hasBeenActivated = False


class StairCase(Tile):
    def __init__(self, color):
        super().__init__(
            walkable=True,
            visible=False,
            transparent=True,
            seen=False,
            color=color,
            char="<")
        self.type = 3
        self.has_monster = False


types_of_tiles = {"floor": 0, "wall": 1, "trap": 2, "stair": 3}

seen_color = (55, 55, 55)
floor_color = (155, 200, 255)
wall_color = (255, 255, 255)
trap_color = (100, 210, 210)

floor = Floor(floor_color)

wall = Wall(wall_color)

stair_case = StairCase(wall_color)

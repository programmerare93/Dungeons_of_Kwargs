import random
from typing import Tuple

from tcod import Console
from window.color import *


class Tile:
    """Klass för att representera en tile"""

    type: int
    walkable: bool
    visible: bool
    transparent: bool  # Ser till att spelaren inte kan se igenom vissa tiles
    seen: bool  # Ser till att spelaren kan se tiles som han har varit nära
    color: Tuple[int, int, int]
    char: str

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
    """Inte för att representera en våning, utan för att representera en tile som spelaren kan gå på"""

    def __init__(self, color):
        self.walkable = True
        self.visible = False
        self.transparent = True
        self.seen = False
        self.color = color
        self.char = "."
        self.type = 0


class Wall(Tile):
    def __init__(self, color):
        self.walkable = False
        self.visible = False
        self.transparent = False
        self.seen = False
        self.color = color
        self.char = "#"
        self.type = 1


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
        self.difficulty = difficulty
        self.hasBeenActivated = False


class StairCase(Tile):
    """En tile som spelaren kan använda för att gå ner"""

    def __init__(self, color):
        super().__init__(
            walkable=True,
            visible=False,
            transparent=True,
            seen=False,
            color=color,
            char="<",
        )
        self.type = 3


types_of_tiles = {
    "floor": 0,
    "wall": 1,
    "trap": 2,
    "stair": 3,
}  # Används i andra filer för tydligare kod

# Olika färger för olika tiles
seen_color = dark_gray
floor_color = sky_blue
wall_color = white
trap_color = baby_blue

floor = Floor(floor_color)

wall = Wall(wall_color)

stair_case = StairCase(wall_color)

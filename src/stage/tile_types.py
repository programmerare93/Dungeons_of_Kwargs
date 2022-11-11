from typing import Tuple

from tcod import Console


class Tile:
    walkable: bool
    visible: bool
    color: Tuple[int, int, int]
    char: str

    def __init__(self, walkable: bool, visible: bool, color: Tuple[int, int, int], char: str):
        self.walkable = walkable
        self.visible = visible
        self.color = color
        self.char = char

    def render(self, console: Console, x: int, y: int):
        if self.visible:
            console.print(x, y, self.char, self.color)
        else:
            console.print(x, y, self.char, (0, 0, 0))


visible_floor = Tile(walkable=True, visible=True, color=(155, 200, 255), char='.')
nonvisible_floor = Tile(walkable=True, visible=False, color=(155, 200, 255), char='.')

visible_wall = Tile(walkable=False, visible=True, color=(255, 255, 255), char='#')
nonvisible_wall = Tile(walkable=False, visible=False, color=(255, 255, 255), char='#')

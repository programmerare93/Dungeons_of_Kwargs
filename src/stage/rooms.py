from __future__ import annotations

from typing import Tuple

import stage.tile_types as tile_types
from stage.game_map import GameMap


class Room:
    """Klass för att representera ett rektangulärt rum"""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height

    # @property gör så att vi kan använda metoden som en konstant variabel snarare än en metod
    # t.ex kan vi skriva mitt_rum.center istället för mitt_rum.center()
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Återvänder den inre arean av det givna rummet"""
        # slice() kommer att återge de givna argumenten
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: Room) -> bool:
        """Återvänder sant om den här instansen av rummet överlappar med ett annat rum"""
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )

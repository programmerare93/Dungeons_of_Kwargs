from __future__ import annotations

from typing import Tuple


class Room:
    """Bas klass för alla andra rum klasser"""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Återvänder den inre arean av det givna rummet som en 2D array index"""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)


class RectangularRoom(Room):
    """Klass för att representera ett rektangulärt rum"""

    def intersects(self, other: RectangularRoom) -> bool:
        """Återvänder sant om den här instansen av rummet överlappar med ett annat rum"""
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


class CircularRoom(Room):
    """Klass för att representera ett runt rum"""
    # TODO: Implementera klassen
    pass

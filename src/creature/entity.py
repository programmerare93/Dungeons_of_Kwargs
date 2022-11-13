from typing import Tuple
from tcod import Console
import random


class Entity:
    """Generisk klass för att representera en 'entitet', något som en fiende eller spelare"""

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int):
        """Ändrar x och y koordinaten på en entity med ett givet värde"""
        self.x += dx
        self.y += dy

    def render(self, console: Console, x: int, y: int):
        """Ritar ut en entity på en given konsol"""
        console.print(x=x, y=y, string=self.char, fg=self.color)


def generate_entities(room, game_map):
    """Genererar en entity i en given rum"""
    x = room.center[0] + random.randint(0, room.width - 3)

    y = room.center[1] + random.randint(0, room.width - 3)

    entity = Entity(x, y, "O", (10, 70, 0))
    game_map.entities.add(entity)

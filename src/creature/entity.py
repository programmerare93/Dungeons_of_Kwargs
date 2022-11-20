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


class Player(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        max_hp: int,
        hp: int,
        strength: int,
        perception: int,
        dexterity: int,
        intelligence: int,
    ):
        super().__init__(x, y, char, color)
        self.max_hp = max_hp
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.perception = perception


class Monster(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        max_hp: int,
        hp: int,
        strength: int,
        perception: int,
        dexterity: int,
        intelligence: int,
    ):
        super().__init__(x, y, char, color)
        self.max_hp = max_hp
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.perception = perception


def generate_monsters(room, game_map):
    """Genererar en entity i ett given rum"""

    x = random.randint(room.x1 + 1, room.x2 - 1)

    y = random.randint(room.y1 + 1, room.y2 - 1)

    if not game_map.entity_at_location(x, y):
        if random.random() < 0.8:
            monster = Monster(x, y, "O", (0, 255, 120), 10, 10, 1, 1, 1, 1)
        else:
            monster = Monster(x, y, "T", (0, 0, 255), 16, 16, 3, 3, 3, 3)
        game_map.entities.add(monster)
        room.type = "monster"

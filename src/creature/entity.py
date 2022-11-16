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


def generate_monsters(room, game_map):
    """Genererar en entity i ett given rum"""
    x = room.center[0] + random.randint(0, room.width // 2)

    y = room.center[1] + random.randint(0, room.height // 2)

    if not game_map.entity_at_location(x, y):
        if random.random() < 0.8:
            monster = Entity(x, y, "O", (0, 255, 120))
        else:
            monster = Entity(x, y, "T", (0, 0, 255))
        game_map.entities.add(monster)


class Player(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        hp: int,
        strength: int,
        perception: int,
        dexterity: int,
        intelligence: int,
    ):
        super().__init__(x, y, char, color)
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
        hp: int,
        strength: int,
        dexterity: int,
        constitution: int,
        intelligence: int,
    ):
        super().__init__(x, y, char, color)
        self.hp = hp
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence

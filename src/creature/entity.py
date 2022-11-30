from typing import Tuple
from tcod import Console
import random

from stage.floor import Floor
from actions.actions import MovementAction
from creature.items import *


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
        self.inventory = Inventory(
            self,
            items=[small_healing_potion, small_healing_potion, small_healing_potion],
        )
        self.xp = 0
        self.xp_to_next_level = 100
        self.level = 1


class Monster(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: Tuple[int, int, int],
        difficulty: int,
        max_hp: int,
        strength: int,
        perception: int,
        dexterity: int,
        intelligence: int,
    ):
        super().__init__(x, y, char, color)
        self.difficulty = difficulty
        self.max_hp = max_hp * self.difficulty
        self.hp = self.max_hp * self.difficulty
        self.strength = strength * self.difficulty
        self.dexterity = dexterity * self.difficulty
        self.intelligence = intelligence * self.difficulty
        self.perception = perception * self.difficulty
        self.internal_tick = 0
        self.inventory = Inventory(
            self,
            items=[small_healing_potion, small_healing_potion, small_healing_potion],
        )
        self.xp_value = self.max_hp + self.strength + self.dexterity + self.intelligence

    def monster_pathfinding(self, player, game_map, engine):
        """Monster pathfinding"""
        tile_x, tile_y = (
            game_map.pathfinding(self.x, self.y, player.x, player.y)[0][0],
            game_map.pathfinding(self.x, self.y, player.x, player.y)[0][1],
        )

        action = MovementAction(tile_x - self.x, tile_y - self.y)
        action.perform(engine, self)


class Chest(Entity):
    def __init__(self, x: int, y: int):
        self.hp = inf
        self.x = x
        self.y = y
        self.char = "C"
        self.color = (0, 255, 255)
        self.inventory = Inventory(self, items=[])
        self.closed = True

    def generate_items(self):
        """Genererar ett antal items i en kista"""
        for _ in range(random.randint(1, 3)):
            self.inventory.items.append(random.choice(all_items))


def generate_monsters(room, game_map):
    """Genererar en entity i ett given rum"""

    x = random.randint(room.x1 + 1, room.x2 - 1)

    y = random.randint(room.y1 + 1, room.y2 - 1)

    if not game_map.entity_at_location(x, y):
        if random.random() < 0.8:
            monster = Monster(
                x=x,
                y=y,
                char="O",
                color=(0, 255, 120),
                difficulty=game_map.difficulty,
                max_hp=30,
                strength=10,
                dexterity=5,
                perception=5,
                intelligence=1,
            )
        else:
            monster = Monster(
                x,
                y,
                "T",
                (0, 0, 255),
                difficulty=game_map.difficulty,
                max_hp=16,
                strength=5,
                perception=5,
                dexterity=3,
                intelligence=3,
            )
        game_map.entities.append(monster)
        room.type = "monster"
    else:  # Om det redan finns en entity på den platsen, kör funktionen igen
        generate_monsters(room, game_map)

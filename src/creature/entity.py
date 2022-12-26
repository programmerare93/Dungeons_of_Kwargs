from typing import Tuple
from tcod import Console
import random

from stage.floor import Floor
from actions.actions import MovementAction
from creature.items import *


class Entity:
    """Generisk klass för att representera en 'entitet', något som en fiende eller spelare"""

    def __init__(
        self, x: int, y: int, char: str, color: Tuple[int, int, int], name: str = None
    ):
        self.name = name
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
        char: str,
        color: Tuple[int, int, int],
        max_hp: int,
        strength: int,
        perception: int,
        dexterity: int,
        intelligence: int,
        name: str = None,
    ):
        super().__init__(0, 0, char, color, name)
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.dexterity = dexterity
        self.intelligence = intelligence
        self.perception = perception
        self.inventory = Inventory(
            self,
            items=[small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   small_healing_potion,
                   ],
        )
        self.xp = 0
        self.xp_to_next_level = 100
        self.level = 1
        self.inventory = Inventory(self, items=[small_perception_potion])
        self.used_items = []

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            # Detta är till för att när vi i en annan del av spelet
            # kollar ifall self.heal(amount_of_healing) < entity.max_hp
            # så kommer det inte leda till ett error
            return self.max_hp + 1

        new_hp = self.hp + amount

        if new_hp > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = new_hp

        amount_recovered = new_hp - self.hp

        return amount_recovered


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
        name: str,
    ):
        super().__init__(x, y, char, color, name)
        self.difficulty = difficulty
        self.max_hp = max_hp * self.difficulty
        self.hp = self.max_hp * self.difficulty
        self.strength = strength * self.difficulty
        self.dexterity = dexterity * self.difficulty
        self.intelligence = intelligence * self.difficulty
        self.perception = perception * self.difficulty
        self.inventory = Inventory(
            self,
            items=[small_healing_potion, small_healing_potion, small_healing_potion],
        )
        self.xp_value = self.max_hp + self.strength + self.dexterity + self.intelligence

    def monster_pathfinding(self, player, game_map, engine):
        """Monster pathfinding"""
        if game_map.pathfinding(self.x, self.y, player.x, player.y) == []:
            return
            
        tile_x, tile_y = (
            game_map.pathfinding(self.x, self.y, player.x, player.y)[0][0],
            game_map.pathfinding(self.x, self.y, player.x, player.y)[0][1],
        )

        action = MovementAction(tile_x - self.x, tile_y - self.y)
        action.perform(engine, self)

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return

        new_hp = self.hp + amount

        if new_hp > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp = new_hp

        amount_recovered = new_hp - self.hp

        return amount_recovered

    def take_damage(self, amount: int):
        self.hp -= amount


class Chest(Entity):
    def __init__(self, x: int, y: int, inventory: Inventory, name: str = "Chest"):
        self.name = name
        self.hp = inf
        self.x = x
        self.y = y
        self.char = "C"
        self.color = (0, 255, 255)
        self.inventory = inventory
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
                name="Orc",
                x=x,
                y=y,
                char="O",
                color=(0, 255, 120),
                difficulty=game_map.difficulty,
                max_hp=16,
                strength=5,
                dexterity=5,
                perception=5,
                intelligence=1,
            )
        else:
            monster = Monster(
                name="Troll",
                x=x,
                y=y,
                char="T",
                color=(0, 0, 255),
                difficulty=game_map.difficulty,
                max_hp=30,
                strength=8,
                perception=5,
                dexterity=3,
                intelligence=3,
            )
        game_map.entities.append(monster)
        room.type = "monster"
    else:  # Om det redan finns en entity på den platsen, kör funktionen igen
        generate_monsters(room, game_map)

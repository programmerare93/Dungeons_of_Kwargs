from typing import Tuple
from tcod import Console
from itertools import chain
import random

from stage.floor import Floor
from actions.actions import MovementAction
from creature.items import *


class Entity:
    """Generisk klass för att representera en 'entitet', något som en fiende eller spelare"""

    def __init__(
            self, x: int, y: int, char: str, color: Tuple[int, int, int], name: str = None
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        """Ändrar x och y koordinaten på en entity med ett givet värde"""
        self.x += dx
        self.y += dy

    def render(self, console: Console, x: int, y: int) -> None:
        """Ritar ut en entity på en given konsol"""
        console.print(x=x, y=y, string=self.char, fg=self.color)


class Player(Entity):
    def __init__(
            self,
            max_hp: int,
            strength: int,
            perception: int,
            agility: int,
            intelligence: int,
            name: str = None,
    ) -> None:
        super().__init__(0, 0, '@', (255, 255, 255), "Player")
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.perception = perception
        self.armor = obama_armor
        self.xp = 0
        self.xp_to_next_level = 100
        self.level = 1
        self.inventory = Inventory(self, items=list(chain(*all_items)))
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
            agility: int,
            intelligence: int,
            name: str,
    ) -> None:
        super().__init__(x, y, char, color, name)
        self.difficulty = difficulty
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.strength = strength * self.difficulty
        self.agility = agility * self.difficulty
        self.intelligence = intelligence * self.difficulty
        self.perception = perception * self.difficulty
        self.inventory = Inventory(
            self,
            items=[small_healing_potion, small_healing_potion, small_healing_potion],
        )
        self.xp_value = self.max_hp + self.strength + self.agility + self.intelligence
        self.armor = leather_armor

    def monster_pathfinding(self, player, game_map, engine) -> None:
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

    def take_damage(self, amount: int) -> None:
        self.hp -= amount


class Chest(Entity):
    def __init__(self, x: int, y: int, name: str = "Chest", tier: int = 1) -> None:
        self.name = name
        self.hp = inf
        self.x = x
        self.y = y
        self.char = "C"
        self.color = (0, 255, 255)
        self.closed = True
        self.tier = tier
        self.inventory = Inventory(
            self,
            items=[
                random.choice(all_items[self.tier - 1])
                for _ in range(random.randint(1, 3))
            ],
        )

    def generate_items(self) -> None:
        """Genererar ett antal items i en kista"""
        for _ in range(random.randint(1, 3)):
            self.inventory.items.append(random.choice(all_items[self.tier - 1]))


def choose_monster(x: int, y: int, game_map) -> Monster:
    number = random.randint(0, 100)
    if number < 10:
        monster = Monster(
            name="Wario",
            x=x,
            y=y,
            char="W",
            color=(255, 255, 0),
            difficulty=game_map.difficulty,
            max_hp=40,
            strength=15,
            agility=3,
            perception=4,
            intelligence=20
        )
    elif 10 <= number < 40:
        monster = Monster(
            name="Orc",
            x=x,
            y=y,
            char="O",
            color=(0, 255, 120),
            difficulty=game_map.difficulty,
            max_hp=16,
            strength=10,
            agility=5,
            perception=5,
            intelligence=1,
        )
    elif 40 <= number < 60:
        monster = Monster(
            name="Skeleton",
            x=x,
            y=y,
            char="S",
            color=(255, 255, 255),
            difficulty=game_map.difficulty,
            max_hp=10,
            strength=8,
            perception=6,
            agility=10,
            intelligence=6,
        )
    elif 60 <= number < 80:
        monster = Monster(
            name="Moomin Troll",
            x=x,
            y=y,
            char="M",
            color=(0, 0, 0),
            difficulty=game_map.difficulty,
            max_hp=14,
            strength=10,
            perception=14,
            agility=8,
            intelligence=4
        )
    elif 80 <= number < 90:
        monster = Monster(
            name="Vampire",
            x=x,
            y=y,
            char="V",
            color=(255, 0, 0),
            difficulty=game_map.difficulty,
            max_hp=18,
            strength=8,
            perception=20,
            agility=14,
            intelligence=20
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
            strength=10,
            perception=5,
            agility=3,
            intelligence=3,
        )

    return monster


def generate_monsters(room, game_map) -> None:
    """Genererar en entity i ett givet rum"""

    x = random.randint(room.x1 + 1, room.x2 - 1)

    y = random.randint(room.y1 + 1, room.y2 - 1)

    if not game_map.entity_at_location(x, y):
        monster = choose_monster(x, y, game_map)
        game_map.entities.append(monster)
        room.type = "monster"
    else:  # Om det redan finns en entity på den platsen, kör funktionen igen
        generate_monsters(room, game_map)


def generate_boss(room, game_map) -> None:
    x, y = room.center

    boss = Monster(
        name="Ancient Titan",
        x=x,
        y=y,
        char="B",
        color=(255, 0, 0),
        difficulty=game_map.difficulty + 2,
        max_hp=100,
        strength=15,
        perception=4,
        agility=2,
        intelligence=2
    )
    game_map.entities.append(boss)
    room.type = "monster"

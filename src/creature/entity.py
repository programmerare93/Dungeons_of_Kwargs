from typing import Tuple
from tcod import Console
from itertools import chain
import random

from stage.floor import Floor
from actions.actions import MovementAction
from creature.items import *
from window.color import *


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

    def move(self, dx: int, dy: int) -> None:
        """Ändrar x och y koordinaten på en entity med ett givet värde"""
        self.x += dx
        self.y += dy

    def render(self, console: Console, x: int, y: int) -> None:
        """Ritar ut en entity på en given konsol"""
        console.print(x=x, y=y, string=self.char, fg=self.color)


class Player(Entity):
    """Klass för att representera spelaren"""

    def __init__(
        self,
        char: str,
        color: Tuple[int, int, int],
        stats=[100, 20, 10, 10, 10],  # Hp, Strength, Perception, Agility, Intelligence
        name: str = "Player",
    ):
        super().__init__(0, 0, "@", color, name)
        if stats is None:
            stats = [100, 20, 10, 20, 10]
        self.stats = stats
        self.update_stats()
        self.armor = leather_armor
        self.xp = 0
        self.xp_to_next_level = 100
        self.level = 1
        self.items = [small_healing_potion, small_healing_potion, small_healing_potion]
        self.used_items = []

    def update_stats(self):
        """Används för att uppdatera statsen när de ändras"""
        self.max_hp = self.stats[0]
        self.hp = self.max_hp
        self.strength = self.stats[1]
        self.perception = self.stats[2]
        self.agility = self.stats[3]
        self.intelligence = self.stats[4]


class Monster(Entity):
    """Klass för att representera en fiende"""

    def __init__(
        self,
        char: str,
        color: Tuple[int, int, int],
        name: str,
        move_chance: int = 100,
        stats: list = [10, 10, 10, 10, 10],
        difficulty: int = 1,
        x: int = None,
        y: int = None,
    ):
        super().__init__(x, y, char, color, name)
        self.difficulty = difficulty  # Monstrets statistik kommer att bero på hur svårt den nuvarande nivån är
        self.stats = stats
        self.update_stats()
        self.move_chance = (
            move_chance  # Hur stor chans det är för att monstret ska röra sig
        )
        self.items = [  # Lista med items som monstret har i sitt inventory
            random.choice(all_potions[self.difficulty - 1])
            for _ in range(random.randint(1, 3))
        ]
        self.xp_value = (
            self.max_hp + self.strength + self.agility + self.intelligence
        )  # Hur mycket xp spelaren får när den dödar monstret
        self.armor = all_armor[self.difficulty - 1]
        self.used_items = (
            []
        )  # Lista med items som monstret använt och som fortfarande är aktiva

    def update_stats(self) -> None:
        """Används för att uppdatera statsen när de ändras"""
        self.max_hp = self.stats[0] * self.difficulty
        self.hp = self.max_hp * self.difficulty
        self.strength = self.stats[1] * self.difficulty
        self.perception = self.stats[2] * self.difficulty
        self.agility = self.stats[3] * self.difficulty
        self.intelligence = self.stats[4] * self.difficulty

    def monster_pathfinding(self, player, game_map, engine) -> None:
        """Monster pathfinding"""
        if game_map.pathfinding(self.x, self.y, player.x, player.y) == []:
            return

        tile_x, tile_y = (
            game_map.pathfinding(self.x, self.y, player.x, player.y)[0][
                0
            ],  # Hittar närmaste tile till spelaren
            game_map.pathfinding(self.x, self.y, player.x, player.y)[0][1],
        )

        action = MovementAction(
            tile_x - self.x, tile_y - self.y
        )  # Räknar ut vilken riktning monstret ska röra sig
        action.perform(engine, self)

    def choose_item(self) -> StatItem:
        """Väljer ett item från inventoryt"""
        return random.choice(self.items)


class Chest(Entity):
    """Klass för att representera en kista,
    kommer att fungera som en container för items och ärver från entiteten
    så att vi enkelt kan ta bort den när den öppnas"""

    def __init__(self, x: int, y: int, name: str = "Chest", tier: int = 1):
        self.name = name
        self.hp = inf
        self.x = x
        self.y = y
        self.char = "C"
        self.color = light_blue
        self.closed = True
        self.tier = tier
        self.items = [
            random.choice(
                all_items[self.tier - 1]
            )  # Genererar ett inventory med items beror på vilken tier kistan är vilket beror på våningen
            for _ in range(random.randint(1, 3))
        ]


# Definierar alla fiender

# Nivå 1
orc = Monster(
    name="Orc",
    char="O",
    color=(0, 255, 0),
    stats=[10, 10, 10, 5, 10],
    move_chance=40,
)

troll = Monster(
    name="Troll",
    char="T",
    color=blue,
    stats=[20, 10, 5, 3, 3],
    move_chance=50,
)

goblin = Monster(
    name="Goblin",
    char="G",
    color=light_green,
    stats=[5, 2, 10, 12, 2],
    move_chance=50,
)

# Nivå 2

skeleton = Monster(
    name="Skeleton",
    char="S",
    color=(237, 236, 230),
    stats=[10, 20, 20, 20, 1],
    move_chance=70,
)

rock_elemental = Monster(
    name="Rock Elemental",
    char="R",
    color=(121, 92, 74),
    stats=[100, 15, 10, 15, 50],
    move_chance=30,
)

basilisk = Monster(
    name="Basilisk",
    char="B",
    color=dark_green,
    stats=[25, 20, 20, 20, 20],
    move_chance=65,
)

# Nivå 3

werewolf = Monster(
    name="Werewolf",
    char="W",
    color=(128, 128, 128),
    stats=[50, 20, 25, 15, 50],
    move_chance=70,
)

arachnid = Monster(
    name="Arachnid",
    char="A",
    color=(72, 75, 98),
    stats=[30, 25, 30, 20, 50],
    move_chance=60,
)

harpy = Monster(
    name="Harpy",
    char="H",
    color=(252, 233, 3),
    stats=[40, 30, 40, 20, 50],
    move_chance=50,
)

# Nivå 4

mummy = Monster(
    name="Mummy",
    char="M",
    color=(237, 236, 231),
    stats=[50, 15, 5, 3, 10],
    move_chance=30,
)

vampire = Monster(
    name="Vampire",
    char="V",
    color=red,
    stats=[80, 30, 20, 16, 30],
    move_chance=80,
)

zombie = Monster(
    name="Zombie",
    char="Z",
    color=(0, 82, 33),
    stats=[60, 20, 5, 3, 20],
    move_chance=40,
)

# Nivå 5

death_knight = Monster(
    name="Death Knight",
    char="K",
    color=(99, 181, 33),
    stats=[150, 50, 20, 20, 20],
    move_chance=80,
)


lich = Monster(
    name="Lich",
    char="L",
    color=(227, 98, 47),
    stats=[200, 60, 50, 50, 50],
    move_chance=90,
)

demon = Monster(
    name="Demon",
    char="D",
    color=(255, 0, 0),
    stats=[225, 50, 70, 70, 70],
    move_chance=90,
)


level_1_monsters = [orc, goblin, troll]

level_2_monsters = [rock_elemental, basilisk, skeleton]

level_3_monsters = [werewolf, arachnid, harpy]

level_4_monsters = [vampire, mummy, zombie]

level_5_monsters = [death_knight, lich, demon]

all_monsters = [
    level_1_monsters,
    level_2_monsters,
    level_3_monsters,
    level_4_monsters,
    level_5_monsters,
]

all_monster_chars = [monster.char for monster in list(chain(*all_monsters))]


def generate_monsters(room, game_map) -> None:
    """Genererar en entity i ett givet rum"""

    x = random.randint(room.x1 + 1, room.x2 - 1)

    y = random.randint(room.y1 + 1, room.y2 - 1)

    if not game_map.entity_at_location(x, y):
        monster = random.choice(all_monsters[game_map.difficulty - 1])
        new_monster = Monster(
            name=monster.name,
            char=monster.char,
            color=monster.color,
            stats=monster.stats,
            x=x,
            y=y,
            move_chance=monster.move_chance,
        )
        game_map.entities.append(new_monster)
        room.type = "monster"
        return
    else:
        return


def generate_boss(room, game_map) -> None:  # Special funktion för att generera bossen
    x, y = room.center

    boss = Monster(
        name="Ancient Titan",
        x=x,
        y=y,
        char="B",
        color=red,
        difficulty=3,
        stats=[80, 80, 80, 80, 80],
    )
    game_map.entities.append(boss)
    room.type = "monster"

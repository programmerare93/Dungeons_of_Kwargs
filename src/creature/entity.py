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

    def move(self, dx: int, dy: int):
        """Ändrar x och y koordinaten på en entity med ett givet värde"""
        self.x += dx
        self.y += dy

    def render(self, console: Console, x: int, y: int):
        """Ritar ut en entity på en given konsol"""
        console.print(x=x, y=y, string=self.char, fg=self.color)


class Player(Entity):
    """Klass för att representera spelaren"""

    def __init__(
        self,
        char: str,
        color: Tuple[int, int, int],
        stats=[10, 10, 10, 10, 10],
        name: str = "Player",
    ):
        super().__init__(0, 0, "@", color, name)
        self.stats = stats
        self.update_stats()
        self.armor = obama_armor
        self.xp = 0
        self.xp_to_next_level = 100
        self.level = 1
        self.inventory = Inventory(items=list(chain(*all_items)))
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
        move_chance: int = 100,
    ):
        super().__init__(x, y, char, color, name)
        self.difficulty = difficulty  # Monstrets statistik kommer att bero på hur svårt den nuvarande nivån är
        self.max_hp = max_hp * self.difficulty
        self.hp = self.max_hp * self.difficulty
        self.strength = strength * self.difficulty
        self.agility = agility * self.difficulty
        self.intelligence = intelligence * self.difficulty
        self.perception = perception * self.difficulty
        self.move_chance = (
            move_chance  # Hur stor chans det är för att monstret ska röra sig
        )
        self.inventory = Inventory(  # Genererar ett inventory med items
            items=[
                random.choice(all_potions[self.difficulty - 1])
                for _ in range(random.randint(1, 3))
            ],
        )
        self.xp_value = (
            self.max_hp + self.strength + self.agility + self.intelligence
        )  # Hur mycket xp spelaren får när den dödar monstret
        self.armor = all_armor[self.difficulty - 1]
        self.used_items = (
            []
        )  # Lista med items som monstret använt och som fortfarande är aktiva

    def monster_pathfinding(self, player, game_map, engine):
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

    def choose_item(self):
        """Väljer ett item från inventoryt"""
        return random.choice(self.inventory.items)


class Chest(Entity):
    """Klass för att representera en kista, kommer att fungera som en container för items och ärver från entiteten så att vi enkelt kan ta bort den när den öppnas"""

    def __init__(self, x: int, y: int, name: str = "Chest", tier: int = 1):
        self.name = name
        self.hp = inf
        self.x = x
        self.y = y
        self.char = "C"
        self.color = light_blue
        self.closed = True
        self.tier = tier
        self.inventory = Inventory(
            items=[
                random.choice(
                    all_items[self.tier - 1]
                )  # Genererar ett inventory med items beror på vilken tier kistan är vilket beror på våningen
                for _ in range(random.randint(1, 3))
            ],
        )


def generate_monsters(room, game_map):
    """Genererar en entity i ett givet rum"""

    x = random.randint(room.x1 + 1, room.x2 - 1)

    y = random.randint(room.y1 + 1, room.y2 - 1)

    if not game_map.entity_at_location(x, y):
        if random.random() < 0.8:
            monster = Monster(
                name="Orc",
                x=x,
                y=y,
                char="O",
                color=light_green,
                difficulty=game_map.difficulty,
                max_hp=16,
                strength=10,
                agility=5,
                perception=5,
                intelligence=1,
                move_chance=40,
            )
        else:
            monster = Monster(
                name="Troll",
                x=x,
                y=y,
                char="T",
                color=blue,
                difficulty=game_map.difficulty,
                max_hp=30,
                strength=10,
                perception=5,
                agility=3,
                intelligence=3,
                move_chance=60,
            )
        game_map.entities.append(monster)
        room.type = "monster"
    else:  # Om det redan finns en entity på den platsen, kör funktionen igen
        generate_monsters(room, game_map)


def generate_boss(room, game_map):  # Special funktion för att generera bossen
    x, y = room.center

    boss = Monster(
        name="Ancient Titan",
        x=x,
        y=y,
        char="B",
        color=red,
        difficulty=game_map.difficulty + 2,
        max_hp=80,
        strength=10,
        perception=4,
        dexterity=2,
        intelligence=2,
    )
    game_map.entities.append(boss)
    room.type = "monster"

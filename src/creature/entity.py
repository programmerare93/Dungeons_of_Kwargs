from typing import Tuple
from tcod import Console
import random

from stage.floor import Floor
from actions.actions import MovementAction
from creature.items import Inventory, potions


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
        self.inventory = Inventory(self)

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

    def take_damage(self, amount: int):
        self.hp -= amount


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
        self.internal_tick = 0

    def monster_pathfinding(self, player, game_map, engine):
        """Monster pathfinding"""
        print("tick")
        tile_x, tile_y = (
            game_map.pathfinding(self.x, self.y, player.x, player.y)[0][0],
            game_map.pathfinding(self.x, self.y, player.x, player.y)[0][1],
        )

        action = MovementAction(tile_x - self.x, tile_y - self.y)
        action.perform(engine, self)
        self.internal_tick += 1

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


def generate_monsters(room, game_map):
    """Genererar en entity i ett given rum"""

    x = random.randint(room.x1 + 1, room.x2 - 1)

    y = random.randint(room.y1 + 1, room.y2 - 1)

    if not game_map.entity_at_location(x, y):
        if random.random() < 0.8:
            monster = Monster(x, y, "O", (0, 255, 120), 10, 10, 1, 5, 1, 1)
        else:
            monster = Monster(
                x,
                y,
                "T",
                (0, 0, 255),
                max_hp=16,
                hp=16,
                strength=3,
                perception=5,
                dexterity=3,
                intelligence=3,
            )
        game_map.entities.add(monster)
        room.type = "monster"

from typing import Tuple, List

from stage.tile_types import Tile


class Inventory:
    def __init__(self, owner, items=None):
        if items is None:
            self.items: List[Item] = []
        else:
            self.items: List[Item] = items
        self.owner = owner

    def add(self, item):
        self.items.append(item)
        pass

    def get_items(self):
        return self.items


class Item(Tile):
    """En subklass av tile klassen som ska representera föremål"""
    def __init__(self, item_type: str, char: str, color: Tuple[int, int, int]):
        super().__init__(
            walkable=True,
            visible=False,
            transparent=True,
            seen=False,
            color=color,
            char=char
        )
        self.type = item_type
        self.owner = None


class StatItem(Item):
    def __init__(self, item_type: str, char: str, color: Tuple[int, int, int], amplitude: int, duration: int):
        super().__init__(item_type, char, color)
        self.amplitude = amplitude
        self.duration = duration

    def use(self):
        if self.type == "health_potion":
            self.owner.hp += self.amplitude
            self.owner.inventory.items.remove(self)
            return self.duration
        elif self.type == "strength_potion":
            self.owner.strength += self.amplitude
            self.owner.inventory.items.remove(self)
            return self.duration
        elif self.type == "dexterity_potion":
            self.owner.dexterity += self.amplitude
            self.owner.inventory.items.remove(self)
            return self.duration
        elif self.type == "perception_potion":
            self.owner.perception += self.amplitude
            self.owner.inventory.items.remove(self)
            return self.duration


small_healing_potion = StatItem("health_potion", 'P', (0, 255, 0), amplitude=10, duration=10)

medium_healing_potion = StatItem("health_potion", 'P', (0, 255, 0), amplitude=20, duration=20)

large_healing_potion = StatItem("health_potion", 'P', (0, 255, 0), amplitude=30, duration=30)

small_strength_potion = StatItem("strength_potion", 'P', (0, 255, 0), amplitude=2, duration=10)

medium_strength_potion = StatItem("strength_potion", 'P', (0, 255, 0), amplitude=4, duration=20)

large_strength_potion = StatItem("strength_potion", 'P', (0, 255, 0), amplitude=6, duration=30)

small_dexterity_potion = StatItem("dexterity_potion", 'P', (0, 255, 0), amplitude=2, duration=10)

medium_dexterity_potion = StatItem("dexterity_potion", 'P', (0, 255, 0), amplitude=4, duration=20)

large_dexterity_potion = StatItem("dexterity_potion", 'P', (0, 255, 0), amplitude=6, duration=30)

small_perception_potion = StatItem("perception_potion", 'P', (0, 255, 0), amplitude=2, duration=10)

medium_perception_potion = StatItem("perception_potion", 'P', (0, 255, 0), amplitude=4, duration=20)

large_perception_potion = StatItem("perception_potion", 'P', (0, 255, 0), amplitude=6, duration=30)

potions = [small_healing_potion,
           medium_healing_potion,
           large_healing_potion,
           small_strength_potion,
           medium_strength_potion,
           large_strength_potion,
           small_dexterity_potion,
           medium_dexterity_potion,
           large_dexterity_potion,
           small_perception_potion,
           medium_perception_potion,
           large_perception_potion
           ]

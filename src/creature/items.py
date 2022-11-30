from math import inf


class Inventory:
    def __init__(self, owner, items):
        self.owner = owner
        self.items = []

    def add_item(self, item):
        self.items.append(item)


class Item:
    def __init__(self, type):
        self.type = type
        self.owner = None


class StatItem(Item):
    def __init__(self, type, amplitude, duration):
        self.type = type
        self.amplitude = amplitude
        self.duration = inf
        self.owner = None
        self.duration = duration

    def use(self, engine):
        if self.type == "health potion":
            self.owner.hp += self.amplitude
            self.owner.inventory.items.remove(self)

        elif self.type == "strength potion":
            self.owner.strength += self.amplitude
            self.owner.inventory.items.remove(self)

        elif self.type == "dexterity potion":
            self.owner.dexterity += self.amplitude
            self.owner.inventory.items.remove(self)

        elif self.type == "perception potion":
            self.owner.perception += self.amplitude
            self.owner.inventory.items.remove(self)

        engine.message_log.add_message("You used a {}!".format(self.type))
        return self.duration


small_healing_potion = StatItem("health potion", 10, duration=10)

medium_healing_potion = StatItem("health potion", 20, duration=20)

large_healing_potion = StatItem("health potion", 30, duration=30)

small_strength_potion = StatItem("strength potion", 2, duration=10)

medium_strength_potion = StatItem("strength potion", 4, duration=20)

large_strength_potion = StatItem("strength potion", 6, duration=30)

small_dexterity_potion = StatItem("dexterity potion", 2, duration=10)

medium_dexterity_potion = StatItem("dexterity potion", 4, duration=20)

large_dexterity_potion = StatItem("dexterity potion", 6, duration=30)

small_perception_potion = StatItem("perception potion", 2, duration=10)

medium_perception_potion = StatItem("perception potion", 4, duration=20)

large_perception_potion = StatItem("perception potion", 6, duration=30)

all_items = [
    small_healing_potion,
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
    large_perception_potion,
]

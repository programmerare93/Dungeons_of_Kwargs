from math import inf


class Inventory:
    def __init__(self, owner=None, items=[]):
        self.items = items
        self.owner = owner

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
        self.activated_tick = 0

    def use(self, engine, entity):
        if self.type.endswith("health potion"):
            entity.hp += self.amplitude
            entity.inventory.items.remove(self)

        elif self.type.endswith("strength potion"):
            entity.strength += self.amplitude
            entity.inventory.items.remove(self)

        elif self.type.endswith("dexterity potion"):
            entity.dexterity += self.amplitude
            entity.inventory.items.remove(self)

        elif self.type.endswith("perception potion"):
            entity.perception += self.amplitude
            entity.inventory.items.remove(self)

        engine.message_log.add_message("You used a {}!".format(self.type))
        self.activated_tick = engine.tick
        return

    def remove_effect(self, entity):
        if self.type.endswith("health potion"):
            entity.hp -= self.amplitude

        elif self.type.endswith("strength potion"):
            entity.strength -= self.amplitude

        elif self.type.endswith("dexterity potion"):
            entity.dexterity -= self.amplitude

        elif self.type.endswith("perception potion"):
            entity.perception -= self.amplitude
        return


small_healing_potion = StatItem("small health potion", 10, duration=10)

medium_healing_potion = StatItem("medium health potion", 20, duration=20)

large_healing_potion = StatItem("large health potion", 30, duration=30)

small_strength_potion = StatItem("small strength potion", 2, duration=10)

medium_strength_potion = StatItem("medium strength potion", 4, duration=20)

large_strength_potion = StatItem("large strength potion", 6, duration=30)

small_dexterity_potion = StatItem("small dexterity potion", 2, duration=10)

medium_dexterity_potion = StatItem("medium dexterity potion", 4, duration=20)

large_dexterity_potion = StatItem("large dexterity potion", 6, duration=30)

small_perception_potion = StatItem("small perception potion", 2, duration=3)

medium_perception_potion = StatItem("medium perception potion", 4, duration=20)

large_perception_potion = StatItem("large perception potion", 6, duration=30)

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

from math import inf


class Inventory:
    def __init__(self, owner, items):
        self.owner = owner
        self.items = []

    def add(self, item):
        self.items.append(item)
        pass


class Item:
    def __init__(self, type):
        self.type = type
        self.owner = None


class StatItem(Item):
    def __init__(self, type, amplitude, duration):
        super().__init__(type)
        self.amplitude = amplitude
        self.duration = inf

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


small_healing_potion = StatItem("health_potion", amplitude=10, duration=10)

medium_healing_potion = StatItem("health_potion", amplitude=20, duration=20)

large_healing_potion = StatItem("health_potion", amplitude=30, duration=30)

small_strength_potion = StatItem("strength_potion", amplitude=2, duration=10)

medium_strength_potion = StatItem("strength_potion", amplitude=4, duration=20)

large_strength_potion = StatItem("strength_potion", amplitude=6, duration=30)

small_dexterity_potion = StatItem("dexterity_potion", amplitude=2, duration=10)

medium_dexterity_potion = StatItem("dexterity_potion", amplitude=4, duration=20)

large_dexterity_potion = StatItem("dexterity_potion", amplitude=6, duration=30)

small_perception_potion = StatItem("perception_potion", amplitude=2, duration=10)

medium_perception_potion = StatItem("perception_potion", amplitude=4, duration=20)

large_perception_potion = StatItem("perception_potion", amplitude=6, duration=30)

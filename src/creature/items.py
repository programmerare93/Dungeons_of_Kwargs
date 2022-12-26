from math import inf


class Inventory:
    def __init__(self, owner=None, items=[]):
        self.items = items
        self.owner = owner

    def add_item(self, item):
        self.items.append(item)


class StatItem:
    def __init__(self, type, amplitude, duration=inf):
        self.type = type
        self.amplitude = amplitude
        self.owner = None
        self.duration = duration
        self.activated_tick = 0

    def use(self, engine, entity):
        if self.type.endswith("health potion") and entity.hp < entity.max_hp:
            hp_diff = entity.max_hp - entity.hp
            if hp_diff < self.amplitude:
                entity.hp = entity.max_hp
            else:
                entity.hp += self.amplitude
            entity.inventory.items.remove(self)
        elif self.type.endswith("health potion") and entity.hp == entity.max_hp:
            engine.message_log.add_message("You are already at full health!")
            return

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
            return

        elif self.type.endswith("strength potion"):
            entity.strength -= self.amplitude

        elif self.type.endswith("dexterity potion"):
            entity.dexterity -= self.amplitude

        elif self.type.endswith("perception potion"):
            entity.perception -= self.amplitude
        return


small_healing_potion = StatItem("small health potion", amplitude=20)

medium_healing_potion = StatItem("medium health potion", amplitude=30)

large_healing_potion = StatItem("large health potion", amplitude=40)

very_large_healing_potion = StatItem("very large health potion", amplitude=50)

giant_healing_potion = StatItem("giant health potion", amplitude=60)

small_strength_potion = StatItem("small strength potion", 2, duration=10)

medium_strength_potion = StatItem("medium strength potion", 4, duration=20)

large_strength_potion = StatItem("large strength potion", 6, duration=30)

very_large_strength_potion = StatItem("very large strength potion", 10, duration=30)

giant_strength_potion = StatItem("giant strength potion", 15, duration=30)

small_dexterity_potion = StatItem("small dexterity potion", 2, duration=10)

medium_dexterity_potion = StatItem("medium dexterity potion", 4, duration=20)

large_dexterity_potion = StatItem("large dexterity potion", 6, duration=30)

very_large_dexterity_potion = StatItem("very large dexterity potion", 10, duration=30)

giant_dexterity_potion = StatItem("giant dexterity potion", 15, duration=30)

small_perception_potion = StatItem("small perception potion", 2, duration=3)

medium_perception_potion = StatItem("medium perception potion", 4, duration=20)

large_perception_potion = StatItem("large perception potion", 6, duration=30)

very_large_perception_potion = StatItem("very large perception potion", 10, duration=30)

giant_perception_potion = StatItem("giant perception potion", 15, duration=30)


class Armor:
    def __init__(self, type, defense):
        self.type = type
        self.defense = defense


leather_armor = Armor("leather armor", 5)
iron_armor = Armor("iron armor", 10)
diamond_armor = Armor("diamond armor", 20)
netherite_armor = Armor("netherite armor", 30)
obama_armor = Armor("obama armor", 50)


tier_1_items = [
    leather_armor,
    small_dexterity_potion,
    small_healing_potion,
    small_perception_potion,
    small_strength_potion,
]

tier_2_items = [
    iron_armor,
    medium_dexterity_potion,
    medium_healing_potion,
    medium_perception_potion,
    medium_strength_potion,
]

tier_3_items = [
    diamond_armor,
    large_dexterity_potion,
    large_healing_potion,
    large_perception_potion,
    large_strength_potion,
]

tier_4_items = [
    netherite_armor,
    very_large_dexterity_potion,
    very_large_healing_potion,
    very_large_perception_potion,
    very_large_strength_potion,
]

tier_5_items = [
    obama_armor,
    giant_dexterity_potion,
    giant_healing_potion,
    giant_perception_potion,
    giant_strength_potion,
]

all_items = [
    tier_1_items,
    tier_2_items,
    tier_3_items,
    tier_4_items,
    tier_5_items,
]

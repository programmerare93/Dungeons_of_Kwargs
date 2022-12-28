from math import inf


class Inventory:
    def __init__(self, owner=None, items=[]):
        self.items = items
        self.owner = owner

    def add_item(self, item):
        self.items.append(item)


class StatItem:
    def __init__(self, name, type, amplitude, duration=inf):
        self.name = name
        self.type = type
        self.amplitude = amplitude
        self.owner = None
        self.duration = duration
        self.activated_tick = 0

    def use(self, engine, entity):
        potion_dict = {
            "strength potion": entity.strength,
            "dexterity potion": entity.dexterity,
            "perception potion": entity.perception,
        }
        potion_dict[self.type] += self.amplitude

        entity.inventory.items.remove(self)
        engine.message_log.add_message("You used a {}!".format(self.name))
        self.activated_tick = engine.tick
        entity.used_items.append(self)
        return

    def remove_effect(self, entity):
        potion_dict = {
            "strength potion": entity.strength,
            "dexterity potion": entity.dexterity,
            "perception potion": entity.perception,
        }
        potion_dict[self.type] -= self.amplitude
        entity.used_items.remove(self)
        return


class HealthPotion:
    def __init__(self, name, type, amplitude):
        self.name = name
        self.amplitude = amplitude
        self.type = type

    def use(self, engine, entity):
        if entity.hp == entity.max_hp:
            engine.message_log.add_message("You are already at full health!")
            return
        hp_diff = entity.max_hp - entity.hp
        if hp_diff < self.amplitude:
            entity.hp = entity.max_hp
        else:
            entity.hp += self.amplitude
        return


small_healing_potion = HealthPotion(
    name="small health potion", amplitude=20, type="health potion"
)

medium_healing_potion = HealthPotion(
    name="medium health potion", amplitude=30, type="health potion"
)

large_healing_potion = HealthPotion(
    name="large health potion", amplitude=40, type="health potion"
)

very_large_healing_potion = HealthPotion(
    name="very large health potion", amplitude=50, type="health potion"
)

giant_healing_potion = HealthPotion(
    name="giant health potion", amplitude=60, type="health potion"
)

small_strength_potion = StatItem(
    name="small strength potion", amplitude=2, duration=10, type="strength potion"
)

medium_strength_potion = StatItem(
    name="medium strength potion", amplitude=4, duration=20, type="strength potion"
)

large_strength_potion = StatItem(
    name="large strength potion", amplitude=6, duration=30, type="strength potion"
)

very_large_strength_potion = StatItem(
    name="very large strength potion", amplitude=10, duration=30, type="strength potion"
)

giant_strength_potion = StatItem(
    name="giant strength potion", amplitude=15, duration=30, type="strength potion"
)

small_dexterity_potion = StatItem(
    name="small dexterity potion", amplitude=2, duration=10, type="dexterity potion"
)

medium_dexterity_potion = StatItem(
    name="medium dexterity potion", amplitude=4, duration=20, type="dexterity potion"
)

large_dexterity_potion = StatItem(
    name="large dexterity potion", amplitude=6, duration=30, type="dexterity potion"
)

very_large_dexterity_potion = StatItem(
    name="very large dexterity potion",
    amplitude=10,
    duration=30,
    type="dexterity potion",
)

giant_dexterity_potion = StatItem(
    name="giant dexterity potion", amplitude=15, duration=30, type="dexterity potion"
)

small_perception_potion = StatItem(
    name="small perception potion", amplitude=2, duration=3, type="perception potion"
)

medium_perception_potion = StatItem(
    name="medium perception potion", amplitude=4, duration=20, type="perception potion"
)

large_perception_potion = StatItem(
    name="large perception potion", amplitude=6, duration=30, type="perception potion"
)

very_large_perception_potion = StatItem(
    name="very large perception potion",
    amplitude=10,
    duration=30,
    type="perception potion",
)

giant_perception_potion = StatItem(
    name="giant perception potion", amplitude=15, duration=30, type="perception potion"
)


class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

    def use(self, engine, entity):
        entity.inventory.items.remove(self)
        entity.inventory.items.append(entity.armor)
        entity.armor = self
        engine.message_log.add_message("You equipped the {}!".format(self.name))
        return


leather_armor = Armor("leather armor", 5)
iron_armor = Armor("iron armor", 10)
diamond_armor = Armor("diamond armor", 20)
obsidian_armor = Armor("obsidian armor", 30)
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
    obsidian_armor,
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

from __future__ import annotations

import random

from typing import TYPE_CHECKING

import stage.tile_types as tile_types
from actions.soundhandler import SoundHandler

# Falskt på 'runtime'
if TYPE_CHECKING:
    from engine.engine import Engine
    from creature.entity import Entity, Chest

sound_handler = SoundHandler()


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Metod som kommer att utföra en handling för en entitet,
        måste implementeras för individuella subklasser"""

        # Kommer att misslyckas om man inte modifierat metoden
        raise NotImplementedError()


class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            # Koordinaten är utanför kartan
            return None

        if engine.player_activated_trap(dest_x, dest_y):
            difficulty = engine.game_map.tiles[dest_x, dest_y].difficulty
            dexterity = engine.player.dexterity
            if (
                difficulty < dexterity
                and not engine.game_map.tiles[dest_x, dest_y].hasBeenActivated
            ):
                engine.message_log.add_message(
                    "You stepped on a trap. You avoided it!", (0, 255, 0)
                )
            elif (
                difficulty > dexterity
                and not engine.game_map.tiles[dest_x, dest_y].hasBeenActivated
            ):
                engine.message_log.add_message(
                    f"You stepped on a trap. You took {difficulty - dexterity} damage!",
                    (255, 0, 0),
                )
                engine.player.hp -= difficulty - dexterity
            else:
                pass
            engine.game_map.tiles[dest_x, dest_y].hasBeenActivated = True

        if not engine.game_map.get_tile(dest_x, dest_y).walkable:
            return None

        if entity.char != "@" and engine.game_map.entity_at_location(dest_x, dest_y):
            target = list(engine.game_map.entity_at_location(dest_x, dest_y))[0]
            if target.char != "@":
                return "tried to attack a monster"
            if entity.perception + random.randint(
                    1, 20
            ) > target.dexterity + random.randint(1, 20):
                damage = entity.strength + random.randint(
                    -entity.strength // 4, entity.strength // 4
                )
                target.hp -= damage
                engine.message_log.add_message(
                    f"{target.name} took {damage} damage!", target.color
                )
                engine.render(
                    console=engine.window.console, context=engine.window.context
                )
                # sound_handler.player_hit()
                return "player_hit"
            else:
                engine.message_log.add_message(
                    f"{target.name} dodged {entity.name}'s attack!", target.color
                )
                engine.render(
                    console=engine.window.console, context=engine.window.context
                )
                # sound_handler.attack_dodged()
                return "miss"

        elif (
                engine.game_map.entity_at_location(dest_x, dest_y)
                and list(engine.game_map.entity_at_location(dest_x, dest_y))[0].char == "C"
        ):
            return None
        elif (
                engine.game_map.entity_at_location(dest_x, dest_y)
                and engine.player_can_attack == True
        ):
            target = list(engine.game_map.entity_at_location(dest_x, dest_y))[0]
            if entity.perception + random.randint(
                    1, 20
            ) > target.dexterity + random.randint(1, 20):
                damage = engine.player.strength + random.randint(
                    -engine.player.strength // 4, engine.player.strength // 4
                )
                target.hp -= damage
                engine.message_log.add_message(f"{target.name} took {damage} damage!")
                engine.render(
                    console=engine.window.console, context=engine.window.context
                )
                # sound_handler.sword_sound()
                engine.player_can_attack = False
                return "hit"
            else:
                engine.message_log.add_message(f"{target.name} dodged your attack!")
                engine.render(
                    console=engine.window.console, context=engine.window.context
                )
                # sound_handler.attack_dodged()
                engine.player_can_attack = False
                return "miss"
        elif (
            engine.game_map.entity_at_location(dest_x, dest_y)
            and not engine.player_can_attack == True
        ):
            return None

        entity.move(self.dx, self.dy)

        return "moved"


class GoDown(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        if engine.game_map.tiles[entity.x, entity.y] == tile_types.stair_case:
            engine.update_game_map()


class HealingAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        if entity.hp < entity.max_hp:
            entity.hp += 10
            engine.message_log.add_message(f"{entity.name} healed 10 hp!")
            return "healed"
        else:
            engine.message_log.add_message(f"{entity.name} is at full health!")


class UseItem(Action):
    def __init__(self) -> None:
        super().__init__()
        self.item = None

    def perform(self, engine: Engine, entity: Entity) -> None:
        self.item = entity.inventory.items[0]

        self.item.use(engine, entity)
        entity.used_items.append(self.item)


class OpenChest(Action):
    def __init__(self) -> None:
        super().__init__()

    def perform(self, engine: Engine, entity: Entity) -> None:
        for monster in engine.game_map.entities:
            if (
                    monster.char == "C"
                    and engine.game_map.calculate_distance(
                entity.x, entity.y, monster.x, monster.y
            )
                    == 1
            ):
                chest = monster
                engine.message_log.add_message("You opened a chest!")
                engine.player.inventory.items.extend(chest.inventory.items)
                engine.message_log.add_message(
                    f"You Received {tuple([item.type for item in chest.inventory.items])}"
                )
                engine.game_map.entities.remove(chest)
                engine.render(
                    console=engine.window.console, context=engine.window.context
                )
                return "opened_chest"

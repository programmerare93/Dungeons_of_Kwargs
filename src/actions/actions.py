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
    def use(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MovementAction:
    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        if not engine.player_can_move:
            return None
        if entity.char == "@" and engine.player_can_attack in (False, "None"):
            return None

        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = (
            engine.game_map.entity_at_location(dest_x, dest_y)[0]
            if engine.game_map.entity_at_location(dest_x, dest_y)
            else None
        )

        if not engine.game_map.in_bounds(dest_x, dest_y):
            # Koordinaten är utanför kartan
            return None

        if not engine.game_map.get_tile(dest_x, dest_y).walkable:
            return None

        """Tittar om spelaren har gått på en fälla"""
        if engine.player_activated_trap(dest_x, dest_y):
            difficulty = engine.game_map.tiles[dest_x, dest_y].difficulty
            agility = engine.player.agility
            if (
                difficulty < agility
                and not engine.game_map.tiles[dest_x, dest_y].hasBeenActivated
            ):
                exp_gain = difficulty * 2
                engine.message_log.add_message(
                    f"You stepped on a trap. You avoided it! You gain {exp_gain} xp!",
                    (0, 255, 0),
                )
                engine.player.xp += exp_gain
            elif (
                difficulty > agility
                and not engine.game_map.tiles[dest_x, dest_y].hasBeenActivated
            ):
                engine.message_log.add_message(
                    f"You stepped on a trap. You took {difficulty - agility} damage!",
                    (255, 0, 0),
                )
                engine.player.hp -= difficulty - agility
            engine.game_map.tiles[dest_x, dest_y].hasBeenActivated = True

        """Tittar vad som händer med entitetens attack"""
        if target:
            if target.char == "C":
                return None
            if entity.char == "@":
                engine.player_can_attack = False
            if entity.perception + random.randint(
                1, 20
            ) > target.agility + random.randint(1, 20):
                damage = (
                    entity.strength
                    + random.randint(-entity.strength // 4, entity.strength // 4)
                    - target.armor.defense
                )
                if damage <= 0:
                    engine.message_log.add_message(
                        f"{entity.name}'s attack couldn't pierce {target.name}'s armor!",
                        target.color,
                    )
                    return "armor blocked"
                else:
                    target.hp -= damage
                    engine.message_log.add_message(
                        f"{target.name} took {damage} damage!", target.color
                    )
                    engine.render(
                        console=engine.window.console, context=engine.window.context
                    )
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

        entity.move(self.dx, self.dy)

        return "moved"


class GoDown:
    def perform(self, engine: Engine, entity: Entity) -> None:
        if engine.game_map.tiles[entity.x, entity.y] == tile_types.stair_case:
            engine.update_game_map()


class HealingAction:
    def perform(self, engine: Engine, entity: Entity) -> None:
        if entity.hp < entity.max_hp:
            entity.hp += 10
            engine.message_log.add_message(f"{entity.name} healed 10 hp!")
            return "healed"
        else:
            engine.message_log.add_message(f"{entity.name} is at full health!")


class OpenChest:
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
                    f"You Received {tuple([item.name for item in chest.inventory.items])}",
                    (0, 255, 255),
                )
                engine.game_map.entities.remove(chest)
                engine.render(
                    console=engine.window.console, context=engine.window.context
                )
                return "opened_chest"

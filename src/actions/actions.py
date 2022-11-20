from __future__ import annotations

import random

from typing import TYPE_CHECKING

import stage.tile_types as tile_types
import random

# Falskt på 'runtime'
if TYPE_CHECKING:
    from engine.engine import Engine
    from creature.entity import Entity


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

        if not engine.game_map.get_tile(dest_x, dest_y).walkable:
            return None

        if entity.char != "@" and engine.game_map.entity_at_location(dest_x, dest_y):
            target = list(engine.game_map.entity_at_location(dest_x, dest_y))[0]
            if entity.perception + random.randint(
                1, 20
            ) > target.dexterity + random.randint(1, 20):
                target.hp -= entity.strength
                engine.message_log.add_message(
                    f"{target.char} took {entity.strength} damage!"
                )
                return "hit"
            else:
                engine.message_log.add_message(
                    f"{target.char} dodged {entity.char}'s attack!"
                )
                return "miss"

        if (
            engine.game_map.entity_at_location(dest_x, dest_y)
            and engine.player_can_attack == True
        ):
            target = list(engine.game_map.entity_at_location(dest_x, dest_y))[0]
            if entity.perception + random.randint(
                1, 20
            ) > target.dexterity + random.randint(1, 20):
                target.hp -= engine.player.strength
                engine.message_log.add_message(
                    f"{target.char} took {entity.strength} damage!"
                )
                engine.player_can_attack = False
                return "hit"
            else:
                engine.message_log.add_message(f"{target.char} dodged your attack!")
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

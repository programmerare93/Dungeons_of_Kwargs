from __future__ import annotations

from typing import TYPE_CHECKING

import random

# Falskt på 'runtime'
if TYPE_CHECKING:
    from src.engine.engine import Engine
    from src.creature.entity import Entity


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

        if (
            engine.game_map.entity_at_location(dest_x, dest_y)
            and engine.player_can_attack == True
        ):
            target = list(engine.game_map.entity_at_location(dest_x, dest_y))[0]
            if entity.perception + random.randint(
                1, 20
            ) > target.perception + random.randint(1, 20):
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
            engine.message_log.add_message("Your attack is on cooldown!")
            return None

        entity.move(self.dx, self.dy)

        return "moved"

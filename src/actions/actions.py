from __future__ import annotations

import random
import asyncio

from typing import TYPE_CHECKING

import stage.tile_types as tile_types
from actions.soundhandler import SoundPlayer
from window.color import *

# Falskt på 'runtime'
if TYPE_CHECKING:
    from engine.engine import Engine
    from creature.entity import Entity

player = SoundPlayer()
# all_monster_chars = (
#     "O",
#     "G",
#     "T",
#     "S",
#     "B",
#     "R",
#     "W",
#     "A",
#     "H",
#     "M",
#     "V",
#     "Z",
#     "K",
#     "L",
# )


class Action:
    """Bara en abstrakt klass för att hålla reda på vad som är en action, vilket krävs i input_handlers.py"""

    def use(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MovementAction:
    """En action som flyttar spelaren eller en fiende, behandlar även fällor och attacker"""

    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        # Först tittar vi om spelaren kan flytta eller inte
        if not engine.player_can_move:
            return None
        # Sen tittar vi om spelaren kan attackera eller inte
        if entity.char == "@" and engine.player_can_attack in (False, "None"):
            return None

        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        # Kollar efter en entitet på destinationen
        target = (
            engine.game_map.entity_at_location(dest_x, dest_y)[0]
            if engine.game_map.entity_at_location(dest_x, dest_y)
            else None
        )

        if not engine.game_map.in_bounds(dest_x, dest_y):
            # Koordinaten är utanför kartan
            return None

        if not engine.game_map.get_tile(
            dest_x, dest_y
        ).walkable:  # Ifall det inte går att gå på den tilen
            return None

        """Tittar om spelaren har gått på en fälla"""
        if engine.player_activated_trap(dest_x, dest_y):
            difficulty = engine.game_map.tiles[dest_x, dest_y].difficulty
            agility = engine.player.agility
            if (
                difficulty
                < agility  # Ser till att spelaren inte tar skada om spelaren har mer agility än fällans svårighetsgrad
                and not engine.game_map.tiles[dest_x, dest_y].hasBeenActivated
            ):
                exp_gain = difficulty * 2
                engine.message_log.add_message(
                    f"You stepped on a trap. You avoided it! You gain {exp_gain} xp!",
                    green,
                )
                engine.player.xp += (
                    exp_gain  # Ger spelaren xp för att ha undvikit fällan
                )
            elif (
                difficulty > agility
                and not engine.game_map.tiles[dest_x, dest_y].hasBeenActivated
            ):
                engine.message_log.add_message(
                    f"You stepped on a trap. You took {difficulty - agility} damage!",
                    red,
                )
                engine.player.hp -= difficulty - agility
            engine.game_map.tiles[
                dest_x, dest_y
            ].hasBeenActivated = True  # Ser till att fällan inte kan aktiveras igen

        """Tittar vad som händer med entitetens attack"""
        if target:  # Ser till att det finns en entitet på destinationen
            if (
                target.char == "C"
            ):  # Kontrollerar om det är en kista och ifall det är det så händer inget
                return None
            if (
                entity.char == "@"
            ):  # Ifall det är spelaren som attackerar så sätts engine.player_can_attack till False, så att spelaren inte kan attackera igen på en sekund
                engine.player_can_attack = False
            if entity.char != "@" and target.char != "@":
                return None
            if entity.perception + random.randint(
                1, 20
            ) > target.agility + random.randint(
                1, 20
            ):  # Tittar om spelaren eller fienden träffar, beror på agility och perception
                damage = (
                    entity.strength
                    + random.randint(
                        -entity.strength // 4, entity.strength // 4
                    )  # Ökar eller minskar skadan lite slumpmässigt
                    - target.armor.defense  # Tar bort fiendens försvar från skadan
                )
                if damage <= 0:  # Om rustningen tog bort all skada
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
                return "miss"

        entity.move(
            self.dx, self.dy
        )  # Ifall ingenting av det ovan var sant så flyttar entiteten

        return "moved"


class GoDown:
    """En action som går ner i trapporna"""

    def perform(self, engine: Engine, entity: Entity) -> None:
        if engine.game_map.tiles[entity.x, entity.y] == tile_types.stair_case:
            engine.update_game_map()


class OpenChest:
    """En action som öppnar en kista"""

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
            ):  # Om spelaren är 1 tile från en kista
                chest = monster
                engine.message_log.add_message("You opened a chest!")
                engine.player.items.extend(
                    chest.items
                )  # Överför alla items från kistan till spelarens inventory
                engine.message_log.add_message(
                    f"You Received {tuple([item.name for item in chest.items])}",
                    light_blue,
                )
                engine.game_map.entities.remove(chest)  # Tar bort kistan från kartan
                engine.render(
                    console=engine.window.console, context=engine.window.context
                )
                return "opened_chest"

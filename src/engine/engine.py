from typing import Set, Iterable, Any
import time

import tcod.constants
from tcod import Console
from tcod.context import Context
from tcod.map import compute_fov

from actions.input_handlers import EventHandler
from creature.entity import Entity, Player, Monster
from stage.game_map import GameMap
from stage.tile_types import *
from stage.procgen import Generator
from window.render_functions import render_bar
from window.message_log import MessageLog
from window import color


class Engine:
    """Klassen för spel motorn, samlar all funktionalitet i metoder"""

    def __init__(
        self,
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
        generator: Generator,
        player_can_attack: bool = True,
        player_attack_cool_down: int = 0,
    ):
        self.event_handler = event_handler
        self.game_map = game_map
        self.message_log = MessageLog()
        self.player = player
        self.generator = generator
        self.tick = 0
        self.monster_tick = 0
        self.player_can_attack = player_can_attack
        self.player_attack_cool_down = player_attack_cool_down
        self.update_fov()

    def update_game_map(self):
        self.generator.generate_dungeon()
        self.game_map = self.generator.get_dungeon()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            if action.perform(self, self.player) != None:
                self.tick += 1
                self.update_fov()

    def handle_enemy_AI(self):
        if self.monster_tick + 1 == self.tick:  # Då får monster göra sitt
            for monster in self.game_map.entities:
                if (
                    monster.char != "@"
                    and self.game_map.calculateDistance(
                        monster.x, monster.y, self.player.x, self.player.y
                    )
                    <= monster.perception
                ):
                    print("Monster is in range")
                    monster.monster_pathfinding(self.player, self.game_map, self)
                    self.monster_tick += 1
                elif monster.char != "@":
                    print("Monster is not in range")
                    self.monster_tick += 1

    def can_player_attack(self):
        if self.player_can_attack == False:
            self.player_attack_cool_down = time.time()
            self.player_can_attack = "None"

        if time.time() - self.player_attack_cool_down >= 1:
            self.player_can_attack = True

    def update_fov(self) -> None:
        for (x, row) in enumerate(self.game_map.tiles):
            for (y, value) in enumerate(row):
                if self.game_map.get_tile(x, y).transparent:
                    self.game_map.transparent_tiles[x, y] = True

        self.game_map.visible[:] = compute_fov(
            transparency=self.game_map.transparent_tiles,
            pov=(self.player.x, self.player.y),
            radius=self.player.perception,
            algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST,
        )

    def check_entities(self):
        for entity in self.game_map.entities:
            if entity.hp <= 0:
                self.game_map.entities.remove(entity)
                self.message_log.add_message(f"{entity.char} died!", color.death_text)
                return

        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        render_bar(
            console=console,
            current_value=self.player.hp,
            maximum_value=self.player.max_hp,
            total_width=20,
        )
        self.message_log.render(console=console, x=23, y=62, width=40, height=6)
        context.present(console)

        console.clear()

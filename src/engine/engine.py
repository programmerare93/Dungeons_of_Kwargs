from typing import Set, Iterable, Any
import time
import winsound

import tcod.constants
from tcod import Console
from tcod.context import Context
from tcod.map import compute_fov

import stage.tile_types as tile_types

from actions.input_handlers import *
from actions.soundhandler import SoundHandler
from creature.entity import Entity, Player, Monster
from stage.game_map import GameMap
from stage.procgen import Generator
from stage.floor import Floor
from window.render_functions import render_bar
from window.message_log import MessageLog
from window import color, window
from window.window import Window


class Engine:
    """Klassen för spel motorn, samlar all funktionalitet i metoder"""

    def __init__(
        self,
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
        floor: Floor,
        generator: Generator,
        player_can_attack: bool = True,
        player_can_move: bool = False,
        player_attack_cool_down: int = 0,
        window: Window = None,
    ):
        self.window = window
        self.event_handler = EventHandler()
        self.game_map = game_map
        self.inventory_open = False
        self.player_can_move = player_can_move
        self.message_log = MessageLog()
        self.player = player
        self.floor = floor
        self.generator = generator
        self.tick = 0
        self.monster_tick = 0
        self.player_can_attack = player_can_attack
        self.player_attack_cool_down = player_attack_cool_down
        self.update_game_map()
        self.update_fov()
        self.sound_handler = SoundHandler()
        self.window = window
        self.creatures = [x for x in self.game_map.entities if x.char != "C"]

    def update_game_map(self):
        self.generator.generate_dungeon()
        self.game_map = self.generator.get_dungeon()
        self.update_fov()
        self.tick = 0
        self.monster_tick = 0
        self.generator.difficulty += 1
        self.game_map.difficulty += 1
        self.generator.max_monsters_per_room = self.generator.difficulty * 2
        self.floor.floor += 1

    # TODO Simplifiera
    def player_activated_trap(self, x: int, y: int) -> bool:
        if isinstance(self.game_map.tiles[x, y], tile_types.Trap):
            return True
        else:
            return False

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            if isinstance(event, tcod.event.MouseButtonDown):
                self.window.context.convert_event(event)
                return tuple(event.tile)
            action = self.event_handler.dispatch(event)

            match action:
                case None:
                    continue
                case "inventory":
                    self.inventory_open = not self.inventory_open
                    return "inventory"
                case "Level Up":
                    self.player.xp += 100
                case "close":
                    return "close"
                case "next_page":
                    return "next_page"
                case "previous_page":
                    return "previous_page"
                case "New Game":
                    return "new_game"
                case "Reset":
                    return "reset"

            if action.perform(self, self.player) is not None:
                self.tick += 1
                self.update_fov()

    def handle_enemy_AI(self):
        if self.monster_tick != self.tick:
            for monster in self.game_map.entities:
                if (
                    monster.char not in ("@", "C")
                    and random.randint(0, 100) > monster.move_chance
                    and monster.hp > 0
                    and self.game_map.calculate_distance(
                        monster.x, monster.y, self.player.x, self.player.y
                    )
                    <= monster.perception
                ):
                    if (
                        monster.hp < monster.max_hp // 2
                        and monster.inventory.items
                        and not monster.used_items
                        and random.randint(0, 100) > 50
                    ):
                        item = monster.choose_item()
                        item.use(engine=self, entity=monster)
                    else:
                        monster.monster_pathfinding(self.player, self.game_map, self)
            self.monster_tick = self.tick

    def can_player_attack(self):
        if not self.player_can_attack:
            self.player_attack_cool_down = time.time()
            self.player_can_attack = "None"

        if time.time() - self.player_attack_cool_down >= 1:
            self.player_can_attack = True

    def handle_used_items(self):
        for entity in self.creatures:
            if entity.used_items != []:
                for item in entity.used_items:
                    if self.tick - item.activated_tick >= item.duration:
                        item.remove_effect(entity)
                        self.message_log.add_message(
                            f"The {entity.name}'s {item.type} has worn off!",
                            color.white,
                        )

    def update_fov(self) -> None:
        for (x, row) in enumerate(self.game_map.tiles):
            for (y, value) in enumerate(row):
                if self.game_map.get_tile(x, y).transparent:
                    self.game_map.transparent_tiles[x, y] = True

        self.game_map.visible[:] = compute_fov(
            transparency=self.game_map.transparent_tiles,
            pov=(self.player.x, self.player.y),
            radius=self.player.perception // 2,
            algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST,
        )

    def check_inventory(self):
        if self.inventory_open:
            return "open"

    def check_entities(self):
        for entity in self.game_map.entities:
            if entity.hp <= 0:
                if entity.char == "@":
                    return "dead"
                self.message_log.add_message(f"{entity.name} died!", color.death_text)
                self.game_map.entities.remove(entity)
                self.player.xp += entity.xp_value
                self.render(console=self.window.console, context=self.window.context)
                # self.sound_handler.monster_death()
                break

        self.game_map.explored |= self.game_map.visible

    def check_xp(self):
        if self.player.xp >= self.player.xp_to_next_level:
            self.player.level += 1
            self.message_log.add_message(
                f"You are now level {self.player.level}!", (0, 0, 255)
            )
            self.player.xp_to_next_level *= 2
            return "Level Up"

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        render_bar(
            console=console,
            current_value=self.player.hp,
            maximum_value=self.player.max_hp,
            total_width=20,
        )
        self.message_log.render(console=console, x=23, y=62, width=40, height=6)
        self.window.render_log(
            player=self.player,
            engine=self,
        )
        context.present(console)

        console.clear()

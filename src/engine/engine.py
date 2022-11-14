from typing import Set, Iterable, Any

import tcod.constants
from tcod.context import Context
from tcod.map import compute_fov

from actions.input_handlers import EventHandler
from creature.entity import Entity, Player, Monster
from stage.game_map import GameMap
from stage.tile_types import *


class Engine:
    """Klassen för spel motorn, samlar all funktionalitet i metoder"""

    def __init__(
        self,
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
        radius: int,
        tick: int,
    ):
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.radius = radius
        self.tick = 0
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.tick += 1

            self.update_fov()

    def update_fov(self) -> None:
        for (x, row) in enumerate(self.game_map.tiles):
            for (y, value) in enumerate(row):
                if self.game_map.get_tile(x, y).transparent:
                    self.game_map.transparent_tiles[x, y] = True

        self.game_map.visible[:] = compute_fov(
            self.game_map.transparent_tiles,
            (self.player.x, self.player.y),
            radius=self.radius,
            algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST,
        )

        self.game_map.explored |= self.game_map.visible

    def entity_at_location(self, x: int, y: int) -> Set[Entity]:
        return {
            entity
            for entity in self.game_map.entities
            if entity.x == x and entity.y == y
        }

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        context.present(console)

        console.clear()

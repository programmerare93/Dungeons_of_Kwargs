from typing import Set, Iterable, Any

import tcod.constants
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

import numpy as np

from src.actions.input_handlers import EventHandler
from src.creature.entity import Entity
from src.stage.game_map import GameMap
from src.stage.tile_types import *


class Engine:
    """Klassen för spel motorn, samlar all funktionalitet i metoder"""

    def __init__(
            self,
            entities: Set[Entity],
            event_handler: EventHandler,
            game_map: GameMap,
            player: Entity,
            radius: int
    ):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.radius = radius
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

            self.update_fov()

    def update_fov(self) -> None:
        """
        self.game_map.explored = np.zeros((self.game_map.width, self.game_map.height), dtype=bool, order="F")
        self.game_map.transparent = np.ones((self.game_map.width, self.game_map.height), dtype=bool, order="F")

        for (i, row) in enumerate(self.game_map.transparent):
            for (j, value) in enumerate(row):
                self.game_map.transparent[i, j] = self.game_map.get_tile(i, j).transparent

        self.game_map.visible_tiles = compute_fov(self.game_map.transparent, (self.player.x, self.player.y), radius=self.radius)

        self.game_map.explored |= self.game_map.visible_tiles

        for (i, row) in enumerate(self.game_map.visible_tiles):
            for (j, value) in enumerate(row):
                if value:
                    self.game_map.get_tile(i, j).visible = True

        for (i, row) in enumerate(self.game_map.explored):
            for(j, value) in enumerate(row):
                if value:
                    self.game_map.get_tile(i, j).seen = True
                    self.game_map.get_tile(i, j).color = seen_color
        """
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles,
            (self.player.x, self.player.y),
            radius=self.radius,
            algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST)

        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            if not self.game_map.visible[entity.x, entity.y]:
                continue
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

        context.present(console)

        console.clear()

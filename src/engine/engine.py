from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from src.actions.input_handlers import EventHandler
from src.creature.entity import Entity
from src.stage.game_map import GameMap


class Engine:
    """Klassen för spel motorn, samlar all funktionalitet i metoder"""
    def __init__(
        self,
        entities: Set[Entity],
        event_handler: EventHandler,
        game_map: GameMap,
        player: Entity,
    ):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

        context.present(console)

        console.clear()

import tcod

from window.window import Window
from engine.engine import Engine
from creature.entity import Entity
from actions.input_handlers import EventHandler
from stage.game_map import GameMap
from stage.procgen import generate_dungeon

tileset = tcod.tileset.load_tilesheet(
    "./assets/Potash_10x10.png", 16, 16, tcod.tileset.CHARMAP_CP437
)

window = Window("Dungeons of Kwargs", 80, 50, tileset)


def main():
    event_handler = EventHandler()

    player = Entity(int(window.width / 2), int(window.height / 2), "@", (255, 255, 255))
    npc = Entity(int(window.width / 2 - 5), int(window.height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = generate_dungeon(map_width=80, map_height=45)

    engine = Engine(
        entities=entities, event_handler=event_handler, game_map=game_map, player=player
    )

    while True:
        engine.render(console=window.console, context=window.context)

        events = tcod.event.wait()

        engine.handle_events(events)


if __name__ == "__main__":
    main()

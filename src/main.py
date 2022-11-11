import tcod

from window.window import Window
from engine.engine import Engine
from creature.entity import Entity
from actions.input_handlers import EventHandler
from stage.game_map import GameMap

tileset = tcod.tileset.load_tilesheet("../assets/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

window = Window("Caves of Kwargs", 80, 50, tileset)

def main():
    event_handler = EventHandler()

    player = Entity(int(window.width / 2), int(window.height / 2), "@", (255, 255, 255))
    npc = Entity(int(window.width / 2 - 5), int(window.height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    game_map = GameMap(window.width, window.height)

    engine = Engine(
        entities=entities, event_handler=event_handler, game_map=game_map, player=player
    )

    while True:
        engine.render(console=window.console, context=window.context)

        events = tcod.event.wait()

        engine.handle_events(events)


if __name__ == "__main__":
    main()

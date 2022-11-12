import tcod

from actions.input_handlers import EventHandler
from creature.entity import Entity
from engine.engine import Engine
from stage.floor import Floor
from stage.procgen import generate_dungeon
from window.window import Window

tileset = tcod.tileset.load_tilesheet(
    "../assets/Potash_10x10.png", 16, 16, tcod.tileset.CHARMAP_CP437
)

window = Window("Dungeons of Kwargs", 80, 50, tileset)


def main():
    event_handler = EventHandler()

    player = Entity(int(window.width / 2), int(window.height / 2), "@", (255, 255, 255))
    entities = {player}

    floor = Floor()

    game_map = generate_dungeon(
        floor.max_rooms,
        floor.room_min_size,
        floor.room_max_size,
        window.width,
        window.height,
        player,
        radius=4
    )

    engine = Engine(
        entities, event_handler, game_map, player, radius=4
    )

    while True:
        engine.render(window.console, window.context)

        events = tcod.event.wait()

        engine.handle_events(events)


if __name__ == "__main__":
    main()

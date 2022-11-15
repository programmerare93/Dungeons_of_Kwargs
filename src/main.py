import tcod

from actions.input_handlers import EventHandler
from creature.entity import Player
from engine.engine import Engine
from stage.floor import Floor
from stage.procgen import generate_dungeon
from window.window import Window

max_monsters_per_room = 3

tileset = tcod.tileset.load_tilesheet(
    "../assets/Potash_10x10.png", 16, 16, tcod.tileset.CHARMAP_CP437
)

window = Window("Dungeons of Kwargs", 80, 70, tileset)


def main():
    event_handler = EventHandler()

    player = Player(
        int(window.width / 2),
        int(window.height / 2),
        "@",
        (255, 255, 255),
        5,
        0,
        0,
        0,
        0,
    )

    floor = Floor()

    game_map = generate_dungeon(
        floor.max_rooms,
        floor.room_min_size,
        floor.room_max_size,
        window.width,
        window.height - 20,
        player,
    )

    engine = Engine(event_handler, game_map, player, radius=4, tick=0)

    while True:
        window.render_log(player, engine)

        engine.render(window.console, window.context)

        events = tcod.event.wait()

        engine.handle_events(events)


if __name__ == "__main__":
    main()

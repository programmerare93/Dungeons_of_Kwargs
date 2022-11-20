import tcod

from actions.input_handlers import EventHandler
from creature.entity import Player
from engine.engine import Engine
from stage.floor import Floor
from stage.procgen import Generator
from window.window import Window
from window.log import Log

max_monsters_per_room = 3

tileset = tcod.tileset.load_tilesheet(
    "../assets/Potash_10x10.png", 16, 16, tcod.tileset.CHARMAP_CP437
)

window = Window("Dungeons of Kwargs", 80, 70, tileset)


def main():
    event_handler = EventHandler()

    floor = Floor()
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

    generator = Generator(floor.max_rooms, window.width, window.height - 20, player)
    generator.generate_dungeon()
    game_map = generator.get_dungeon()

    engine = Engine(event_handler, game_map, player, generator, radius=4)
    log = Log(window, player, engine)

    while True:
        log.render()

        engine.render(window.console, window.context)

        events = tcod.event.wait()

        engine.handle_events(events)


if __name__ == "__main__":
    main()

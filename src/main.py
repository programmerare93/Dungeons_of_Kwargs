import tcod

from actions.input_handlers import EventHandler
from creature.entity import Player
from engine.engine import Engine
from stage.floor import Floor
from stage.procgen import Generator
from window.window import Window
from window import color

max_monsters_per_room = 3

tileset = tcod.tileset.load_tilesheet(
    "./assets/Potash_10x10.png", 16, 16, tcod.tileset.CHARMAP_CP437
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
        max_hp=30,
        hp=30,
        strength=2,
        dexterity=5,
        intelligence=5,
        perception=4,
    )

    generator = Generator(floor.max_rooms, window.width, window.height - 20, player)
    generator.generate_dungeon()
    game_map = generator.get_dungeon()

    engine = Engine(event_handler, game_map, player, generator)
    engine.message_log.add_message("Welcome to Dungeons of Kwargs!", color.welcome_text)

    while True:
        engine.render(window.console, window.context)

        events = tcod.event.wait()

        engine.handle_events(events)

        engine.can_player_attack()

        engine.check_entities()


if __name__ == "__main__":
    main()

import tcod
import numpy as np

from actions.input_handlers import EventHandler
from creature.entity import Player
from engine.engine import Engine
from stage.floor import Floor
from stage.procgen import Generator
from window.window import Window
from window import color
from window.log import Log
from engine.game_states import level_up_state, death_state


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
        strength=50,
        dexterity=8,
        intelligence=5,
        perception=10,
    )

    generator = Generator(floor.max_rooms, window.width, window.height - 20, player)
    game_map = None

    engine = Engine(event_handler, game_map, player, floor, generator)
    engine.message_log.add_message("Welcome to Dungeons of Kwargs!", color.welcome_text)
    log = Log(window, player, engine)
    engine.game_map.generate_pathfinding_map()

    while True:
        engine.render(window.console, window.context)
        log.render()

        events = tcod.event.wait()

        engine.handle_events(events)

        engine.handle_enemy_AI()

        engine.can_player_attack()

        if engine.check_entities() == "dead":
            death_state(engine, window)

        if engine.check_xp() == "Level Up":
            level_up_state(engine, window)


if __name__ == "__main__":
    main()

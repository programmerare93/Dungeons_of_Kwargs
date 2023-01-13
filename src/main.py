import tcod

from actions.input_handlers import EventHandler
from creature.entity import Player
from engine.engine import Engine
from engine.game_states import *
from stage.floor import Floor
from stage.procgen import Generator
from window.window import Window
from window import color


tileset = tcod.tileset.load_tilesheet(
    "./assets/Potash_10x10.png", 16, 16, tcod.tileset.CHARMAP_CP437
)


window = Window("Dungeons of Kwargs", 80, 70, tileset)


def main():
    event_handler = EventHandler()
    floor = Floor()
    player = Player(
        color=(255, 255, 255),
        char="@",
    )

    game_map = None

    generator = Generator(window.width, window.height - 26, player, floor=floor)
    engine = Engine(
        event_handler,
        game_map,
        player=player,
        floor=floor,
        generator=generator,
        window=window,
    )
    engine.message_log.add_message("Welcome to Dungeons of Kwargs!", color.welcome_text)
    engine.game_map.generate_pathfinding_map()
    main_menu(engine, window=window)
    player.stats = stats_screen(engine, window=window)
    player.update_stats()

    while True:

        events = tcod.event.wait()

        engine.handle_events(events)

        engine.handle_enemy_AI()

        engine.can_player_attack()

        engine.handle_used_items()

        if engine.check_entities() == "dead":
            death_state(engine, window)

        if engine.check_xp() == "Level Up":
            player.stats = stats_screen(engine, window=window)
            player.update_stats()

        if engine.check_inventory() == "open":
            inventory_state(engine, window)

        engine.render(window.console, window.context)


if __name__ == "__main__":
    main()

from creature.entity import Player
from engine.engine import Engine
from engine.game_states import *
from stage.floor import Floor
from stage.procgen import Generator
from window.window import Window
from window.color import *

# Definierar ett tileset för att använda i spelet, den här är en 16x16 tileset
# som representerar varje tecken som vi använder i spelet
tileset = tcod.tileset.load_tilesheet(
    "../assets/Potash_10x10.png", 16, 16, tcod.tileset.CHARMAP_CP437
)


window = Window(
    "Dungeons of Kwargs", 80, 70, tileset
)  # Definierar ett window med namnet Dungeons of Kwargs, 80x70 storlek och använder tileset som tileset


def main():  # Huvudfunktionen som körs när spelet startas
    floor = Floor()  # Definierar en floor som används i spelet
    player = Player(
        color=light_purple,
        char="@",
    )

    game_map = None

    generator = Generator(
        window.width, window.height - 26, player, floor=floor
    )  # Skapar en generator som används för att generera spelplanen
    engine = (
        Engine(  # Skapar en engine som används för att hantera allt som händer i spelet
            game_map=game_map,
            player=player,
            floor=floor,
            generator=generator,
            window=window,
        )
    )
    engine.message_log.add_message(
        "Welcome to Dungeons of Kwargs!", welcome_color
    )  # Skriver ut ett meddelande när spelet startas
    engine.game_map.generate_pathfinding_map()  # Genererar en pathfinding map som används för att beräkna vägen till spelaren
    main_menu(engine, window=window)  # Visar huvudmenyn
    player.stats = stats_screen(engine, window=window)  # Visar statsmenyn
    player.update_stats()  # Uppdaterar statsen utifrån spelarens val
    engine.player_can_move = True
    engine.game_has_started = True

    while True:  # Spel loopen

        engine.handle_events()

        engine.handle_enemy_AI()

        engine.can_player_attack()

        engine.handle_used_items()

        who_dead = engine.check_entities()
        if who_dead == "player_kill":
            death_state(engine, window)
        elif who_dead == "boss_kill":
            victory_state(engine, window)

        if engine.check_xp() == "Level Up":  # Ifall spelaren har levlat upp
            player.stats = stats_screen(
                engine, window=window
            )  # Visar statsmenyn, som i början av spelet
            player.update_stats()

        if engine.check_inventory() == "open":  # Ifall spelaren öppnar sin inventory
            inventory_state(engine, window)  # Visar inventory skärmen

        engine.render(
            window.console, window.context
        )  # Renderar allt som händer i spelet


if __name__ == "__main__":  # Sant ifall filen körs som huvud fil
    main()  # Kör huvud funktionen

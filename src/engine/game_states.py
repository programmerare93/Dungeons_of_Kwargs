from creature.entity import Player
import tcod.event


def level_up_state(engine, window):
    available_points = engine.player.intelligence // 2 + 5
    temp_player = engine.player

    while available_points > 0:
        events = tcod.event.wait()
        stat = engine.handle_level_up_events(events)
        if stat is not None and stat != "reset":
            if stat == "max_hp":
                engine.player.max_hp += 1
            elif stat == "strength":
                engine.player.strength += 1
            elif stat == "perception":
                engine.player.perception += 1
            elif stat == "dexterity":
                engine.player.dexterity += 1
            elif stat == "intelligence":
                engine.player.intelligence += 1
            available_points -= 1
        elif stat == "reset":
            engine.player.max_hp = temp_player.max_hp
            engine.player.strength = temp_player.strength
            engine.player.perception = temp_player.perception
            engine.player.dexterity = temp_player.dexterity
            engine.player.intelligence = temp_player.intelligence
            available_points = engine.player.intelligence // 2 + 5
        window.console.clear(bg=(0, 0, 0))
        window.console.draw_frame(
            window.width // 2 - 20,
            10,
            window.width - 40,
            window.height - 20,
            "Level Up !",
            clear=False,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        window.console.print(
            window.width // 2 - 10,
            12,
            "Available points: " + str(available_points),
            fg=(0, 255, 0),
        )

        window.console.print(
            window.width // 2 - 18,
            24,
            f"Max HP: {engine.player.max_hp} (1)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2 - 18,
            40,
            f"Strength: {engine.player.strength} (3)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2 - 18,
            54,
            f"Dexterity: {engine.player.dexterity} (5)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2,
            24,
            f"Perception: {engine.player.perception} (2)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2,
            40,
            f"Intelligence: {engine.player.intelligence} (4)",
            fg=(255, 255, 255),
        )

        window.console.print(
            window.width // 2,
            45,
            f"Press the number\n\n of the stat you\n\n want to increase",
            fg=(0, 255, 255),
        )

        window.console.print(
            window.width // 2,
            56,
            f"Reset (R)",
            fg=(255, 0, 0),
        )

        engine.render(window.console, window.context, level_up=True)


def death_state(engine, window):
    while True:
        events = tcod.event.wait()
        engine.handle_death_events(events)
        engine.render(window.console, window.context)
        window.console.print_box(
            window.width // 2 - 5,
            window.height // 2,
            20,
            5,
            "You died!",
            fg=(255, 0, 0),
        )

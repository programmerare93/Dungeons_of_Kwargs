import tcod.event
import tcod.sdl.render


def inventory_state(engine, window):
    while True:
        window.console.clear()

        window.console.draw_frame(
            0,
            0,
            window.width,
            window.height,
            title="Inventory",
            fg=(255, 255, 255),
            bg=(0, 0, 0),
            clear=True,
        )

        x = 1
        y = 1
        if len(engine.player.inventory.items) == 0:
            window.console.print(
                window.width // 2,
                window.height // 2,
                "Inventory is empty",
                fg=(255, 255, 255),
                alignment=tcod.CENTER,
            )
        else:
            for (place_in_inventory, item) in enumerate(engine.player.inventory.items):
                if place_in_inventory == 0:
                    # På första enumerationen ändra inte x och y värdet
                    pass
                elif y >= window.width:
                    x += 25
                    y = 1
                else:
                    y += 2

                window.console.print(
                    x,
                    y,
                    string=f"{item.type}({place_in_inventory + 1})",
                    fg=(255, 255, 255),
                    bg=(0, 0, 0),
                    alignment=tcod.LEFT
                )

        window.console.print(
            window.width // 2,
            window.height,
            "Press the number next to the item to use it"
        )

        window.context.present(window.console)

        events = tcod.event.wait()

        event = engine.handle_inventory_events(events)

        if event == "close":
            engine.inventory_open = False
            break


def main_menu(engine, window):
    while True:
        events = tcod.event.wait()
        if engine.handle_main_menu_events(events) == "new_game":
            return "playing"
        window.console.clear(bg=(0, 0, 0))

        window.console.draw_frame(
            0,
            0,
            window.width,
            window.height,
            title="Main menu",
            fg=(255, 255, 255),
            bg=(0, 0, 0),
            clear=True,
        )

        window.console.print(
            x=window.width // 2,
            y=window.height // 2 - 4,
            string="Press enter to start",
            fg=(255, 255, 255),
            alignment=tcod.CENTER,
        )

        window.context.present(window.console)


def level_up_state(engine, window):
    available_points = engine.player.intelligence // 2 + 5
    temp_player = engine.player
    temp_stats = (
        engine.player.max_hp,
        engine.player.strength,
        engine.player.perception,
        engine.player.dexterity,
        engine.player.intelligence,
    )

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
            engine.player.max_hp = temp_stats[0]
            engine.player.strength = temp_stats[1]
            engine.player.perception = temp_stats[2]
            engine.player.dexterity = temp_stats[3]
            engine.player.intelligence = temp_stats[4]
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

        window.context.present(window.console)


def death_state(engine, window):
    window.console.clear(bg=(0, 0, 0))
    while True:
        events = tcod.event.wait()
        engine.handle_death_events(events)
        window.console.print_box(
            window.width // 2 - 5,
            window.height // 2,
            100,
            200,
            "You died!",
            fg=(255, 0, 0),
        )
        window.console.print_box(
            window.width // 2 - 10,
            window.height - 5,
            20,
            5,
            "Press esc to to quit",
            fg=(255, 255, 255),
        )
        window.context.present(window.console)

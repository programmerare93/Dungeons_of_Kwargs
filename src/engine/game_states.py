import tcod.event
import tcod.sdl.render


class InventoryBox:
    def __init__(self, x, y, width, height, item=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item = item
        self.item_path = "assets\\items\\{}.png".format(
            self.item.name.replace(" ", "_") + "-removebg-preview"
        )

    def render(self, window):
        window.console.print_box(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            string=self.item.name,
        )
        if self.item.name in (
            "small health potion",
            "medium health potion",
            "large health potion",
            "very large health potion",
            "giant health potion",
        ):
            window.show_image(
                self.item_path, self.x, self.y + 4, self.width, self.height
            )


def inventory_state(engine, window):
    x_offset = 3
    y_offset = 4
    box_width = 13
    box_height = 20
    max_items_per_page = (
        window.width // (box_width + 1) * (window.height // (box_height + 1))
    )
    player_items = engine.player.inventory.items
    if len(player_items) != 0:
        num_pages = len(player_items) // max_items_per_page
        all_page_items = [[] for _ in range(num_pages + 1)]
        i = 0
        for item in player_items:
            if len(all_page_items[i]) == max_items_per_page:
                i += 1
                y_offset = 4
                x_offset = 3
            elif x_offset + 8 > window.width:
                x_offset = 3
                y_offset += box_height + 1
            new_box = InventoryBox(x_offset, y_offset, box_width, box_height, item)
            all_page_items[i].append(new_box)
            x_offset += box_width + 1
        current_page = 0
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

        if len(player_items) == 0:
            window.console.print(
                window.width // 2,
                window.height // 2,
                "Inventory is empty",
                fg=(255, 255, 255),
                alignment=tcod.CENTER,
            )
        else:
            for inventory_box in all_page_items[current_page]:
                inventory_box.render(window)

        window.context.present(window.console)

        events = tcod.event.wait()

        event = engine.handle_inventory_events(events)

        if event == "close":
            engine.inventory_open = False
            return
        elif event == "next_page":
            if current_page < num_pages:
                current_page += 1
        elif event == "previous_page":
            if current_page > 0:
                current_page -= 1
        elif isinstance(event, tuple):
            mouse_x, mouse_y = event
            for inventory_box in all_page_items[current_page]:
                if (
                    mouse_x >= inventory_box.x
                    and mouse_x <= inventory_box.x + inventory_box.width
                    and mouse_y >= inventory_box.y
                    and mouse_y <= inventory_box.y + inventory_box.height
                ):
                    inventory_box.item.use(engine, engine.player)
                    engine.inventory_open = False
                    return


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
        engine.update_fov()


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

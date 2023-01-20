import tcod.event
import tcod.sdl.render
from window.color import *
from typing import List


class Box:
    def __init__(self, x, y, width, height) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class StatBox(Box):
    """Liknande till inventory box klassen fast för statistik"""

    def __init__(self, x, y, width, height, stat_name, stats, index):
        super().__init__(x, y, width, height)
        self.stat_name = stat_name
        self.stat_value = stats[self.stat_name]
        self.stat_description = stat_description[self.stat_name]
        self.stat_color = all_stat_colors[self.stat_name]
        self.stat_path = "..\\assets\\attributes\\{}.png".format(self.stat_name)
        self.index = index

    def render(self, window) -> None:
        """Renderar en attribut samt en bild av den"""
        window.console.draw_frame(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            title=self.stat_name,
            fg=self.stat_color,
            bg=(0, 0, 0),
        )
        window.console.print_box(
            x=self.x + 3,
            y=self.y + 3,
            width=self.width - 5,
            height=self.height + self.y,
            string=self.stat_description,
        )
        window.print(
            x=self.x + self.width // 2,
            y=self.y + self.width // 2,
            string=f"{self.stat_value}",
            fg=green,
        )

        window.print(x=self.x + 1, y=self.y + 1, string=f"({self.index})")

        window.show_image(self.stat_path, self.x + 1, self.y + 10)


class InventoryBox(Box):
    """En låda som innehåller ett föremål och allt som krävs för att rendera den"""

    def __init__(self, x, y, width, height, item=None):
        super().__init__(x, y, width, height)
        self.item = item
        self.item_path = "..\\assets\\items\\{}.png".format(self.item.name)

    def render(self, window) -> None:
        window.console.print_box(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            string=self.item.name,
        )
        window.show_image(
            self.item_path, self.x, self.y + 4, self.width, self.height
        )  # Visar föremålets bild


def is_in_box(all_boxes, x, y) -> StatBox:
    """Kollar ifall en låda har blivit klickad på"""
    for box in all_boxes:
        if x in range(box.x, box.x + box.width) and y in range(
            box.y, box.y + box.height
        ):
            return box
    return None


def inventory_state(engine, window) -> None:
    """Game state för inventory"""
    engine.player_can_move = False
    x_offset = 3
    y_offset = 4
    box_width = 13
    box_height = 20
    max_items_per_page = (  # Räknar ut hur många items som kan visas på en sida
        window.width // (box_width + 1) * (window.height // (box_height + 1))
    )
    player_items = engine.player.items
    if len(player_items) != 0:
        num_pages = (
            len(player_items) // max_items_per_page
        )  # Räknar ut hur många sidor som behövs
        all_page_items = [
            [] for _ in range(num_pages + 1)
        ]  # Skapar en lista med listor för varje sida
        i = 0
        for item in player_items:
            if (
                len(all_page_items[i]) == max_items_per_page
            ):  # Om den nuvarande sidan är full så skapas en ny
                i += 1
                y_offset = 4
                x_offset = 3
            elif x_offset + 8 > window.width:  # "Byter rad" för föremålen
                x_offset = 3
                y_offset += box_height + 1
            new_box = InventoryBox(
                x_offset, y_offset, box_width, box_height, item
            )  # Skapar en ny låda med all information för att kunna visa ett föremål
            all_page_items[i].append(new_box)
            x_offset += box_width + 1
        current_page = 0
    while True:
        window.clear()

        window.console.draw_frame(
            0,
            0,
            window.width,
            window.height,
            title="Inventory",
            fg=white,
            bg=black,
            clear=True,
        )

        if (
            len(player_items) == 0
        ):  # Om det inte finns några föremål i inventory så visas bara ett meddelande
            window.print(
                window.width // 2,
                window.height // 2,
                "Inventory is empty",
                fg=white,
                alignment=tcod.CENTER,
            )
        else:
            for inventory_box in all_page_items[
                current_page
            ]:  # Renderar alla lådor på nuvarande sida
                inventory_box.render(window)
            window.console.print_box(
                x=window.width - 11,
                y=1,
                width=10,
                height=20,
                string="Page {}/{}: Arrow keys to switch page".format(
                    current_page + 1, num_pages + 1
                ),
                fg=yellow,
            )
            window.console.print_box(
                x=window.width - 11,
                y=6,
                width=10,
                height=20,
                string="Right click to drop items",
                fg=yellow,
            )

        window.present()

        event = engine.handle_events()

        if event == "inventory":  # Ifall spelaren trycker på i så stängs inventoryt
            engine.inventory_open = False
            engine.player_can_move = True
            window.clear()
            window.present()
            return
        elif event == "next_page":  # Ändrar sida
            if current_page < num_pages:
                current_page += 1
        elif event == "previous_page":
            if current_page > 0:
                current_page -= 1
        elif (
            isinstance(event, tuple) and len(player_items) != 0
        ):  # Ifall spelaren klickade
            mouse_x, mouse_y = event
            hit_box = is_in_box(
                all_page_items[current_page], mouse_x, mouse_y
            )  # Ifall det träffade en låda
            if hit_box != None:
                hit_box.item.use(
                    engine, engine.player
                )  # Använder föremålet och stänger inventoryt
                engine.inventory_open = False
                engine.player_can_move = True
                return
        elif isinstance(event, list):
            mouse_x, mouse_y = tuple(event)
            hit_box = is_in_box(all_page_items[current_page], mouse_x, mouse_y)
            if hit_box != None:
                all_page_items[current_page].remove(hit_box)
                engine.player.items.remove(hit_box.item)
                engine.message_log.add_message(
                    "You dropped the {}!".format(hit_box.item.name)
                )


# Varje attribut har sin egen beskrivning
stat_description = {
    "Max_HP": "The maximum amount of health your character can have",
    "Strength": "How much damage your character can do",
    "Perception": "Your character's ability to hit enemies as well as how far your character can see",
    "Agility": "Your character's ability to dodge attacks as well as traps",
    "Intelligence": "The amount of skill points your character has to spend each level",
}

all_stat_names = ["Max_HP", "Strength", "Perception", "Agility", "Intelligence"]


# Varje attribut har sin egen färg
all_stat_colors = {
    "Max_HP": red,
    "Strength": blue,
    "Perception": orange,
    "Agility": light_blue,
    "Intelligence": pink,
}


def main_menu(engine, window) -> str:
    """Game state för huvudmenyn"""

    while True:
        if engine.handle_events() == "new_game":
            window.clear()
            window.present()
            return "playing"
        window.clear()

        window.show_image("..\\assets\\main_menu.png", 0, 0)

        window.print(
            x=window.width // 2 - 10,
            y=window.height // 2 - 10,
            string="DUNGEONS OF KWARGS",
            fg=(0, 255, 255),
        )
        window.print(
            x=window.width // 2 - 10,
            y=window.height // 2,
            string="Press Enter to start",
            fg=white,
        )

        window.present()


def stats_screen(engine, window) -> List:
    """Game state för player sheet samt för level up"""
    engine.player_can_move = False
    x_offset = 5
    y_offset = 3
    box_width = 26
    box_height = 20
    all_boxes = []
    temp_stats = {  # Sparar spelarens nuvarande statistik så att spelaren kan gå tillbaka till den ifall de vill
        "Max_HP": engine.player.max_hp,
        "Strength": engine.player.strength,
        "Perception": engine.player.perception,
        "Intelligence": engine.player.intelligence,
        "Agility": engine.player.agility,
    }

    for i, stat in enumerate(all_stat_names):  # Liknande till inventory lådorna
        if y_offset + box_height >= window.height:
            y_offset = 3
            x_offset += box_width + 1
        new_box = StatBox(
            x_offset, y_offset, box_width, box_height, stat, temp_stats, i + 1
        )
        all_boxes.append(new_box)
        y_offset += box_height + 1
    original_points = (
        engine.player.intelligence // 2 + 5
    )  # Räknar ut hur många skill points som spelaren får
    available_points = original_points
    while (
        available_points > 0
    ):  # Så länge spelaren har skill points så kan de öka sina stats
        event = engine.handle_events()
        if isinstance(
            event, tuple
        ):  # Ifall spelaren klickar på en attribut så ökar den med 1
            mouse_x, mouse_y = event
            hit_stat = is_in_box(all_boxes, mouse_x, mouse_y)
            if hit_stat != None:
                hit_stat.stat_value += 1
                available_points -= 1
        elif (
            event == "reset"
        ):  # Om spelaren klickar på reset så återställs alla stats till de värden de var innan
            for stat_box in all_boxes:
                stat_box.stat_value = temp_stats[stat_box.stat_name]
            available_points = original_points
        elif event in [str(i) for i in range(6)]:
            all_boxes[int(event) - 1].stat_value += 1
            available_points -= 1
        window.clear()

        for box in all_boxes:
            box.render(window)

        window.console.draw_frame(
            0,
            0,
            window.width,
            window.height,
            title="Player Sheet",
            fg=white,
            bg=black,
            clear=False,
        )

        window.print(
            x=window.width // 2 + 5,
            y=window.height - 14,
            string=f"(Available points: {available_points})",
            fg=pink,
            bg=black,
            alignment=tcod.CENTER,
        )

        window.console.print_box(
            x=window.width - 21,
            y=5,
            width=21,
            height=window.height - 5,
            string="Controls: \n\n\nMove: WASD \n\n\nGo down stairs: < \n\n\nToggle Inventory: i \n\n\n Open Chest: e \n\n\nExit: Escape \n\n\nTo attack an enemy simply walk into them!",
        )

        window.print(
            x=window.width // 2 - 8,
            y=window.height // 2 + 15,
            string="Choose your stats wisely!",
            fg=yellow,
        )

        window.print(
            x=window.width // 2 - 8,
            y=window.height // 2 + 17,
            string="Click on the boxes to increase your stats \nor press the number of \nthe stat you want to increase",
            fg=light_purple,
        )

        window.show_image("..\\assets\\main_character.png", window.width - 18, 48)

        window.print(
            x=window.width - 18, y=window.height // 2 + 10, string="Your character:"
        )

        window.print(
            x=window.width // 2 + 5,
            y=window.height - 10,
            string="Press r to reset",
            fg=red,
            bg=black,
            alignment=tcod.CENTER,
        )
        window.present()
    engine.player_can_move = True
    new_stats = [x.stat_value for x in all_boxes]
    window.clear()
    window.present()
    return new_stats  # Ger tillbaka en lista med alla stats så att de kan användas för att uppdatera spelarens stats


def victory_state(engine, window):
    window.console.clear(bg=(0, 0, 0))
    while True:
        events = tcod.event.wait()
        engine.handle_events(events)
        window.console.print_box(
            window.width // 2 - 5,
            window.height // 2,
            100,
            200,
            "You won!",
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


def death_state(engine, window) -> None:
    """Game state för när spelaren dör"""
    engine.player_can_move = False
    window.clear()
    while True:
        engine.handle_events()
        window.console.print_box(
            window.width // 2 - 5,
            window.height // 2,
            100,
            200,
            "You died!",
            fg=red,
        )
        window.console.print_box(
            window.width // 2 - 10,
            window.height - 5,
            20,
            5,
            "Press esc to to quit",
            fg=white,
        )
        window.present()

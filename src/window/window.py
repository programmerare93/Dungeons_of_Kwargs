import tcod.sdl.render
import os


class Window:
    """Klass för att skapa ett fönster med tcod"""

    context: tcod.context
    console: tcod.Console
    width: int
    height: int

    def __init__(self, title: str, width: int, height: int, tileset):
        self.console = tcod.Console(width, height, "F")

        self.context = tcod.context.new(  # Skapar ett nytt fönster
            width=width,
            height=height,
            title=title,
            vsync=True,
            tileset=tileset,
            sdl_window_flags=tcod.context.SDL_WINDOW_FULLSCREEN_DESKTOP,
        )

        self.height = height
        self.width = width

    def show_image(self, image_path, x, y, width=None, height=None):
        """Metod för att visa bilder"""
        image = tcod.image_load(image_path)
        if width is None and height is None:
            width, height = image._get_size()
        image.blit_2x(self.console, x, y)
        tcod.console_blit(self.console, 0, 0, width, height, 0, 0, 0)

    def render_log(self, player, engine):
        """Metod för att visa loggen"""
        self.console.draw_frame(0, 45, self.width, self.height - 45, "Log", clear=False)
        x_offset = 5
        y_offset = 46
        all_images = [
            "Max_HP.png",
            "Strength.png",
            "Perception.png",
            "Agility.png",
            "Intelligence.png",
        ]
        all_stat_colors = {
            "Max_HP.png": (255, 0, 0),
            "Strength.png": (0, 0, 255),
            "Perception.png": (255, 128, 0),
            "Agility.png": (0, 255, 255),
            "Intelligence.png": (255, 0, 255),
        }
        for i, stat in enumerate(player.stats):  # Visar alla stats
            if i == 3:
                x_offset = 9
                y_offset += 10
            self.show_image(
                f"assets\\attributes\\{all_images[i]}", 50 + x_offset, y_offset
            )
            self.console.print(
                50 + x_offset,
                y_offset + 9,
                f"{stat}",
                fg=all_stat_colors[all_images[i]],
            )
            x_offset += 8

        self.show_image("assets\\main_character.png", 3, 46)  # Visar spelarens bild

    def print(
        self, x: int, y: int, string: str, fg=(255, 255, 255), bg=None, alignment=0
    ):
        self.console.print(x, y, string, fg, bg=bg, alignment=alignment)

    def clear(self):
        self.console.clear()

    def present(self):
        """Metod för att visa konsolen(fönstret)"""
        self.context.present(self.console)

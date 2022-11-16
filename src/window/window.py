from dataclasses import dataclass
import tcod


@dataclass
class Window:
    """Klass för att skapa ett fönster med tcod"""

    context: tcod.context
    console: tcod.Console
    width: int
    height: int

    def __init__(self, title: str, width: int, height: int, tileset):
        self.console = tcod.Console(width, height, "F")

        self.context = tcod.context.new(
            width=width,
            height=height,
            title=title,
            vsync=True,
            tileset=tileset,
            sdl_window_flags=tcod.context.SDL_WINDOW_FULLSCREEN_DESKTOP,
        )

        self.height = height
        self.width = width

    def render_log(self, player, engine):
        self.console.draw_frame(0, 51, self.width, self.height - 51, "Log", clear=False)
        self.console.print_box(
            5,
            52,
            self.width,
            self.height + 20,
            "Player position: {}, {}".format(player.x, player.y),
        )

        self.console.print_box(
            5,
            53,
            self.width,
            self.height - 53,
            "Current Tick: {}".format(engine.tick),
        )

        self.console.print_box(
            5,
            54,
            self.width,
            self.height - 53,
            "Player HP: {}".format(player.hp),
        )

    def print(self, x: int, y: int, string: str):
        self.console.print(x, y, string)

    def clear(self):
        self.console.clear()

    def present(self):
        """Metod för att visa konsolen(fönstret)"""
        self.context.present(self.console)

    def get_events(self):
        return tcod.event.wait()

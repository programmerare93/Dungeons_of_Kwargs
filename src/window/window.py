import tcod


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
            54,
            52,
            self.width,
            self.height + 20,
            "Player position: {}, {}".format(player.x, player.y),
        )

        self.console.print_box(
            54,
            53,
            self.width,
            self.height - 53,
            "Current Tick: {}".format(engine.tick),
        )

        self.console.print_box(
            55,
            54,
            self.width,
            self.height - 53,
            "Current Monster Tick: {}".format(engine.monster_tick),
        )

        self.console.print_box(
            55,
            55,
            self.width,
            self.height - 53,
            "Player HP: {}".format(engine.player.hp),
        )

        self.console.print_box(
            55,
            56,
            self.width,
            self.height - 52,
            "Player XP: {}".format(engine.player.xp),
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

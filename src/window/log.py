from creature.entity import Player
from engine.engine import Engine
from window.window import Window


class Log:
    def __init__(self, window: Window, player: Player, engine: Engine):
        self.player = player
        self.engine = engine
        self.window = window

    def render(self):
        self.window.console.draw_frame(0, 51, self.window.width, self.window.height - 51, "Log", clear=False)
        self.window.console.print_box(
            5,
            52,
            self.window.width,
            self.window.height - 52,
            "Player position: {}, {}".format(self.player.x, self.player.y),
        )

        self.window.console.print_box(
            5,
            53,
            self.window.width,
            self.window.height - 53,
            "Current Tick: {}".format(self.engine.tick),
        )

        self.window.console.print_box(
            5,
            54,
            self.window.width,
            self.window.height - 53,
            "Player HP: {}".format(self.player.hp),
        )

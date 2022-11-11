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
        self.context = tcod.context.new_terminal(width, height, tileset=tileset, title=title, vsync=True)
        self.width = width
        self.height = height


    def print(self, x: int, y: int, string: str):
        self.console.print(x, y, string)

    def clear(self):
        self.console.clear()

    def present(self):
        """Metod för att visa konsolen(fönstret)"""
        self.context.present(self.console)

    def get_events(self):
        return tcod.event.wait()

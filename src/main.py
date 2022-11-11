from window.window import *

tileset = tcod.tileset.load_tilesheet("../assets/arial10x10.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

window = Window("Caves of Kwargs", 80, 50, tileset)

# Main-loopen
while True:
    window.clear()

    window.print(40, 25, "@")

    window.present()

    for event in window.get_events():
        window.convert_event(event)
        if isinstance(event, tcod.event.Quit):
            exit()

        elif isinstance(event, tcod.event.KeyDown):
            # Skriv kod för knappar här
            pass

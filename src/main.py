from window.window import *

window = Window("test", 800, 600)
tile_set = TileSet("../assets/ibm_pc_font.png")

icon = pygame.image.load("../assets/fort_icon.png")
window.set_icon(icon)

# Main-loopen
while window.is_running:
    for event in window.get_event():
        if window.should_quit(event):
            window.is_running = False

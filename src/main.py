from window.window import *
from sys import exit

window = Window("test", 800, 600)

icon = pygame.image.load("../assets/fort_icon.png")
window.set_icon(icon)

# Main-loopen
while True:
    for event in window.get_event():
        if window.should_quit(event):
            exit()
    window.update()

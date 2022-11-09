from window.window import *
from sys import exit

window = Window("test", 800, 600)
from window.window import Window

window = Window("test", 600, 600)


# Main-loopen
while True:
    for event in window.get_event():
        if window.should_quit(event):
            exit()
    window.update()

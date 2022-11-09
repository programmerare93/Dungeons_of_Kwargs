from window.window import Window

window = Window("test", 600, 600)

running = True

while running:
    for event in window.get_event():
        if window.should_quit(event):
            running = False

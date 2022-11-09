import pygame
from dataclasses import dataclass


@dataclass
class Window:
    """Klass för att skapa ett fönster med pygame"""
    screen: pygame.surface
    image: pygame.image
    clock: pygame.time.Clock

    def __init__(self, title: str, width: int, height: int):
        """Constructor som initializerar pygame och skapar fönstret"""
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()

    def __del__(self):
        """Destructor som ser till att pygame avslutas"""
        pygame.quit()

    def set_icon(self, surface):
        pygame.display.set_icon(surface)

    def get_event(self):
        return pygame.event.get()

    def should_quit(self, event):
        if event.type == pygame.QUIT:
            return True
        else:
            return False

    def update(self):
        pygame.display.update()

    def tick(self, framerate: int):
        self.clock.tick(framerate)

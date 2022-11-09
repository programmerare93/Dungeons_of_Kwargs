import pygame
from dataclasses import dataclass


@dataclass
class Window:
    """Klass för att skapa ett fönster med pygame"""

    def __init__(self, title: str, width: int, height: int):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

    def get_event(self):
        return pygame.event.get()

    def should_quit(self, event):
        if event.type == pygame.QUIT:
            return True
        else:
            return False

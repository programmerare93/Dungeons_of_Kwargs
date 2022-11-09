import numpy as np
import pygame
from dataclasses import dataclass


@dataclass
class Window:
    """Klass för att skapa ett fönster med pygame"""
    screen: pygame.surface
    image: pygame.image
    is_running: bool

    def __init__(self, title: str, width: int, height: int):
        """Constructor som initializerar pygame och skapar fönstret"""
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.is_running = True

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


@dataclass
class TileSet:
    file: str
    size: tuple[int, int]
    margin: int
    spacing: int
    image: pygame.image
    rect: pygame.rect
    tiles: list

    def __init__(self, file: str, size=(8, 8), margin=1, spacing=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []

        self.load()

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

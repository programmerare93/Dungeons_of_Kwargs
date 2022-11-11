from typing import Tuple


class Entity:
    """Generisk klass för att representera en 'entitet', något som en fiende eller spelare"""

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int):
        """Ändrar x och y koordinaten på en entity med ett givet värde"""
        self.x += dx
        self.y += dy

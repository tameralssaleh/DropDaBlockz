import pygame
from colors import COLOR_MAP

class Square:
    def __init__(self, x: int, y: int, color: int = 0) -> "Square":
        self.x: int = x
        self.y: int = y
        self.square_size: int = 30
        self.color: int = color

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, COLOR_MAP[self.color], (self.x * self.square_size, self.y * self.square_size, self.square_size, self.square_size))

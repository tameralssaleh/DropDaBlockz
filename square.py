import pygame

class Square:
    def __init__(self, x: int, y: int, color: tuple[int, int, int] = None) -> "Square":
        self.x: int = x
        self.y: int = y
        self.square_size: int = 30
        self.color: tuple[int, int, int] = color

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, (self.x * self.square_size, self.y * self.square_size, self.square_size, self.square_size))
        
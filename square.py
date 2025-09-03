import pygame

class Square:
    def __init__(self, x: int, y: int, color: tuple[int, int, int] = None) -> "Square":
        self.x: int = x
        self.y: int = y
        self.color: tuple[int, int, int] = color

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, (self.x, self.y, 30, 30))
        
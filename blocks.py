import pygame
from random import choice
from square import Square
from colors import colors

class Block:
    def __init__(self, squares: list[Square], color: tuple[int, int, int] = None) -> "Block":
        # color will be None initially.. will be set later during runtime.
        self.squares: list[Square] = squares
        self.color: tuple[int, int, int] = color
        for square in self.squares:
            square.color = self.color

    def draw(self, surface: pygame.Surface) -> None:
        for square in self.squares:
            square.draw(surface)

    def move_right(self, velocity: int) -> None:
        for square in self.squares:
            square.x += velocity

    def move_left(self, velocity: int) -> None:
        for square in self.squares:
            square.x -= velocity

# Upside-down stair shape
block_squares_one: list[Square] = [
    Square(300, 0),
    Square(300, 30),
    Square(330, 0)
]

# 1x4 bar shape
block_squares_two: list[Square] = [
    Square(300, 0),
    Square(330, 0),
    Square(360, 0),
    Square(390, 0)
]

# 2x2 square shape
block_squares_three: list[Square] = [
    Square(300, 0),
    Square(300, 30),
    Square(330, 0),
    Square(330, 30)
]
# L shape
block_squares_four: list[Square] = [
    Square(300, 0),
    Square(300, 30),
    Square(300, 60),
    Square(330, 60)
]

block_squares: list[Square] = [block_squares_one, block_squares_two, block_squares_three, block_squares_four]
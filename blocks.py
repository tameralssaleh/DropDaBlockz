import pygame
from random import choice
from square import Square
from colors import block_colors

class Block:
    def __init__(self, squares: list[Square], color: tuple[int, int, int] = None) -> "Block":
        # color will be None initially.. will be set later during runtime.
        self.squares: list[Square] = squares
        self.color: tuple[int, int, int] = color
        self.can_move: bool = True
        self.is_falling: bool = True
        self.fast_falling: bool = False
        self.can_fall: bool = True
        self.is_settled: bool = False
        for square in self.squares:
            square.color = self.color

    def draw(self, surface: pygame.Surface) -> None:
        for square in self.squares:
            square.draw(surface)

    def move_right(self) -> None:
        for square in self.squares:
            square.x += 1

    def move_left(self) -> None:
        for square in self.squares:
            square.x -= 1

    def move_down(self) -> None:
        for square in self.squares:
            square.y += 1

block_squares_one: list[Square] = [
    Square(5, 0),
    Square(4, 0),
    Square(6, 0),
    Square(5, 1)
]

# 1x4 bar shape
block_squares_two: list[Square] = [
    Square(5, 0),
    Square(6, 0),
    Square(7, 0),
    Square(8, 0)
]

# 2x2 square shape
block_squares_three: list[Square] = [
    Square(5, 0),
    Square(5, 1),
    Square(6, 0),
    Square(6, 1)
]
# L shape
block_squares_four: list[Square] = [
    Square(5, 0),
    Square(5, 1),
    Square(5, 2),
    Square(6, 2)
]

block_squares_five: list[Square] = [
    Square(5, 1),
    Square(4, 1),
    Square(6, 1),
    Square(5, 0)
]

block_squares_six: list[Square] = [
    Square(5, 0),
    Square(5, 1),
    Square(6, 1),
    Square(6, 2)
]

block_squares_seven: list[Square] = [
    Square(6, 0),
    Square(6, 1),
    Square(5, 1),
    Square(5, 2)
]
 
block_squares: list[Square] = [
    block_squares_one, block_squares_two, 
    block_squares_three, block_squares_four,
    block_squares_five, block_squares_six,
    block_squares_seven
]
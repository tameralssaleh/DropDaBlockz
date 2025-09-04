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

    def move_right(self, velocity: int) -> None:
        for square in self.squares:
            square.x += velocity

    def move_left(self, velocity: int) -> None:
        for square in self.squares:
            square.x -= velocity

    def move_down(self, velocity: int) -> None:
        for square in self.squares:
            square.y += velocity

block_squares_one: list[Square] = [
    Square(300, 0),
    Square(270, 0),
    Square(330, 0),
    Square(300, 30)
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

block_squares_five: list[Square] = [
    Square(300, 30),
    Square(270, 30),
    Square(330, 30),
    Square(300, 0)
]

block_squares_six: list[Square] = [
    Square(300, 0),
    Square(300, 30),
    Square(330, 30),
    Square(330, 60)
]

block_squares_seven: list[Square] = [
    Square(330, 0),
    Square(330, 30),
    Square(300, 30),
    Square(300, 60)
]
 
block_squares: list[Square] = [
    block_squares_one, block_squares_two, 
    block_squares_three, block_squares_four,
    block_squares_five, block_squares_six,
    block_squares_seven
]
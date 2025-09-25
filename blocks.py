import pygame
from random import choice
from square import Square
from colors import block_colors
from copy import deepcopy

class Block:
    def __init__(self, squares: tuple[list[Square], str], color: tuple[int, int, int] = None) -> "Block":
        # color will be None initially.. will be set later during runtime.
        self.squares: tuple[list[Square], str] = squares
        self.color: tuple[int, int, int] = color
        self.can_move: bool = True
        self.is_falling: bool = True
        self.fast_falling: bool = False
        self.can_fall: bool = True
        self.is_settled: bool = False
        for square in self.squares[0]:
            square.color = self.color

    def draw(self, surface: pygame.Surface) -> None:
        for square in self.squares[0]:
            square.draw(surface)

    def move_right(self) -> None:
        for square in self.squares[0]:
            square.x += 1

    def move_left(self) -> None:
        for square in self.squares[0]:
            square.x -= 1

    def move_down(self) -> None:
        for square in self.squares[0]:
            square.y += 1

    def hard_drop(self) -> None:
        ...

    def rotate(self) -> None:
        # General formula for rotating a point (x, y) around a pivot (px, py) by 90 degrees counter-clockwise:
        # (x', y') = (-y + pivot_x, x + pivot_y)

        pivot = self.squares[0][1]  # Using the second square as the pivot

        for square in self.squares[0]:

            # Translate to pivot
            rel_x = square.x - pivot.x
            rel_y = square.y - pivot.y

            # Rotate 90 degrees counter-clockwise
            new_x = -rel_y
            new_y = rel_x

            # Translate back
            square.x = new_x + pivot.x
            square.y = new_y + pivot.y


block_squares_one: tuple[list[Square], str] = (
    [
        Square(4, 0),
        Square(5, 0),
        Square(6, 0),
        Square(5, 1)
    ],
    "T_Shape"
)

# 1x4 bar shape
block_squares_two: tuple[list[Square], str] = (
    [
    Square(5, 0),
    Square(6, 0),
    Square(7, 0),
    Square(8, 0)
    ],
    "I_Shape"
)

# 2x2 square shape
block_squares_three: tuple[list[Square], str] = (
    [
    Square(5, 0),
    Square(5, 1),
    Square(6, 0),
    Square(6, 1)
],  
    "Square_Shape"
)
# L shape
block_squares_four: tuple[list[Square], str] = (
    [
    Square(5, 0),
    Square(5, 1),
    Square(5, 2),
    Square(6, 2)
],
    "L_Shape"
)

block_squares_five: tuple[list[Square], str] = (
    [
        Square(5, 0),
        Square(5, 1),
        Square(4, 1),
        Square(6, 1)
    ],
    "T_Shape2"
)

block_squares_six: tuple[list[Square], str] = (
    [
        Square(5, 0),
        Square(5, 1),
        Square(6, 1),
        Square(6, 2)
    ],
    "S_Shape"
)

block_squares_seven: tuple[list[Square], str] = (
    [
        Square(6, 0),
        Square(6, 1),
        Square(5, 1),
        Square(5, 2)
    ],
    "Z_Shape"
)
 
block_squares: tuple[list[Square], str] = [
    block_squares_one, block_squares_two, 
    block_squares_three, block_squares_four,
    block_squares_five, block_squares_six,
    block_squares_seven
]
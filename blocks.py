import pygame
from random import choice
from game import Game
from square import Square
from colors import *
from copy import deepcopy

class Block:
    def __init__(self, squares: tuple[list[Square], str], color: int) -> "Block":
        # color will be None initially.. will be set later during runtime.
        self.squares: tuple[list[Square], str] = squares
        self.color: int = color
        self.can_move: bool = True
        self.is_falling: bool = True
        self.fast_falling: bool = False
        self.can_fall: bool = True
        self.is_settled: bool = False
        for square in self.squares[0]:
            square.color = self.color
        self.hard_drop_offset: int = 0 # How far the block will fall on hard drop

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
        for square in self.squares[0]:
            square.y += self.hard_drop_offset
        self.is_settled = True

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

    def can_move_left(self):
        for square in self.squares[0]:
            next_pos = (square.x - 1, square.y)
            if next_pos[0] < Game.get_instance().x_boundary[0] or Game.get_instance().gameboard.unified_grid[next_pos[1]][next_pos[0]]:
                return False
        return True

    def can_move_right(self):
        for square in self.squares[0]:
            next_pos = (square.x + 1, square.y)
            if next_pos[0] > Game.get_instance().x_boundary[1] or Game.get_instance().gameboard.unified_grid[next_pos[1]][next_pos[0]]:
                return False
        return True
    
    def set_hard_drop_offset(self):
        lowest_square_y = max(square.y for square in self.squares[0])
        y_offset = 19 - lowest_square_y  # get largest possible offset
        for offset in range(y_offset + 1):
            collision = False
            for square in self.squares[0]:
                if Game.get_instance().gameboard.unified_grid[square.y + offset][square.x] or (square.y + offset) > 19:
                    collision = True
                    break
            if collision:
                self.hard_drop_offset = offset - 1 # Set to last valid offset
                return
        self.hard_drop_offset = y_offset # If no collision, set to max possible offset
    
    def draw_hard_drop(self):
        for square in self.squares[0]:
            pygame.draw.rect(
                Game.get_instance().gameboard.surface,
                COLOR_MAP[square.color],
                pygame.Rect(
                    square.x * Game.get_instance().square_size,
                    (square.y + self.hard_drop_offset) * Game.get_instance().square_size,
                    Game.get_instance().square_size,
                    Game.get_instance().square_size
                ),
                1  # Draw only the border
            )

    def can_move_down(self):
        for square in self.squares[0]:
            next_pos = (square.x, square.y + 1)
            # Hit bottom?
            if next_pos[1] > Game.get_instance().y_boundary[1] or Game.get_instance().gameboard.unified_grid[next_pos[1]][next_pos[0]]:
                print("Hit bottom")
                return False
            # Hit another block?
            # if Game.get_instance().gameboard.unified_grid[next_pos[1]][next_pos[0]]:
            #     print("Hit another block")
            #     return False
        return True

    def can_rotate(self) -> bool:
        squares, _ = self.squares
        pivot = squares[1]   # always the pivot

        block_copy = deepcopy(self)
        copy_squares, _ = block_copy.squares

        for square in copy_squares:
            # Translate to pivot
            rel_x = square.x - pivot.x
            rel_y = square.y - pivot.y

            # Rotate 90 degrees counter-clockwise
            rotated_x = -rel_y + pivot.x
            rotated_y = rel_x + pivot.y
            try:
                cell = Game.get_instance().gameboard.unified_grid[rotated_y][rotated_x]
            except IndexError:
                return False
            # Check collisions/bounds
            if cell:
                return False
            if rotated_x < Game.get_instance().x_boundary[0] or rotated_x > Game.get_instance().x_boundary[1]:
                return False
            if rotated_y < Game.get_instance().y_boundary[0] or rotated_y > Game.get_instance().y_boundary[1]:
                return False
        return True


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
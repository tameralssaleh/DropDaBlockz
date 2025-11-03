import pygame
from random import choice, randint, shuffle
from game import Game
from colors import *

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],                                  # I
    [[1, 0, 0], [1, 1, 1]],                          # J
    [[0, 0, 1], [1, 1, 1]],                          # L
    [[1, 1], [1, 1]],                                # O
    [[0, 1, 1], [1, 1, 0]],                          # S
    [[0, 1, 0], [1, 1, 1]],                          # T
    [[1, 1, 0], [0, 1, 1]]                           # Z
]

# For all blocks except I and O
JLSTZ_KICKS = [(0, 0), (1, 0), (1, 2), (1, -2), (-1, 0), (-1, -2), (-1, 2)]
# {
#     (0, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
#     (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
#     (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
#     (2, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
#     (2, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
#     (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
#     (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
#     (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]
# }

# For I block (different kick data)
I_KICKS = [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2), (1, -2), (-2, 1), (2, 0), (-1, 0), (2, 1), (-1, -2), (-1, 2), (2, -1)]
    # (1, 0): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    # (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    # (2, 1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)], # (-2, -1), (1, 2), (2, 0), (-1, 0), (2, 1), (-1, -2), (-1, 2), (2, -1)
    # (2, 3): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)], # (-2, 0), (1, 0), (-2, -1), (1, 2), (1, -2), (-2, 1), (-1, 2), (2, -1)
    # (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    # (3, 0): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    # (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)]  # (-2, 0), (1, 0), (-2, -1), (1, 2), (1, -2), (-2, 1), (2, 1), (-1, -2)
#}

# Piece class
class Block:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = randint(0,6) + 1
        self.rotation = 0  # 0 = spawn, 1 = right, 2 = 180, 3 = left

    def rotated_shape(self):
        # Return a rotated version of the shape according to rotation state
        shape = self.shape
        for _ in range(self.rotation % 4):
            shape = [list(row) for row in zip(*shape[::-1])]
        return shape
    
    def draw(self, gameboard):
        for i, row in enumerate(self.rotated_shape()):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(gameboard.surface, COLOR_MAP[self.color], ((self.x+j)*gameboard.cell_size, (self.y+i)*gameboard.cell_size, gameboard.cell_size, gameboard.cell_size))

    def draw_drop_preview(self, board):
        y = self.y
        while board.valid_transform(self):
            self.y += 1
        self.y -= 1
        for i, row in enumerate(self.rotated_shape()):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(board.surface, COLOR_MAP[self.color], ((self.x+j)*board.cell_size, (self.y+i)*board.cell_size, board.cell_size, board.cell_size), 4)
        self.y = y

    @staticmethod
    def get_new_block():
        return Block(10 // 2 - 2, 0, choice(SHAPES)) #hard coded Columns: 10
    
    @staticmethod
    def get_shuffled_blocks():
        blocks = [Block(1,1, shape) for shape in SHAPES]
        shuffle(blocks)
        return blocks

class BlockQueue:
    def __init__(self):
        self.blocks: list[Block] = Block.get_shuffled_blocks()
    
    def get_next(self):
        next = self.blocks.pop(0)
        if len(self.blocks) < 4:
            self.blocks.extend(Block.get_shuffled_blocks())
        next.x, next.y = 10//2 - 2, 0
        return next
    
    def draw(self, grid):
        for i,blocks in enumerate(self.blocks):
            blocks.y = (i * 4) + 1
            blocks.draw(grid)

class BlockController:
    def __init__(self):
        self.current_block = None

    def set_block(self, block):
        self.current_block = block
    
    def clear_block(self):
        self.current_block = None

    def move_block_horizontal(self, direction):
        self.current_block.x += direction
        if not Game._instance.gameboard.valid_transform(self.current_block):
            self.current_block.x -= direction
    
    def try_move_down(self):
        self.current_block.y += 1
        if not Game._instance.gameboard.valid_transform(self.current_block):
            self.current_block.y -= 1
            return False
        return True
    
    def hard_drop(self):
        while Game._instance.gameboard.valid_transform(self.current_block):
            self.current_block.y += 1
        self.current_block.y -= 1
        
    def rotate_block(self, direction=1):
        """
        direction: +1 for clockwise, -1 for counterclockwise
        """
        old_rotation = self.current_block.rotation
        self.current_block.rotation = (self.current_block.rotation + direction) % 4

        # Determine which kick table to use
        if self.current_block.shape == SHAPES[0]:  # I-block
            kicks = I_KICKS#.get((old_rotation, self.current_block.rotation), [(0, 0)])
        elif self.current_block.shape == SHAPES[3]:  # O-block (no kicks needed)
            kicks = [(0, 0)]
        else:
            kicks = JLSTZ_KICKS#.get((old_rotation, self.current_block.rotation), [(0, 0)])

        for dx, dy in kicks:
            self.current_block.x += dx
            self.current_block.y += dy
            if Game._instance.gameboard.valid_transform(self.current_block):
                return True  # Successful rotation
            self.current_block.x -= dx
            self.current_block.y -= dy

        # Revert if all kicks fail
        self.current_block.rotation = old_rotation
        return False
    
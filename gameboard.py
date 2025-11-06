import pygame
from colors import *
from game import Game


class GameBoard:
    def __init__(self, size=(300,600), midtop=(300,0), cell_size=30, columns = 10, rows = 20):
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(midtop = midtop)
        self.cell_size = cell_size
        self.columns = columns
        self.rows = rows
        self.unified_grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)] # grid [y][x]

    def draw(self):
        self.surface.fill((0,0,0))
        self.draw_blocks()
        game = Game.get_instance()
        if game.controller.current_block:
            game.controller.current_block.draw(self)
            game.controller.current_block.draw_drop_preview()
        self.draw_grid()
    
    def draw_grid(self):
        for x in range(0, self.rect.width, self.cell_size):
            pygame.draw.line(self.surface, GRID_LINES_COLOR, (x, 0), (x, self.rect.height))
        for y in range(0, self.rect.height, self.cell_size):
            pygame.draw.line(self.surface, GRID_LINES_COLOR, (0, y), (self.rect.width, y))

    def draw_blocks(self):
        self.surface.fill(BLACK)
        for y in range(self.rows):
            for x in range(self.columns):
                if self.unified_grid[y][x]:
                    cell_color = COLOR_MAP[self.unified_grid[y][x]]
                    cell_rect = (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.surface, cell_color, cell_rect)

    def clear(self):
        self.unified_grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def find_full_rows(self):
        full_rows = []
        for i in range(self.rows):
            if min(cell for cell in self.unified_grid[i]):
                full_rows.append(i)
        return full_rows
    
    def clear_rows(self, rows):
        for row in rows:
            del self.unified_grid[row]
            self.unified_grid.insert(0, [0 for _ in range(self.columns)])

    def valid_transform(self, block):
        for i, row in enumerate(block.rotated_shape()):
            for j, cell in enumerate(row):
                if cell:
                    x, y = block.x + j, block.y + i
                    if x < 0 or x >= self.columns or y >= self.rows:
                        return False
                    if y >= 0 and self.unified_grid[y][x] != 0:
                        return False
        return True
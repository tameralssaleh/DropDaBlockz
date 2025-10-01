import pygame
from colors import *


class GameBoard:
    def __init__(self, size=(300,600), midtop=(300,0), cell_size=30):
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(midtop = midtop)
        self.cell_size = cell_size
        self.unified_grid = [[0 for _ in range(10)] for _ in range(20)] # grid [y][x]
        #self.occupied_positions = set()
        #self.settled_blocks = []

    def draw(self):
        self.surface.fill((0,0,0))
        self.draw_blocks()
        self.draw_grid()
    
    def draw_grid(self):
        for x in range(0, self.rect.width, self.cell_size):
            pygame.draw.line(self.surface, GRID_LINES_COLOR, (x, 0), (x, self.rect.height))
        for y in range(0, self.rect.height, self.cell_size):
            pygame.draw.line(self.surface, GRID_LINES_COLOR, (0, y), (self.rect.width, y))

    def draw_blocks(self):
        for y in range(20):
            for x in range(10):
                if self.unified_grid[y][x]:
                    pygame.draw.rect(self.surface, COLOR_MAP[self.unified_grid[y][x]], (x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))

    def blit(self, surface, rect):
        self.surface.blit(surface,rect)

    def clear(self):
        #self.occupied_positions.clear()
        #self.settled_blocks.clear()
        self.unified_grid = [[0 for _ in range(10)] for _ in range(20)]

    def find_full_rows(self):
        full_rows = []
        for i in range(20):
            if min(cell for cell in self.unified_grid[i]):
                full_rows.append(i)
        return full_rows
    
    def clear_rows(self, rows):
        for row in rows:
            del self.unified_grid[row]
            self.unified_grid.insert(0, [0 for _ in range(10)])
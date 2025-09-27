import pygame
from colors import *


class GameBoard:
    def __init__(self, size=(300,600), midtop=(300,0), cell_size=30):
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(midtop = midtop)
        self.cell_size = cell_size
        self.occupied_positions = set()
        self.settled_blocks = []

    
    def draw(self):
        self.surface.fill((0,0,0))
        for x in range(0, self.rect.width, self.cell_size):
            pygame.draw.line(self.surface, GRID_LINES_COLOR, (x, 0), (x, self.rect.height))
        for y in range(0, self.rect.height, self.cell_size):
            pygame.draw.line(self.surface, GRID_LINES_COLOR, (0, y), (self.rect.width, y))

    def blit(self, surface, rect):
        self.surface.blit(surface,rect)

    def clear(self):
        self.occupied_positions.clear()
        self.settled_blocks.clear()
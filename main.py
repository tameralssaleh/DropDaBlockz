import pygame
from random import choice
from blocks import block_squares, Block
from colors import colors

###### Game Variables

# Screen Dimensions; allows for 10 40x40 px squares per row with 30 rows in total.

SCREEN_SIZE: tuple[int, int] = (600, 600)
SCREEN_WIDTH: int = SCREEN_SIZE[0]
SCREEN_HEIGHT: int = SCREEN_SIZE[1]
SQUARE_SIZE: int = 30
X_BOUNDARY: tuple[int, int] = (150, SCREEN_WIDTH - 150 - SQUARE_SIZE)
Y_BOUNDARY: tuple[int, int] = (0, SCREEN_HEIGHT - SQUARE_SIZE)
GRID_SIZE: int = 30
VELOCITY: int = SQUARE_SIZE # We want blocks to move evenly.

player_x_pos = 300
player_y_pos = 30

### Colors
DARK_GRAY: tuple[int, int, int] = (48, 48, 48)
GRID_LINES_COLOR: tuple[int, int, int] = (16, 16, 16)

# Other colors are in colors.py file. (these colors are for the player blocks)

# Flags
running: bool = True
game_active: bool = False
game_over: bool = False
can_move: bool = True

# Clock
FPS: int = 10
clock: pygame.time.Clock = pygame.time.Clock()

### Initialization

pygame.init()
window: pygame.Surface = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Drop da blockz")

def draw_board_frame():
    # Fill background
    window.fill((0, 0, 0))
    # Draw grid lines
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(window, GRID_LINES_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(window, GRID_LINES_COLOR, (0, y), (SCREEN_WIDTH, y))
    # Draw sidebars
    pygame.draw.rect(window, DARK_GRAY, (0, 0, 150, SCREEN_HEIGHT))  # Left Sidebar
    pygame.draw.rect(window, DARK_GRAY, (SCREEN_WIDTH - 150, 0, 150, SCREEN_HEIGHT))  # Right Sidebar

### Game Loop

# Create new randomized block
block_color = choice(colors)
block_squares_list = choice(block_squares)
block = Block(block_squares_list, block_color)

while running:
    can_move = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        for square in block.squares:
            if square.x - VELOCITY < X_BOUNDARY[0]:
                can_move = False
                break
        if can_move:
            block.move_left(VELOCITY)

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        for square in block.squares:
            if square.x + VELOCITY > X_BOUNDARY[1]:
                can_move = False
                break
        if can_move:
            block.move_right(VELOCITY)

    draw_board_frame()
    block.draw(window)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()


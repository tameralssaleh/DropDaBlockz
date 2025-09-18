import pygame
from states import GameRunningState
# from random import choice
# from copy import deepcopy
# from blocks import block_squares, Block
# from colors import block_colors, DARK_GRAY, GRID_LINES_COLOR

###### Game Variables

# Screen Dimensions; allows for 10 30x30 px squares per row with 20 rows in total.

SCREEN_SIZE: tuple[int, int] = (600, 600)
SCREEN_WIDTH: int = SCREEN_SIZE[0]
SCREEN_HEIGHT: int = SCREEN_SIZE[1]
SQUARE_SIZE: int = 30
X_BOUNDARY: tuple[int, int] = (150, 450 - SQUARE_SIZE) 
Y_BOUNDARY: tuple[int, int] = (0, 600)
GRID_SIZE: int = 30
VELOCITY: int = SQUARE_SIZE # We want blocks to move evenly.
# X and Y coordinates are relative to the X and Y **pixel** coordinates. this means that at x=300px, y=0px, the true coordinate is (3,0)
GAME_BOARD_SIZE: tuple[int, int] = (300, 600)
GAME_BOARD_LOCATION: tuple[int, int] = (150, 0) # Top-left corner of game board

game_board_coordinates = [
    (x // SQUARE_SIZE, y // SQUARE_SIZE)
    for y in range(Y_BOUNDARY[0], Y_BOUNDARY[1], SQUARE_SIZE)
    for x in range(X_BOUNDARY[0], X_BOUNDARY[1] + SQUARE_SIZE, SQUARE_SIZE)
]

print(game_board_coordinates)

game_board = pygame.Surface(GAME_BOARD_SIZE)
game_board.fill((0, 0, 0))

# active_blocks: list[Block] = []
# occupied_positions: set = set()

# Other colors are in colors.py file. (these colors are for the player blocks)

# Flags
running: bool = True
game_active: bool = False
game_over: bool = False

# Clock
FPS: int = 15
# clock: pygame.time.Clock = pygame.time.Clock()
# frame_count: int = 0

### Initialization

pygame.init()
window: pygame.Surface = pygame.display.set_mode(SCREEN_SIZE)

grs = GameRunningState(None)
grs.screen_width = SCREEN_WIDTH
grs.screen_height = SCREEN_HEIGHT
grs.frame_rate = FPS
grs.x_boundary = X_BOUNDARY
grs.y_boundary = Y_BOUNDARY
grs.velocity = VELOCITY
grs.square_size = SQUARE_SIZE
grs.grid_size = GRID_SIZE
grs.game_board = game_board
grs.game_board_location = GAME_BOARD_LOCATION
grs.enter()

# pygame.display.set_caption("Drop da blockz")

### Helper functions for collisions

# def can_move_down(block: Block):
#     for square in block.squares:
#         next_pos = (square.x, square.y + SQUARE_SIZE)
#         if next_pos in occupied_positions or next_pos[1] >= Y_BOUNDARY[1]:
#             return False
#     return True

# def can_move_left(block: Block):
#     for square in block.squares:
#         next_pos = (square.x - SQUARE_SIZE, square.y)
#         if next_pos[0] < X_BOUNDARY[0] or next_pos in occupied_positions:
#             return False
#     return True

# def can_move_right(block: Block):
#     for square in block.squares:
#         next_pos = (square.x + SQUARE_SIZE, square.y)
#         if next_pos[0] > X_BOUNDARY[1] or next_pos in occupied_positions:
#             return False
#     return True

# def draw_board():
#     # Fill background
#     window.fill((0, 0, 0))
#     # Draw grid lines
#     for x in range(0, SCREEN_WIDTH, GRID_SIZE):
#         pygame.draw.line(window, GRID_LINES_COLOR, (x, 0), (x, SCREEN_HEIGHT))
#     for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
#         pygame.draw.line(window, GRID_LINES_COLOR, (0, y), (SCREEN_WIDTH, y))
#     # Draw sidebars
#     pygame.draw.rect(window, DARK_GRAY, (0, 0, 150, SCREEN_HEIGHT))  # Left Sidebar
#     pygame.draw.rect(window, DARK_GRAY, (SCREEN_WIDTH - 150, 0, 150, SCREEN_HEIGHT))  # Right Sidebar

# # Create new randomized block
# block_color = deepcopy(choice(block_colors))
# block_squares_list = deepcopy(choice(block_squares))
# current_block = Block(block_squares_list, block_color) 

### Game Loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    grs.handle_events(window)
    grs.update(window)

    # # Check if blocks have reached top of board

    # for positions in occupied_positions:
    #     y_position = positions[1]
    #     if y_position - SQUARE_SIZE <= 0:
    #         game_over = True
    #         running = False   

    # if current_block.is_settled:
    #     for square in current_block.squares:
    #         occupied_positions.add((square.x, square.y))
    #     active_blocks.append(current_block)
    #     # Make new block
    #     block_color = deepcopy(choice(block_colors))
    #     block_squares_list = deepcopy(choice(block_squares))
    #     current_block = Block(block_squares_list, block_color)

    # keys = pygame.key.get_pressed()

    # # Handle left/right movement
    # if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    #     if can_move_left(current_block) and frame_count % 4 == 0:
    #         current_block.move_left(VELOCITY)

    # if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    #     if can_move_right(current_block) and frame_count % 4 == 0: 
    #         current_block.move_right(VELOCITY)

    # Handle fast-fall
    # fast_fall = keys[pygame.K_SPACE] or keys[pygame.K_s] or keys[pygame.K_DOWN]

    # # Move block down
    # if frame_count % (1 if fast_fall else 10) == 0:
    #     if can_move_down(current_block):
    #         current_block.move_down(VELOCITY)
    #     else:
    #         # Block has settled into place
    #         current_block.is_settled = True   

    # # Draw game board
    # draw_board()

    # # Draw all active blocks that had reached the bottom
    # for block in active_blocks:
    #     block.draw(window)

    # # Display block/tetromino
    # current_block.draw(window)

    # # Update display
    # pygame.display.flip()

    # clock.tick(FPS)
    # frame_count += 1

pygame.quit()

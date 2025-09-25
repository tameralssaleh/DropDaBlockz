import pygame
from states import GameRunningState 

###### Game Variables

# Screen Dimensions; allows for 10 30x30 px squares per row with 20 rows in total.

SCREEN_SIZE: tuple[int, int] = (600, 600)
SCREEN_WIDTH: int = SCREEN_SIZE[0]
SCREEN_HEIGHT: int = SCREEN_SIZE[1]
SQUARE_SIZE: int = 30
X_BOUNDARY: tuple[int, int] = (0, 9) 
Y_BOUNDARY: tuple[int, int] = (0, 19)
GRID_SIZE: int = 30
VELOCITY: int = SQUARE_SIZE # We want blocks to move evenly.
# X and Y coordinates are relative to the X and Y **pixel** coordinates. this means that at x=300px, y=0px, the true coordinate is (3,0)
GAME_BOARD_SIZE: tuple[int, int] = (300, 600)
GAME_BOARD_LOCATION: tuple[int, int] = (150, 0) # Top-left corner of game board
FPS: int = 15

# game_board_coordinates = [
#     (x // SQUARE_SIZE, y // SQUARE_SIZE)
#     for y in range(Y_BOUNDARY[0], Y_BOUNDARY[1], SQUARE_SIZE)
#     for x in range(X_BOUNDARY[0], X_BOUNDARY[1] + SQUARE_SIZE, SQUARE_SIZE)
# ]

# print(game_board_coordinates)

game_board = pygame.Surface(GAME_BOARD_SIZE)
game_board.fill((0, 0, 0))

# Flags
running: bool = True
game_active: bool = False
game_over: bool = False

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

### Game Loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        grs.handle_events(event)
        
    grs.update()
    grs.render(window)

    pygame.display.flip()

pygame.quit()

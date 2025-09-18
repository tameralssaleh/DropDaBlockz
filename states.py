import pygame
from blocks import Block, block_squares
from colors import *
from copy import deepcopy
from random import choice

class GameStateMachine():
    def __init__(self):
        self.current = None
        self.state_map = dict()

    def register_states(self, new_states): # new_states is a dict<string, GameState>
        self.state_map.update(new_states)

    def change_state(self, state):
        if self.current:
            self.current.exit()
        self.current = self.state_map[state.__name__]
        self.current.enter()

    def handle_events(self, event):
        self.current.handle_events(event)

    def update(self):
        self.current.update()

    def render(self, screen): # Render (draw) content on screen.
        self.current.render(screen)

class GameState: # base class for states
    def __init__(self, machine):
        self.machine = machine

    def __repr__(self):
        return f"{self.name}:{'active' if self.machine.current is self else 'inactive'}"
    
    def __str__(self):
        return self.__repr__()
    
    def enter(self):
        pass

    def exit(self):
        print(f"Exiting {type(self).__name__}")

    def update(self):
        pass

    def handle_events(self, event):
        pass

    def render(self, screen):
        pass

class GameRunningState(GameState):
    def __init__(self, machine):
        self.header = "Drop Da Blockz"
        # The following properties are not native to state machines, but are necessary for the game to function.
        self.screen_width: int = None
        self.screen_height: int = None
        self.square_size: int = None
        self.grid_size: int = None
        self.game_board: pygame.Surface = None
        self.game_board_location: tuple[int, int] = None
        self.velocity: int = None
        self.frame_count: int = 0
        self.frame_rate: int = None
        self.clock = pygame.time.Clock()
        self.current_block: Block = None
        self.x_boundary: tuple[int, int] = None
        self.y_boundary: tuple[int, int] = None
        self.occupied_positions: set = set()
        self.settled_blocks: list[Block] = []

    def enter(self) -> None:
        pygame.display.set_caption(self.header)
        block_color = deepcopy(choice(block_colors))
        block_squares_list = deepcopy(choice(block_squares))
        current_block = Block(block_squares_list, block_color) 
        self.current_block = current_block

    def can_move_left(self, block: Block):
        for square in block.squares:
            next_pos = (square.x - 1, square.y)
            if next_pos[0] < self.x_boundary[0] or next_pos in self.occupied_positions:
                return False
        return True

    def can_move_right(self, block: Block):
        for square in block.squares:
            next_pos = (square.x + 1, square.y)
            if next_pos[0] > self.x_boundary[1] or next_pos in self.occupied_positions:
                return False
        return True

    def can_move_down(self, block: Block):
        for square in block.squares:
            next_pos = (square.x, square.y + 1)
            # Hit bottom?
            if next_pos[1] > self.y_boundary[1]:
                return False
            # Hit another block?
            if next_pos in self.occupied_positions:
                return False
        return True
    
    def render(self, screen: pygame.Surface) -> None:
        # Clear everything
        screen.fill((0, 0, 0))
        self.game_board.fill((0, 0, 0))  # clear game board too

        # Draw grid lines (on game board first)
        for x in range(0, self.game_board.get_width(), self.grid_size):
            pygame.draw.line(self.game_board, GRID_LINES_COLOR, (x, 0), (x, self.game_board.get_height()))
        for y in range(0, self.game_board.get_height(), self.grid_size):
            pygame.draw.line(self.game_board, GRID_LINES_COLOR, (0, y), (self.game_board.get_width(), y))

        # Draw settled blocks
        for block in self.settled_blocks:
            block.draw(self.game_board)

        # Draw current falling block
        if self.current_block:
            self.current_block.draw(self.game_board)

        screen.blit(self.game_board, self.game_board_location)

        # Draw sidebars
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, 150, self.screen_height))  # Left Sidebar
        pygame.draw.rect(screen, DARK_GRAY, (self.screen_width - 150, 0, 150, self.screen_height))  # Right Sidebar

    def update(self, screen) -> None:
        # Handle fast-fall
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        fast_fall = keys[pygame.K_SPACE] or keys[pygame.K_s] or keys[pygame.K_DOWN]
        
        # Move block down
        if self.frame_count % (1 if fast_fall else 10) == 0:
            if self.can_move_down(self.current_block):
                self.current_block.move_down(self.velocity)
            else:
                # Block has settled into place
                self.current_block.is_settled = True   
    # Check if blocks have reached top of board

        for positions in self.occupied_positions:
            y_position = positions[1]
            if y_position - self.square_size <= 0:
                game_over = True
                running = False   
                # Do not set these flags, enter the respective states.

        if self.current_block.is_settled:
            for square in self.current_block.squares:
                self.occupied_positions.add((square.x, square.y))
            self.settled_blocks.append(self.current_block)
            # Make new block
            block_color = deepcopy(choice(block_colors))
            block_squares_list = deepcopy(choice(block_squares))
            self.current_block = Block(block_squares_list, block_color)

        self.clock.tick(self.frame_rate)
        self.frame_count += 1

    def handle_events(self, screen) -> None:
        # Function to keyboard events.

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        
        # Handle left/right movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.can_move_left(self.current_block) and self.frame_count % 4 == 0:
                self.current_block.move_left(self.velocity)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.can_move_right(self.current_block) and self.frame_count % 4 == 0: 
                self.current_block.move_right(self.velocity)



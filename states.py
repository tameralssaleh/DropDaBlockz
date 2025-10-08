import pygame
from blocks import Block, block_squares
from colors import *
from copy import deepcopy
from random import choice, randint
from time import time
from game import Game

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

    def render(self): # Render (draw) content on screen.
        self.current.render()

    def initialize(self):
        self.register_states({"StartScreen": StartScreen(), 
                              "TransitionState": TransitionState(), 
                              "GameRunningState": GameRunningState(),
                              "PauseState": PauseState()})
        self.change_state(StartScreen)

class GameState: # base class for states
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

    def render(self):
        pass

class PauseState(GameState):
    def __init__(self):
        self.text = Game.get_instance().lg_font.render("PAUSED", True, '#FFFFFF')
        self.text_rect = self.text.get_rect(center = Game.get_instance().screen.get_rect().center)
    
    def enter(self):
        Game.get_instance().screen.blit(self.text, self.text_rect)
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.get_instance().state_machine.change_state(GameRunningState)

class TransitionState(GameState):
    def __init__(self):
        self.tick = 5
        
    def enter(self):
        Game.get_instance().screen.fill((0, 0, 0))
        Game.get_instance().gameboard.clear()

    def update(self):
        self.tick -= 1
        if not self.tick:
            Game.get_instance().state_machine.change_state(GameRunningState)

    def exit(self):
        self.tick = 5

class StartScreen(GameState):
    def __init__(self):
        self.text = Game.get_instance().lg_font.render("Press SPACE to start", True, '#FFFFFF')
        self.text_rect = self.text.get_rect(center = Game.get_instance().screen.get_rect().center)

    def enter(self):
        Game.get_instance().screen.fill("#0000FF")
        Game.get_instance().screen.blit(self.text, self.text_rect)
        pass

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Game.get_instance().state_machine.change_state(TransitionState)

class GameRunningState(GameState):
    def __init__(self):
        self.header = "Drop Da Blockz"
        # The following properties are not native to state machines, but are necessary for the game to function.
        self.current_block: Block = None
        self.frame_count: int = 0
        self.gravity_timer: float = time()
        self.input_timer: float = time()
        self.time_buffer: float = 0.3
        self.gravity_buffer: float = 0.5  # Time in seconds between automatic downward movements of the block.

    def enter(self) -> None:
        pygame.display.set_caption(self.header)
        Game.get_instance().screen.fill(DARK_GRAY)
        if not self.current_block:
            block_squares_list = deepcopy(choice(block_squares))
            current_block = Block(block_squares_list, randint(1, 7)) # Random color from COLOR_MAP (1-7)
            self.current_block = current_block
    
    def render(self) -> None:
        Game.get_instance().gameboard.draw() # Draw gameboard surface grid and settled blocks
        # Draw current falling block
        if self.current_block:
            self.current_block.draw(Game.get_instance().gameboard.surface)

        self.current_block.draw_hard_drop()
        Game.get_instance().screen.blit(Game.get_instance().gameboard.surface, Game.get_instance().gameboard.rect)

    def update(self) -> None:
        # Handle fast-fall
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if time() - self.input_timer > self.time_buffer:
                if self.current_block.can_move_left():
                    self.current_block.move_left()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if time() - self.input_timer > self.time_buffer:
                if self.current_block.can_move_right():
                    self.current_block.move_right()

        if keys[pygame.K_r]:
            if time() - self.input_timer > self.time_buffer:
                if self.current_block.squares[1] == "Square_Shape":  # 2x2 square shape does not rotate
                    return
                if self.current_block.can_rotate():
                    self.current_block.rotate()

    # Move block down
        if time() - self.gravity_timer > self.gravity_buffer:
            self.gravity_timer = time()
            # if self.frame_count % (1 if fast_fall else 10) == 0:
            if self.current_block.can_move_down():
                self.current_block.move_down()
            else:
                # Block has settled into place
                self.current_block.is_settled = True 
    
        self.current_block.set_hard_drop_offset()

        if self.current_block.is_settled:                    
            print("Block settled")
            for square in self.current_block.squares[0]:
                Game.get_instance().gameboard.unified_grid[square.y][square.x] = self.current_block.color
                # Game.get_instance().gameboard.occupied_positions.add((square.x, square.y))
                # Game.get_instance().gameboard.settled_blocks.append(self.current_block)
            full_rows = Game.get_instance().gameboard.find_full_rows()
            Game.get_instance().gameboard.clear_rows(full_rows)
            Game.get_instance().gameboard.score += 100
            print(f"Score: {Game.get_instance().gameboard.score}")
            # Make new block
            block_squares_list = deepcopy(choice(block_squares))
            self.current_block = Block(block_squares_list, randint(1, 7)) # Random color from COLOR_MAP (1-7)
            for square in self.current_block.squares[0]:
                if Game.get_instance().gameboard.unified_grid[square.y][square.x]:
                    print("Game Over")
                    Game.get_instance().state_machine.change_state(StartScreen)
                    return
            
    def handle_events(self, event: pygame.event.Event) -> None:
        # Function to manage keyboard events.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.get_instance().state_machine.change_state(PauseState)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if self.current_block.can_move_left():
                    self.current_block.move_left()
                    self.input_timer = time()  

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if self.current_block.can_move_right():
                    self.current_block.move_right()
                    self.input_timer = time()    
                  
            if event.key == pygame.K_r:
                if self.current_block.squares[1] == "Square_Shape":  # 2x2 square shape does not rotate
                    return
                if self.current_block.can_rotate():
                    self.current_block.rotate()
                    self.input_timer = time()
            
            if event.key == pygame.K_SPACE:
                self.current_block.hard_drop()

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.gravity_buffer = 0.05

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.gravity_buffer = 0.5




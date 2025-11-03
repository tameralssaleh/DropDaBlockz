import pygame
from colors import *
from random import choice, randint
from time import time
from game import Game
from blocks import Block, BlockQueue
from highscore import add_highscore, load_highscores

class GameStateMachine():
    def __init__(self):
        self.current = None
        self.state_map = dict()
        self.state_stack = []
    
    def register_states(self, new_states): # new_states is a dict<string, GameState>
        self.state_map.update(new_states)

    def change_state(self, state):
        if self.current:
            self.current.exit()
        self.current = self.state_map[state.__name__]
        self.current.enter()

    def enter_sub_state(self, state):
        if self.current:
            self.state_stack.append(self.current)
        self.current = self.state_map[state.__name__]
        self.current.enter()

    def exit_sub_state(self):
        if self.current:
            self.current.exit()
        self.current = self.state_stack.pop()

    def handle_events(self, event):
        self.current.handle_events(event)

    def update(self):
        self.current.update()

    def render(self): # Render (draw) content on screen.
        self.current.render()

    def initialize(self):
        self.register_states({"StartScreen": StartScreen(), 
                              "GameOverState": GameOverState(), 
                              "GameRunningState": GameRunningState(),
                              "PauseState": PauseState(),
                              "ConfirmInitials": ConfirmInitials(),
                              "HighScoreBoard": HighScoreBoard()})
        self.change_state(StartScreen)

    def peek_state(self, state):
        return self.state_map[state.__name__]

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
                Game.get_instance().state_machine.exit_sub_state()
            elif event.key == pygame.K_x:
                Game.get_instance().gameboard.clear()

class ConfirmInitials(GameState):
    def enter(self):
        Game.get_instance().screen.fill(BLACK)
        text = Game.get_instance().lg_font.render("Press Esc to re-enter", True, '#FFFFFF')
        text_rect = text.get_rect(midbottom = Game.get_instance().screen.get_rect().center)
        Game.get_instance().screen.blit(text, text_rect)
        text = Game.get_instance().lg_font.render("Press Enter to confirm", True, '#FFFFFF')
        text_rect = text.get_rect(midbottom = text_rect.midtop)
        Game.get_instance().screen.blit(text, text_rect)
        game_over_state = Game.get_instance().state_machine.peek_state(GameOverState)
        Game.get_instance().screen.blit(game_over_state.initials_text, game_over_state.initials_text_rect)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                score = Game.get_instance().state_machine.peek_state(GameRunningState).score
                initials = Game.get_instance().state_machine.peek_state(GameOverState).initials
                add_highscore(initials, score)
                Game.get_instance().state_machine.change_state(StartScreen)
            elif event.key == pygame.K_ESCAPE:
                Game.get_instance().state_machine.change_state(GameOverState)

    
class GameOverState(GameState):
    def __init__(self):
        self.initials = ""
        self.initials_text = Game.get_instance().lg_font.render("AAA", True, '#FFFFFF')
        self.initials_text_rect = self.initials_text.get_rect(midtop = Game.get_instance().screen.get_rect().center)
        
    def enter(self):
        self.initials = ""
        text = Game.get_instance().lg_font.render("Enter Initials", True, '#FFFFFF')
        text_rect = text.get_rect(midbottom = Game.get_instance().screen.get_rect().center)
        Game.get_instance().screen.fill((0, 0, 0))
        Game.get_instance().gameboard.clear()
        Game.get_instance().screen.blit(text, text_rect)
        text = Game.get_instance().lg_font.render("Game Over", True, '#FFFFFF')
        text_rect = text.get_rect(midbottom = text_rect.midtop)
        Game.get_instance().screen.blit(text, text_rect)



    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.unicode and event.unicode.isalnum():
                print(event.unicode)
                self.initials += str.upper(event.unicode)
                self.initials_text = Game.get_instance().lg_font.render(self.initials, True, '#FFFFFF')
                Game.get_instance().screen.blit(self.initials_text, self.initials_text_rect)
                if len(self.initials) == 3:
                    print(self.initials)
                    Game.get_instance().state_machine.change_state(ConfirmInitials)

class StartScreen(GameState):
    def enter(self):
        text = Game.get_instance().lg_font.render("Press SPACE to start", True, '#FFFFFF')
        text_rect = text.get_rect(midbottom = Game.get_instance().screen.get_rect().center)
        Game.get_instance().screen.fill("#0000FF")
        Game.get_instance().screen.blit(text, text_rect)
        text = Game.get_instance().lg_font.render("Enter for High Scores", True, '#FFFFFF')
        text_rect = text.get_rect(midtop = Game.get_instance().screen.get_rect().center)
        Game.get_instance().screen.blit(text, text_rect)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Game.get_instance().state_machine.change_state(GameRunningState)
            elif event.key == pygame.K_RETURN:
                Game.get_instance().state_machine.change_state(HighScoreBoard)

class GameRunningState(GameState):
    def __init__(self):
        self.header = "Drop Da Blockz"
        # The following properties are not native to state machines, but are necessary for the game to function.
        self.frame_count: int = 0
        self.gravity_timer: float = time()
        self.input_timer: float = time()
        self.time_buffer: float = 0.3
        self.gravity_buffer: float = 0.5  # Time in seconds between automatic downward movements of the block.
        self.score: int = 0
        self.level: int = 0
        self.clearedRowCount: int = 0

    def enter(self) -> None:
        Game.get_instance().gameboard.clear()
        pygame.display.set_caption(self.header)
        self.gravity_buffer = 0.5
        self.score = 0
        self.level = 0
        self.clearedRowCount = 0
        Game.get_instance().screen.fill(DARK_GRAY)
        Game.get_instance().controller.set_block(Game.get_instance().block_queue.get_next())
    
    def render(self) -> None:
        Game.get_instance().gameboard.draw_blocks()
        Game.get_instance().controller.current_block.draw(Game.get_instance().gameboard)
        Game.get_instance().controller.current_block.draw_drop_preview(Game.get_instance().gameboard)
        Game.get_instance().gameboard.draw_grid()
        Game.get_instance().previewboard.draw_blocks()
        Game.get_instance().block_queue.draw(Game.get_instance().previewboard)
        Game.get_instance().previewboard.draw_grid()
        Game.get_instance().screen.blit(Game.get_instance().gameboard.surface, Game.get_instance().gameboard.rect)
        Game.get_instance().screen.blit(Game.get_instance().previewboard.surface, Game.get_instance().previewboard.rect)


    def update(self) -> None:
        # Handle fast-fall
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if time() - self.input_timer > self.time_buffer:
                Game.get_instance().controller.move_block_horizontal(-1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if time() - self.input_timer > self.time_buffer:
                Game.get_instance().controller.move_block_horizontal(1)

    # Move block down
        is_settled = False
        level_adjusted_buffer = max(.05, self.gravity_buffer - self.level/20) # speed up as level increases
        if time() - self.gravity_timer > level_adjusted_buffer:
            print(f"level: {self.level} buffer: {level_adjusted_buffer}")
            self.gravity_timer = time()
            # if self.frame_count % (1 if fast_fall else 10) == 0:
            if not Game.get_instance().controller.try_move_down():
                # Block has settled into place
                is_settled = True 
    

        if is_settled:                    
            print("Block settled")
            for i, row in enumerate(Game.get_instance().controller.current_block.rotated_shape()):
                    for j, cell in enumerate(row):
                        if cell:
                            x, y = Game.get_instance().controller.current_block.x + j, Game.get_instance().controller.current_block.y + i
                            Game.get_instance().gameboard.unified_grid[y][x] = Game.get_instance().controller.current_block.color
            full_rows = Game.get_instance().gameboard.find_full_rows()
            points = 5 if len(full_rows) == 4 else len(full_rows)
            self.score += points * 10 + points*self.level
            self.clearedRowCount += len(full_rows)
            if self.clearedRowCount >= 10:
                self.level += 1
                self.clearedRowCount = self.clearedRowCount % 10 #set full row count back in range
            Game.get_instance().gameboard.clear_rows(full_rows)
            Game.get_instance().controller.current_block = Game.get_instance().block_queue.get_next()
            for i, row in enumerate(Game.get_instance().controller.current_block.rotated_shape()):
                    for j, cell in enumerate(row):
                        if cell:
                            x, y = Game.get_instance().controller.current_block.x + j, Game.get_instance().controller.current_block.y + i
                            if Game.get_instance().gameboard.unified_grid[y][x] != 0:
                                print("Game Over")
                                Game.get_instance().state_machine.change_state(GameOverState)
                                return

    def handle_events(self, event: pygame.event.Event) -> None:
        # Function to manage keyboard events.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.get_instance().state_machine.enter_sub_state(PauseState)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                Game.get_instance().controller.move_block_horizontal(-1)
                self.input_timer = time()  

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                Game.get_instance().controller.move_block_horizontal(1)
                self.input_timer = time()    
                  
            if event.key == pygame.K_UP:
                Game.get_instance().controller.rotate_block()
                self.input_timer = time()
            
            if event.key == pygame.K_SPACE:
                Game.get_instance().controller.hard_drop()
                self.gravity_timer = self.gravity_buffer # end cycle immediately

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.gravity_buffer = 0.05

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.gravity_buffer = 0.5

class HighScoreBoard(GameState):
    def enter(self):
        Game.get_instance().screen.fill(BLACK)
        text = Game.get_instance().sm_font.render("Esc to exit", True, '#FFFFFF')
        text_rect = text.get_rect(topleft = Game.get_instance().screen.get_rect().topleft)
        Game.get_instance().screen.blit(text, text_rect)
        text = Game.get_instance().lg_font.render("High Scores", True, '#FFFFFF')
        text_rect = text.get_rect(midtop = Game.get_instance().screen.get_rect().midtop)
        Game.get_instance().screen.blit(text, text_rect)
        scores = load_highscores()
        text_rect.y += text_rect.h + 25
        text_rect.x -= 50
        for i, entry in enumerate(scores):
            msg = f"{i + 1}. {entry['name']} - {entry['score']}"
            text = Game.get_instance().mdlg_font.render(msg, True, '#FFFFFF')
            text_rect = text.get_rect(midleft = text_rect.midleft)
            Game.get_instance().screen.blit(text, text_rect)
            text_rect.y += text_rect.h

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.get_instance().state_machine.change_state(StartScreen)



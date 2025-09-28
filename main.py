from states import GameStateMachine
from game import Game
from gameboard import GameBoard


if __name__ == "__main__":
    state_machine = GameStateMachine() 
    gameboard = GameBoard()
    game = Game(state_machine, gameboard)
    state_machine.initialize()
    game.run()
 
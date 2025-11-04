from states import GameStateMachine
from game import Game
from gameboard import GameBoard
from blocks import BlockQueue, BlockController


if __name__ == "__main__":
    state_machine = GameStateMachine() 
    gameboard = GameBoard()
    controller = BlockController()
    block_queue = BlockQueue()
    previewboard = GameBoard((60,160), (500, 0), 10)
    game = Game(state_machine, gameboard, controller, block_queue, previewboard)
    state_machine.initialize()
    game.run()
  
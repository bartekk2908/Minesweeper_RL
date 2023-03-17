from minesweeper import Game
from board import Board

if __name__ == "__main__":
    board_size = (3, 3)
    board = Board(board_size)
    screen_size = (800, 800)
    game = Game(board, screen_size)
    game.run()

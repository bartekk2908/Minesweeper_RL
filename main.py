from game import Game
from board import Board

if __name__ == "__main__":
    board_size = (6, 6)
    prob = 0.1
    board = Board(board_size, prob)
    screen_size = (800, 800)
    game = Game(board, screen_size)
    game.run()

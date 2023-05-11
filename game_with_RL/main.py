from game import Game
from board import Board

if __name__ == "__main__":
    board_size = (30, 30)
    num_bombs = 150
    board = Board(board_size, num_bombs)
    screen_size = (700, 700)
    game = Game(board, screen_size)
    game.run()

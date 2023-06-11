from game import Game
from board import Board

if __name__ == "__main__":
    board_size = (9, 9)
    num_bombs = 10
    board = Board(board_size, num_bombs)
    screen_size = (700, 700)
    game = Game(board, screen_size)
    game.run_user()

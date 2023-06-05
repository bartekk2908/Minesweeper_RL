from piece import Piece
from random import sample
from itertools import product
from numpy import empty


class Board:
    def __init__(self, size, num_bombs):
        self.size = size
        self.num_bombs = num_bombs
        self.won = False
        self.lost = False
        self.num_clicked = 0
        self.set_board()

    def set_board(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                piece = Piece(False)
                row.append(piece)
            self.board.append(row)
        indexes_for_bombs = sample(list(product(range(self.size[0]), range(self.size[1]))), self.num_bombs + 1)
        for row, col in indexes_for_bombs[:-1]:
            self.board[row][col].has_bomb = True
        self.piece_for_replacement = self.get_piece(indexes_for_bombs[-1])

    def set_neighbours(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.get_piece((row, col))
                neighbours = self.get_list_of_neighbours((row, col))
                piece.set_neighbours(neighbours)

    def get_list_of_neighbours(self, index):
        neighbours = []
        for row in range(index[0] - 1, index[0] + 2):
            for col in range(index[1] - 1, index[1] + 2):
                out_of_bounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if same or out_of_bounds:
                    continue
                neighbours.append(self.get_piece((row, col)))
        return neighbours

    def get_size(self):
        return self.size

    def get_piece(self, index):
        return self.board[index[0]][index[1]]

    def handle_click(self, piece, piece_click, flag_click):
        if self.lost:
            return
        if piece.get_clicked() or (not flag_click and piece.get_flagged()):
            return
        if flag_click:
            piece.toggle_flagged()
        if piece_click:
            if not self.num_clicked:
                if piece.get_has_bomb():
                    piece.has_bomb = False
                    self.piece_for_replacement.has_bomb = True
                self.set_neighbours()
            piece.click()
            if piece.get_has_bomb():
                self.lost = True
                return
            self.num_clicked += 1
            if piece.get_num_around() != 0:
                return
            for neighbour in piece.get_neighbours():
                if not neighbour.get_has_bomb() and not neighbour.get_clicked():
                    self.handle_click(neighbour, True, False)

    def get_lost(self):
        return self.lost

    def get_won(self):
        return self.num_bombs == self.size[0] * self.size[1] - self.num_clicked

    def reset_board(self):
        self.won = False
        self.lost = False
        self.num_clicked = 0
        self.set_board()

    def represent_state(self):
        state = empty((self.size[0], self.size[1]), dtype=int)
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.get_piece((row, col))
                if not piece.get_clicked():
                    state[row][col] = -1
                else:
                    if piece.get_has_bomb():
                        state[row][col] = -2
                    else:
                        state[row][col] = piece.get_num_around()
        return state

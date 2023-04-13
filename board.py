from piece import Piece
from random import random


class Board:
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.won = False
        self.lost = False
        self.num_clicked = 0
        self.num_non_bombs = 0
        self.set_board()

    def set_board(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                has_bomb = random() < self.prob
                if not has_bomb:
                    self.num_non_bombs += 1
                piece = Piece(has_bomb)
                row.append(piece)
            self.board.append(row)
        self.set_neighbours()

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

    def handle_click(self, piece, piece_click, flag):
        if self.lost:
            return
        if piece.get_clicked() or (not flag and piece.get_flagged()):
            return
        if flag:
            piece.toggle_flagged()
        if piece_click:
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
        return self.num_non_bombs == self.num_clicked


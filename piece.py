
class Piece:
    def __init__(self, has_bomb):
        self.has_bomb = has_bomb
        self.clicked = False
        self.flagged = False

    def get_has_bomb(self):
        return self.has_bomb

    def get_clicked(self):
        return self.clicked

    def get_flagged(self):
        return self.flagged

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours
        self.set_num_around()

    def set_num_around(self):
        self.num_around = 0
        for piece in self.neighbours:
            if piece.get_has_bomb():
                self.num_around += 1

    def get_num_around(self):
        return self.num_around

    def click(self):
        self.clicked = True

    def toggle_flagged(self):
        self.flagged = not self.flagged



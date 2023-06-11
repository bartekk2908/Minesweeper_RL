import pygame as pg
from os import listdir
from time import sleep


IMAGES_DIR = "images"


class Game:
    def __init__(self, board, screen_size):
        self.board = board
        self.screen_size = screen_size
        self.piece_size = self.screen_size[0] // self.board.get_size()[1], self.screen_size[1] // self.board.get_size()[0]
        self.last_clicked = None
        self.load_images()

    def run_user(self):
        self.init_visualization()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    position = pg.mouse.get_pos()
                    left_click, middle_click, right_click = pg.mouse.get_pressed(3)
                    self.handle_click(self.get_index_of_position(position), left_click, right_click)
            self.draw()
            pg.display.flip()
            if self.board.get_won() or self.board.get_lost():
                # sound
                sleep(1)
                # running = False
                self.board.reset()
        pg.quit()

    def draw(self):
        top_left = (0, 0)
        for row in range(self.board.get_size()[0]):
            for col in range(self.board.get_size()[1]):
                piece = self.board.get_piece((row, col))
                image = self.get_image(piece)
                self.screen.blit(image, top_left)
                top_left = top_left[0] + self.piece_size[0], top_left[1]
            top_left = 0, top_left[1] + self.piece_size[1]
        if self.last_clicked:
            self.screen.blit(self.images["frame"], (self.last_clicked[1] * self.piece_size[0], self.last_clicked[0] * self.piece_size[1]))

    def load_images(self):
        self.images = {}
        for file_name in listdir(IMAGES_DIR):
            if not file_name.endswith(".png"):
                continue
            image = pg.image.load(f"{IMAGES_DIR}/" + file_name)
            image = pg.transform.scale(image, self.piece_size)
            self.images[file_name.split(".")[0]] = image

    def get_image(self, piece):
        if piece.get_clicked():
            string = "bomb-at-clicked-block" if piece.get_has_bomb() else str(piece.get_num_around())
        else:
            if self.board.get_won():
                string = "flag"
            elif self.board.get_lost():
                if piece.get_has_bomb():
                    string = "flag" if piece.get_flagged() else "unclicked-bomb"
                else:
                    string = "wrong-flag" if piece.get_flagged() else "empty-block"
            else:
                string = "flag" if piece.get_flagged() else "empty-block"
        return self.images[string]

    def get_index_of_position(self, position):
        return position[1] // self.piece_size[1], position[0] // self.piece_size[0]

    def handle_click(self, index, left_click, right_click):
        piece = self.board.get_piece(index)
        self.board.handle_click(piece, left_click, right_click)
        self.last_clicked = index

    def init_visualization(self):
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)

    def agent_playing_visualization(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
        self.draw()
        pg.display.flip()

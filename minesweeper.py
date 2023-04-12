import pygame as pg
import os


class Game:
    def __init__(self, board, screen_size):
        self.board = board
        self.screen_size = screen_size
        self.piece_size = self.screen_size[0] // self.board.get_size()[1], self.screen_size[1] // self.board.get_size()[0]
        self.load_images()

    def run(self):
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    position = pg.mouse.get_pos()
                    left_click, middle_click, right_click = pg.mouse.get_pressed(3)
                    print(pg.mouse.get_pressed(3))
                    print(position)
                    self.handle_click(position, left_click, right_click)
                self.draw()
            pg.display.flip()
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

    def load_images(self):
        self.images = {}
        for file_name in os.listdir("images"):
            if not file_name.endswith(".png"):
                continue
            image = pg.image.load("images/" + file_name)
            image = pg.transform.scale(image, self.piece_size)
            self.images[file_name.split(".")[0]] = image

    def get_image(self, piece):
        string = None
        if piece.get_clicked():
            pass
        else:
            string = "empty-block"
        return self.images[string]

    def handle_click(self, position, left_click, right_click):
        index = position[1] // self.piece_size[0], position[0] // self.piece_size[1]
        print(index)
        piece = self.board.get_piece(index)
        self.board.handle_click(piece, left_click, right_click)


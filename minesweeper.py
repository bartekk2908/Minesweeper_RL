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
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            pg.display.flip()
        pg.quit()

    def draw(self):
        top_left = (0, 0)
        for row in range(self.board.get_size()[0]):
            for col in range(self.board.get_size()[1]):
                image = self.images["empty-block"]
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


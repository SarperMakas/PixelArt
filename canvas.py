"""Canvas of the game"""
import numpy as np
import pygame


class Canvas:
    """canvas class of the game """
    def __init__(self, W, H, screen):
        # defining width, height, screen
        self.WIDTH = W
        self.HEIGHT = H
        self.screen = screen
        # sq size
        self.sqSize = 12
        # positions
        self.x = [141, self.WIDTH]
        self.y = [0, self.HEIGHT]
        # columns and rows
        # rows => y, columns => x
        self.col = (self.WIDTH-self.x[0]) // self.sqSize + 1
        self.row = self.HEIGHT // self.sqSize
        # color of the lines
        self.color = (125, 125, 125)
        # array of the canvas
        self.array = np.full((self.row, self.col, 3), [255, 255, 255], dtype=np.uint8)

    def reArray(self, size, row, col):
        """re define array"""
        self.col = col + 1
        self.row = row + 1
        self.sqSize = size
        self.array = np.full((self.row, self.col, 3), [255, 255, 255], dtype=np.uint8)

    def pixel(self, color):
        """add to pixel"""
        x, y = pygame.mouse.get_pos()
        if self.x[0] <= x <= self.x[1] and self.y[0] <= y <= self.y[1]:
            x -= 141
            col = x // self.sqSize
            row = y // self.sqSize
            self.array[row][col] = color

    
    def draw(self):
        """draw"""
        # draw pixels
        for row in range(self.row):
            for col in range(self.col):
                rect = pygame.Rect((col * self.sqSize + self.x[0], row * self.sqSize), (self.sqSize, self.sqSize))
                pygame.draw.rect(self.screen, self.array[row][col], rect)

        # draw lines
        for row in range(1, self.row + 2):
            for col in range(1, self.col + 2):
                # | line
                pygame.draw.line(self.screen, self.color, (col * self.sqSize+self.x[0], self.y[0]), (col * self.sqSize+self.x[0], self.y[1]))
                # - line
                pygame.draw.line(self.screen, self.color, (self.x[0], row*self.sqSize), (self.x[1], row*self.sqSize))


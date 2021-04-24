import pygame as pg

from data.config import SCR_H, SCR_W


class TextBox:
    def __init__(self, text, font, size, is_bold, color, pos, centralised=True):
        self.color = color
        self.x, self.y = pos
        self.centralised = centralised
        self.text = text

        pg.font.init()
        if font is None:
            self.font = pg.font.SysFont('Calibri', size, is_bold)
        elif font not in ['Arial', 'Calibri']:
            self.font = pg.font.Font(font, size)
        else:
            self.font = pg.font.SysFont(font, size, is_bold)

        self.letter_h = self.font.size('A')[1]
        self.box = self.make_box(text)
        self.w, self.h = self.get_box_size()

    def make_box(self, text):
        box = list()
        for string in text:
            box.append(self.font.render(string, True, self.color, None))
        return box

    def get_box_size(self):
        width = 0
        for i in range(len(self.box)):
            width = max(self.box[i].get_size()[0], width)
        height = len(self.box) * self.letter_h
        return width, height

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def is_on_screen(self):
        return -self.w <= self.x <= SCR_W and -self.h <= self.y <= SCR_H

    def draw(self, surface, dx=0, dy=0):
        if self.is_on_screen():
            y = self.y
            for string in self.box:
                x = self.x - string.get_width()/2 if self.centralised else self.x
                surface.blit(string, (int(x) - int(dx), int(y)-int(dy)))
                y += self.letter_h
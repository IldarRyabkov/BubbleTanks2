import pygame as pg
from data.config import SCR_H, SCR_W


class Text:
    """Widget that stores text on multiple lines. """
    def __init__(self,
                 x: float,
                 y: float,
                 font: str,
                 size: int,
                 color: tuple,
                 centralised=False):
        pg.font.init()
        self.font = pg.font.Font(font, size)
        self.x = x
        self.y = y
        self.color = color
        self.centralised = centralised
        self.surfaces = []   # list of text surfaces with their coords
        self.w = 0
        self.h = 0
        self.letter_h = self.font.size('A')[1]

    @property
    def is_on_screen(self) -> bool:
        return -self.w <= self.x <= SCR_W and -self.h <= self.y <= SCR_H

    def replace_with(self, text_widget):
        self.surfaces = text_widget.surfaces

    def clear(self):
        self.surfaces = []

    def set_text(self, text=()):
        """Receives a list of strings as input and makes a list,
        consisting of text surfaces with their coords.
        Then remembers the width and height of resulting text object.
        """
        self.surfaces = []
        for i, string in enumerate(text):
            surface = self.font.render(string, True, self.color)
            x = -surface.get_width() / 2 if self.centralised else 0
            y = i * self.letter_h
            self.surfaces.append([surface, x, y])

        self.w = max(line.get_size()[0] for line, _, _ in self.surfaces) if text else 0
        self.h = self.letter_h * len(text)

    def set_alpha(self, alpha):
        """Sets alpha-value for all text surfaces. """
        for surface, _, _ in self.surfaces:
            surface.set_alpha(alpha)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, dx=0, dy=0):
        if self.is_on_screen:
            for surface, x, y in self.surfaces:
                screen.blit(surface, (round(self.x + x - dx), round(self.y + y - dy)))


__all__ = ["Text"]

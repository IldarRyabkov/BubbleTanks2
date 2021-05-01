import pygame as pg
from math import sqrt, hypot

from data.colors import WHITE, LIGHT_GREY


class ExitButton:
    def __init__(self):
        self.x = 112
        self.y = 864
        self.r = 37
        self.d = int(self.r / sqrt(2))
        self.colors = ((33, 51, 62), LIGHT_GREY)
        self.color = self.colors[0]

    @property
    def cursor_on_button(self):
        x, y = pg.mouse.get_pos()
        return hypot(x - self.x, y - self.y) <= self.r

    def update(self):
        self.color = self.colors[1] if self.cursor_on_button else self.colors[0]

    def draw(self, surface):
        pg.draw.circle(surface, WHITE, (self.x, self.y), self.r)
        pg.draw.circle(surface, self.color, (self.x, self.y), self.r-4)
        pg.draw.line(surface, WHITE, (self.x - self.d + 2, self.y + self.d - 2),
                                         (self.x + self.d - 2, self.y - self.d + 2), 6)
        pg.draw.line(surface, WHITE, (self.x - self.d + 2, self.y - self.d + 1),
                                         (self.x + self.d - 2, self.y + self.d - 2), 6)
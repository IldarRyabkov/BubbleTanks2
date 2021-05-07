import pygame as pg
from math import hypot

from utils import H
from data.paths import EXIT_BUTTON, EXIT_BUTTON_PRESSED


class ExitButton:
    """Button to exit the pause menu and return to the game."""
    def __init__(self, xo):
        self.x = xo + H(7)
        self.y = H(827)
        self.r = H(37)
        size = (2 * self.r, 2 * self.r)
        self.bg = {False: pg.transform.scale(pg.image.load(EXIT_BUTTON).convert_alpha(), size),
                   True: pg.transform.scale(pg.image.load(EXIT_BUTTON_PRESSED).convert_alpha(), size)}

    @property
    def cursor_on_button(self):
        x, y = pg.mouse.get_pos()
        return hypot(x - self.x - self.r, y - self.y - self.r) <= self.r

    def draw(self, screen):
        screen.blit(self.bg[self.cursor_on_button], (self.x, self.y))


__all__ = ["ExitButton"]

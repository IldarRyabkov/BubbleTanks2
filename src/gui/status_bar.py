import pygame as pg

from data.colors import WHITE, STATUS_BAR_BG
from utils import H


class StatusBar:
    """ The status bar is used in the cooldown window to show the cooldown
    of the player's weapon and superpower, and in the health window to show
    how many bubbles are left to collect to upgrade the tank.
    """
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 max_value: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.value = 0
        self.scaled_w = 0
        self.max_value = max_value
        self.boundary_rect = pg.Rect(0, 0, round(self.w), round(self.h))
        self.value_rect = pg.Rect(0, 0, round(self.scaled_w), round(self.h))

    def set_value(self, value: float, reset=False):
        """Sets new value to the status bar. """
        self.value = 0 if reset and value >= self.max_value else value
        self.scaled_w = self.w * self.value/self.max_value if self.max_value else 0

    def set_max_value(self, max_value: int):
        self.max_value = max_value

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        topleft = round(self.x), round(self.y)
        self.boundary_rect.topleft = topleft
        self.value_rect.topleft = topleft
        self.value_rect.w = round(self.scaled_w)
        pg.draw.rect(surface, WHITE, self.boundary_rect, H(1))
        pg.draw.rect(surface, STATUS_BAR_BG, self.value_rect)


__all__ = ["StatusBar"]

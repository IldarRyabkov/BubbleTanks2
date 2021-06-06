import pygame as pg

from gui.widgets.tank_body import TankBody
from utils import H
from constants import *


class TankBodySmooth(TankBody):
    """Widget of Pause menu that shows player's tank look. """
    def __init__(self, menu, x, y):
        super().__init__(x, y)
        self.menu = menu
        self.r = H(129)
        self.center = (self.r + H(20), self.r)
        self.surface = pg.Surface((2 * self.r + H(40), 2 * self.r), pg.SRCALPHA)
        self.surface_pos = (self.x - self.r - H(20), self.y - self.r)

    def clear_surface(self):
        self.surface.fill((0, 0, 0, 0))
        pg.draw.circle(self.surface, WHITE, self.center, self.r)
        pg.draw.circle(self.surface, TANK_BG_COLOR, self.center, H(123))

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if self.menu.is_opening or self.menu.is_closing:
            if self.menu.is_opening:
                alpha = round(255 * time_elapsed)
            else:
                alpha = round(255 - 255 * time_elapsed)
            self.body.update(*self.center, dt, target_x=9000, target_y=self.r)
            self.clear_surface()
            self.surface.set_alpha(alpha)
        else:
            super().update(dt, animation_state, time_elapsed)

    def draw(self, screen, dx=0, dy=0):
        if self.menu.is_closing or self.menu.is_opening:
            self.body.draw(self.surface)
            screen.blit(self.surface, self.surface_pos)
        else:
            super().draw(screen)


__all__ = ["TankBodySmooth"]

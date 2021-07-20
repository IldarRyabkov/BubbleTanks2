import pygame as pg

from .tank_preview import TankPreview
from components.utils import H
from data.constants import *


class TankPreviewSmooth(TankPreview):
    """Widget that shows player's tank look and changes
    transparency during opening/closing animation.
    """
    def __init__(self, screen_rect, x, y, no_background=False):
        super().__init__(screen_rect, x, y, no_background)
        self.r = H(129)
        self.center = (self.r + H(20), self.r)
        self.surface = pg.Surface((2 * self.r + H(40), 2 * self.r), pg.SRCALPHA)
        self.surface_pos = (self.x - self.r - H(20), self.y - self.r)

    def clear_surface(self):
        self.surface.fill((0, 0, 0, 0))
        if not self.no_background:
            pg.draw.circle(self.surface, WHITE, self.center, self.r)
            pg.draw.circle(self.surface, TANK_BG_COLOR, self.center, H(123))

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if animation_state in (OPEN, CLOSE):
            if animation_state == OPEN:
                alpha = round(255 * time_elapsed)
            else:
                alpha = round(255 - 255 * time_elapsed)
            x, y = self.center
            x += self.dx
            for circle in self.circles:
                circle.update(x, y, dt, 0)
            for gun in self.guns:
                gun.update(x, y, dt)

            self.clear_surface()
            self.surface.set_alpha(alpha)
        else:
            super().update(dt, animation_state, time_elapsed)

    def draw(self, screen, animation_state=WAIT):
        if animation_state == WAIT:
            super().draw(screen)
        else:
            super().draw(self.surface)
            screen.blit(self.surface, self.surface_pos)


__all__ = ["TankPreviewSmooth"]

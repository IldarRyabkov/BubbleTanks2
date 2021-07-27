import pygame as pg

from gui.widgets.animated_widget import AnimatedWidget
from data.constants import *


class Rectangle(AnimatedWidget):
    def __init__(self, x, y, w, h, rect_width, border_radius, color):
        super().__init__()
        self.surface = pg.Surface((w, h), pg.SRCALPHA)
        self.pos = x, y
        rect = pg.Rect(rect_width // 2, rect_width // 2, w - rect_width, h - rect_width)
        pg.draw.rect(self.surface, color, rect, width=rect_width, border_radius=border_radius)
        rect.x += x
        rect.y += y
        self.rect = rect
        self.color = color
        self.rect_width = rect_width
        self.border_radius = border_radius

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if animation_state == WAIT:
            if self.surface.get_alpha() != 255:
                self.surface.set_alpha(255)
        elif animation_state == OPEN:
            self.surface.set_alpha(round(255 * time_elapsed))
        elif animation_state == CLOSE:
            self.surface.set_alpha(round(255 * (1 - time_elapsed)))

    def draw(self, screen, animation_state=WAIT):
        if animation_state == WAIT:
            pg.draw.rect(screen, self.color, self.rect,
                         width=self.rect_width,
                         border_radius=self.border_radius)
        else:
            screen.blit(self.surface, self.pos)


__all__ = ["Rectangle"]

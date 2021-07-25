import pygame as pg

from gui.widgets.animated_widget import AnimatedWidget
from data.constants import *


class BackgroundImage(AnimatedWidget):
    def __init__(self, x, y, w, h, image):
        super().__init__()
        self.pos = x, y
        self.image = pg.transform.smoothscale(pg.image.load(image).convert_alpha(), (w, h))

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if animation_state == WAIT and self.image.get_alpha() !=255:
            self.image.set_alpha(255)
        elif animation_state == OPEN:
            self.image.set_alpha(round(255 * time_elapsed))
        elif animation_state == CLOSE:
            self.image.set_alpha(round(255 * (1 - time_elapsed)))

    def draw(self, screen, animation_state=WAIT):
        screen.blit(self.image, self.pos)


__all__ = ["BackgroundImage"]

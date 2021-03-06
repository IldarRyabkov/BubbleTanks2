import pygame as pg

from gui.widgets.text_widget import TextWidget
from components.utils import H
from data.constants import *
from assets.paths import FONT_1


class CreditsLabel(TextWidget):
    def __init__(self, height, image, image_height):
        super().__init__(SCR_W2, height, FONT_1, H(42), WHITE, 1)
        self.image = pg.image.load(image).convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (int(8/9*SCR_H), image_height))
        self.image_pos = (SCR_W2 - self.image.get_width()//2, self.y - H(15))

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        super().update(dt, animation_state, time_elapsed)
        if animation_state == OPEN:
            self.image.set_alpha(round(255 * time_elapsed))
        elif animation_state == CLOSE:
            self.image.set_alpha(round(255 - 255 * time_elapsed))
        else:
            self.image.set_alpha(255)

    def draw(self, screen, animation_state=WAIT, dx=0, dy=0):
        screen.blit(self.image, self.image_pos)
        super().draw(screen)


__all__ = ["CreditsLabel"]

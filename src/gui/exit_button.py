import pygame as pg

from data.paths import *
from gui.button import Button
from constants import *
from utils import *


class ExitButton(Button):
    """Button that is used to exit pause menu. """
    def __init__(self, xo, sound_player, action):
        super().__init__(pg.SYSTEM_CURSOR_HAND, sound_player, UI_CLICK, action)
        self.x = xo + H(15)
        self.y = H(840)
        self.radius = H(34)

        size = (2 * self.radius, 2 * self.radius)
        self.images = (
            pg.transform.scale(pg.image.load(EXIT_BUTTON).convert_alpha(), size),
            pg.transform.scale(pg.image.load(EXIT_BUTTON_PRESSED).convert_alpha(), size)
        )
        self.current_image = 0

    @property
    def cursor_on_button(self):
        return circle_collidepoint(self.x + self.radius,
                                   self.y + self.radius,
                                   self.radius, *pg.mouse.get_pos())

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        self.current_image = int(self.cursor_on_button)

    def draw(self, screen):
        screen.blit(self.images[self.current_image], (self.x, self.y))


__all__ = ["ExitButton"]

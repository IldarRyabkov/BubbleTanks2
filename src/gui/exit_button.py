import pygame as pg

from data.paths import *
from gui.button import Button
from constants import *
from utils import *


class ExitButton(Button):
    """Button that is used to exit pause menu. """
    def __init__(self, menu, xo, sound_player, action):
        super().__init__(pg.SYSTEM_CURSOR_HAND, sound_player, UI_CLICK, action)
        self.menu = menu
        self.x = xo + H(15)
        self.y = H(840)
        self.radius = H(34)

        size = (2 * self.radius, 2 * self.radius)
        self.images = (
            pg.transform.scale(pg.image.load(EXIT_BUTTON_BG).convert_alpha(), size),
            pg.transform.scale(pg.image.load(EXIT_BUTTON_PRESSED_BG).convert_alpha(), size)
        )
        self.current_image = 0

    @property
    def cursor_on_button(self):
        return circle_collidepoint(self.x + self.radius,
                                   self.y + self.radius,
                                   self.radius, *pg.mouse.get_pos())

    def set_alpha(self, alpha):
        self.images[0].set_alpha(alpha)
        self.images[1].set_alpha(alpha)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        if animation_state == WAIT:
            self.set_alpha(255)
        if animation_state == OPEN and self.menu.is_opening:
            self.set_alpha(round(255 * time_elapsed))
        elif animation_state == CLOSE and self.menu.is_closing:
            self.set_alpha(round(255 - 255 * time_elapsed))
        self.current_image = self.cursor_on_button

    def draw(self, screen):
        screen.blit(self.images[self.current_image], (self.x, self.y))


__all__ = ["ExitButton"]

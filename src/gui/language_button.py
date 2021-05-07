import pygame as pg
from math import hypot

from data.config import CLOSE, OPEN, MAIN_MENU_ANIMATION_TIME as TIME
from utils import HF


class LanguageButton:
    """A button which is used in Start menu to choose a language. """
    SIZE_MAX = HF(112)
    SIZE_MIN = HF(80)
    VEL = HF(0.704)  # velocity with which button shows and hides
    SCALING_VEL = HF(0.24)  # velocity with which button scales

    def __init__(self, x: float, image_file: str):
        self.x = x
        self.y = HF(1008)
        self.start_pos = (self.x, self.y)
        self.image = pg.image.load(image_file).convert_alpha()
        self.surface = None
        self.size = self.SIZE_MIN

    @property
    def cursor_on_button(self) -> bool:
        x, y = pg.mouse.get_pos()
        return hypot(x - self.x, y - self.y) <= self.size / 2

    def update_size(self, dt):
        """Updates the size of the button based on
        whether the cursor is over it or not.
        """
        if self.cursor_on_button:
            self.size = min(self.SIZE_MAX, self.size + self.SCALING_VEL * dt)
        else:
            self.size = max(self.SIZE_MIN, self.size - self.SCALING_VEL * dt)
        self.surface = pg.transform.scale(self.image, (round(self.size), round(self.size)))

    def update_pos(self, dt, animation_time, state):
        """Updates the size of the button based on
        whether start menu is showing, hiding or waiting.
        """
        if state == CLOSE and  3/6 * TIME <= animation_time <= 4/6 * TIME:
            self.y += self.VEL * dt
        elif state == OPEN and 5/6 * TIME <= animation_time <= TIME:
            self.y -= self.VEL * dt

    def update(self, dt, animation_time, state):
        self.update_size(dt)
        self.update_pos(dt, animation_time, state)

    def draw(self, screen):
        screen.blit(self.surface, (round(self.x - self.size / 2),
                                   round(self.y - self.size / 2)))


__all__ = ["LanguageButton"]

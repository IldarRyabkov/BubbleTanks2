import pygame as pg

from gui.buttons.scaling_button import ScalingButton
from components.utils import H
from data.constants import SCR_H
from assets.paths import *


class StartButton(ScalingButton):
    def __init__(self, x, y_top, sound_player, action):
        super().__init__(x, SCR_H + H(90), H(225), H(175), 0.77, 220, None, sound_player,
                         scaling_time=90, action=action, click_sound=ENEMY_DEATH)
        self.image = pg.image.load(START_BUTTON_IMAGE).convert_alpha()
        self.surface = pg.transform.smoothscale(self.image, (round(self.w), round(self.h)))
        self.y_top = y_top
        self.velocity = (self.y_top - self.y) / 200

    def set_language(self, language):
        pass

    def update_open(self, time_elapsed, dt):
        if time_elapsed > 0.8:
            dy = max(self.y_top - self.y, self.velocity * dt)
            self.move(0, dy)

    def set_surface(self):
        self.surface = pg.transform.smoothscale(self.image, (round(self.w), round(self.h)))


__all__ = ["StartButton"]

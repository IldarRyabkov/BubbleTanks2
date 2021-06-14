import pygame as pg

from .scaling_button import ScalingButton
from assets.paths import DELETE_BUTTON_BG
from components.utils import H


class DeleteButton(ScalingButton):
    def __init__(self, x, sound_player, save_button, delete_button_action):
        super().__init__(x, H(740), H(55), H(55), 0.85, 180, None, sound_player,
                         action=lambda: delete_button_action(self))

        self.save_button = save_button
        self.surface = pg.image.load(DELETE_BUTTON_BG).convert_alpha()
        self.surface = pg.transform.smoothscale(self.surface, (round(self.w), round(self.h)))

    def set_language(self, language):
        pass

    def set_surface(self):
        pass


__all__ = ["DeleteButton"]

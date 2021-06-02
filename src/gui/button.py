import pygame as pg
from constants import *


class Button:
    """"A parent class for all button. """
    def __init__(self,
                 cursor,
                 sound_player=None,
                 click_sound=None,
                 action=lambda: None):
        self.rect = pg.Rect(0, 0, 0, 0)
        self.action = action
        self.is_pressed = False
        self.cursor = cursor
        self.sound_player = sound_player
        self.click_sound = click_sound

    @property
    def cursor_on_button(self):
        return self.rect.collidepoint(pg.mouse.get_pos())

    @property
    def pressed(self):
        self.is_pressed = self.cursor_on_button
        return self.is_pressed

    @property
    def clicked(self):
        clicked = self.is_pressed and self.cursor_on_button
        if clicked and self.click_sound is not None:
            self.sound_player.play_sound(self.click_sound)
        self.is_pressed = False
        return clicked

    def update_look(self, dt, animation_state=WAIT, time_elapsed=0):
        pass

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        pass

    def reset(self):
        self.is_pressed = False

    def draw(self, screen):
        pass


__all__ = ["Button"]

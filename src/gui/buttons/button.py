import pygame as pg
from data.constants import *


class Button:
    """"A parent class for all button. """
    def __init__(self,
                 cursor,
                 sound_player=None,
                 click_sound=None,
                 action=lambda: None):
        self.x = 0
        self.y = 0
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

    def set_language(self, language):
        pass

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
        self.rect.center = self.x, self.y

    def move_to(self, x=None, y=None):
        x = x or self.x
        y = y or self.y
        self.x = x
        self.y = y
        self.rect.center = x, y

    def update_look(self, dt, animation_state=WAIT, time_elapsed=0.0):
        pass

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        pass

    def update_click_animation(self, dt):
        pass

    def reset(self, state):
        self.is_pressed = False

    def draw(self, screen, animation_state=WAIT):
        pass


__all__ = ["Button"]

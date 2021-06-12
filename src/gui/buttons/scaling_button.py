import pygame as pg

from assets.paths import *
from gui.buttons.button import Button
from data.constants import *


class ScalingButton(Button):
    """Parent class for all buttons that change their size
    and transparency, when a cursor is on them.
    """
    def __init__(self, x, y, w, h,
                 min_scale, min_alpha,
                 texts, sound_player, scaling_time=100,
                 cursor=pg.SYSTEM_CURSOR_HAND,
                 click_sound=BUTTON_CLICK,
                 action=lambda: None):

        super().__init__(cursor, sound_player, click_sound, action)

        # (x, y) is the center of the button
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.scaling_time = scaling_time
        self.scale = min_scale
        self.SCALE_MIN = min_scale
        self.SCALE_MAX = 1
        self.SCALE_DELTA = (self.SCALE_MAX - self.SCALE_MIN) / self.scaling_time

        self.alpha = min_alpha
        self.ALPHA_MIN = min_alpha
        self.ALPHA_MAX = 255
        self.ALPHA_DELTA = (self.ALPHA_MAX - self.ALPHA_MIN) / self.scaling_time

        self.surface = pg.Surface((self.w, self.h), pg.SRCALPHA)
        self.surface.set_alpha(min_alpha)
        self.scaled_surface = None
        self.set_scaled_surface()

        self.rect = pg.Rect(self.x - self.w // 2,
                            self.y - self.h // 2,
                            self.w, self.h)

        self.sound_lock = False
        self.texts = texts
        self.text_widget = None

    def set_scaled_surface(self):
        size = (round(self.w * self.scale), round(self.h * self.scale))
        self.scaled_surface = pg.transform.smoothscale(self.surface, size)

    def render_surface(self):
        self.surface.fill((0, 0, 0, 0))
        self.text_widget.draw(self.surface)
        self.set_alpha()
        self.set_scaled_surface()

    def set_language(self, language):
        self.text_widget.set_text(self.texts[language])
        self.render_surface()

    def set_alpha(self, default_alpha=None):
        self.surface.set_alpha(self.alpha if default_alpha is None else default_alpha)

    def reset(self, state):
        self.alpha = self.ALPHA_MIN
        self.scale = self.SCALE_MIN
        self.sound_lock = False
        self.is_pressed = False
        self.render_surface()

    def increase(self, dt):
        self.alpha = min(self.ALPHA_MAX, self.alpha + self.ALPHA_DELTA * dt)
        self.scale = min(self.SCALE_MAX, self.scale + self.SCALE_DELTA * dt)

    def decrease(self, dt):
        self.alpha = max(self.ALPHA_MIN, self.alpha - self.ALPHA_DELTA * dt)
        self.scale = max(self.SCALE_MIN, self.scale - self.SCALE_DELTA * dt)

    def update_click_animation(self, dt):
        self.update_size(dt, True, default_alpha=255)

    def update_size(self, dt, increasing, default_alpha=None):
        old_scale = self.scale

        if increasing and self.scale < self.SCALE_MAX:
            self.increase(dt)
        elif not increasing and self.scale > self.SCALE_MIN:
            self.decrease(dt)

        if self.scale != old_scale:
            self.set_alpha(default_alpha)
            self.set_scaled_surface()

    def update_wait(self, dt):
        increasing = False if self.is_pressed else self.cursor_on_button
        self.update_size(dt, increasing)

    def update_open(self, time_elapsed, dt):
        self.scaled_surface.set_alpha(self.ALPHA_MIN * time_elapsed)

    def update_close(self, time_elapsed, dt):
        self.scaled_surface.set_alpha(self.alpha - self.alpha * time_elapsed)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        if animation_state == WAIT:
            self.update_wait(dt)
        elif animation_state == OPEN:
            self.update_open(time_elapsed, dt)
        else:
            self.update_close(time_elapsed, dt)

    def draw(self, screen, animation_state=WAIT):
        screen.blit(self.scaled_surface, (self.x - self.scaled_surface.get_width() // 2,
                                          self.y - self.scaled_surface.get_height() // 2))


__all__ = ["ScalingButton"]

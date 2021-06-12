import pygame as pg

from gui.widgets.text_widget import TextWidget
from gui.buttons.scaling_button import ScalingButton
from data.constants import *
from assets.paths import *
from components.utils import H


class MainMenuButton(ScalingButton):
    """Parent class for all Main menu buttons. """
    def __init__(self,
                 x,
                 texts,
                 radius,
                 image,
                 sound_player,
                 aspect_ratio,
                 y_min,
                 action,
                 click_sound=BUTTON_CLICK):
        """Radius is half the height of the button. """

        super().__init__(x, SCR_H + radius, 2*radius*aspect_ratio, 2*radius, 0.7, 210,
                         texts, sound_player, 140, click_sound=click_sound, action=action)

        self.Y_MIN = y_min  # y-coord when button is shown
        self.Y_MAX = SCR_H + radius  # y-coord when button is hidden
        self.vel = (self.Y_MAX - self.Y_MIN) / 250

        self.text_widget = TextWidget(SCR_W2, H(820) - 2.2 * radius, FONT_1, round(0.6 * radius), WHITE, 1)

        self.text_alpha = 0
        self.TEXT_ALPHA_MIN = 0
        self.TEXT_ALPHA_MAX = 255
        self.TEXT_ALPHA_DELTA = (self.TEXT_ALPHA_MAX - self.TEXT_ALPHA_MIN) / self.scaling_time

        self.surface = pg.image.load(image).convert_alpha()
        self.surface = pg.transform.scale(self.surface, (round(self.w), round(self.h)))

    @property
    def cursor_on_button(self) -> bool:
        x, y = pg.mouse.get_pos()
        a, b = self.scaled_surface.get_width()//2, self.scaled_surface.get_height()//2
        return (self.x - x) * (self.x - x) / (a * a) + (self.y - y) * (self.y - y) / (b * b) <= 1

    def set_alpha(self, default_alpha=None):
        super().set_alpha(default_alpha)
        self.text_widget.set_alpha(self.text_alpha if default_alpha is None else default_alpha)

    def render_surface(self):
        self.set_alpha()
        self.set_scaled_surface()

    def reset(self, state):
        self.y = self.Y_MAX
        self.text_alpha = self.TEXT_ALPHA_MIN
        super().reset(state)

    def increase(self, dt):
        super().increase(dt)
        self.text_alpha = min(self.TEXT_ALPHA_MAX, self.text_alpha + self.TEXT_ALPHA_DELTA * dt)

    def decrease(self, dt):
        super().decrease(dt)
        self.text_alpha = max(self.TEXT_ALPHA_MIN, self.text_alpha - self.TEXT_ALPHA_DELTA * dt)

    def update_close(self, time_elapsed, dt):
        if time_elapsed >= 0.3:
            self.update_size(dt, False)
        if time_elapsed >= 0.5:
            self.y = min(self.Y_MAX, self.y + self.vel * dt)

    def update_open(self, time_elapsed, dt):
        if time_elapsed >= 0.5:
            self.y = max(self.Y_MIN, self.y - self.vel * dt)

    def draw(self, screen, animation_state=WAIT):
        super().draw(screen)
        self.text_widget.draw(screen)


__all__ = ["MainMenuButton"]

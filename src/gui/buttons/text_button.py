from gui.widgets.text_widget import TextWidget
from gui.buttons.scaling_button import ScalingButton
from data.constants import *
from components.utils import H
from assets.paths import BUTTON_CLICK


class TextButton(ScalingButton):
    def __init__(self, x, y, texts, font, font_size, min_alpha,
                 sound_player, action=lambda: None, w=H(700), click_sound=BUTTON_CLICK):

        super().__init__(x, y, w, font_size, 0.88, min_alpha, texts, sound_player,
                         action=action,
                         click_sound=click_sound)

        self.text_widget = TextWidget(self.w // 2, 0, font, font_size, WHITE, 1)
        self.rect.h = H(60)
        self.rect.centery = self.y

    def set_text(self, text):
        self.text_widget.set_text(text)
        self.render_surface()

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


class DoubleTextButton(ScalingButton):
    def __init__(self, x, y, texts, value, font, font_size, sound_player, action):
        super().__init__(x, y, H(700), font_size, 0.88, 220, texts, sound_player, action=action)

        self.text_widget = TextWidget(self.w // 2 - H(40), 0, font, font_size, WHITE, 2)
        self.value_widget = TextWidget(self.w // 2 + H(40), 0, font, font_size, WHITE, 0)
        self.set_value(value)

    def set_value(self, value):
        self.value_widget.set_text(value)
        self.render_surface()

    def render_surface(self):
        self.surface.fill((0, 0, 0, 0))
        self.text_widget.draw(self.surface)
        self.value_widget.draw(self.surface)
        self.set_alpha()
        self.set_scaled_surface()


__all__ = ["TextButton", "DoubleTextButton"]

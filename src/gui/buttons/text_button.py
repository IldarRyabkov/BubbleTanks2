import pygame as pg

from gui.widgets.text_widget import TextWidget
from gui.buttons.scaling_button import ScalingButton
from data.constants import *
from components.utils import H
from assets.paths import BUTTON_CLICK


class TextButton(ScalingButton):
    def __init__(self, x, y, texts, font, font_size, min_alpha,
                 sound_player, action=lambda: None, w=H(700),
                 click_sound=BUTTON_CLICK, cursor=pg.SYSTEM_CURSOR_HAND):

        super().__init__(x, y, w, font_size, 0.88, min_alpha, texts, sound_player,
                         action=action,
                         click_sound=click_sound,
                         cursor=cursor)

        self.text_widget = TextWidget(self.w // 2, 0, font, font_size, WHITE, 1)
        self.rect.h = font_size
        self.rect.centery = self.y

    def set_text(self, text):
        self.text_widget.set_text(text)
        self.render_surface()


class TextButton2(ScalingButton):
    def __init__(self, x, y, w, texts, font, font_size, sound_player, action, min_alpha):
        super().__init__(x, y, w, font_size,
                         0.88, min_alpha, texts,
                         sound_player, action=action,
                         cursor=pg.SYSTEM_CURSOR_ARROW,
                         click_sound=None)

        self.rect = pg.Rect(x - w//2, 0, w, font_size)
        self.rect.centery = y
        self.text_widget = TextWidget(w, 0, font, font_size, WHITE, 2)


class DoubleTextButton(ScalingButton):
    def __init__(self, game, x, y, texts, value,
                 font, font_size, sound_player,
                 action, min_alpha=200, w=H(700)):
        super().__init__(x, y, w, font_size, 0.88, min_alpha, texts, sound_player, action=action)

        self.text_widget = TextWidget(self.w // 2 - H(40), 0, font, font_size, WHITE, 2)
        self.value_widget = TextWidget(self.w // 2 + H(40), 0, font, font_size, WHITE, 0)

        self.game = game
        self.value = None
        self.set_value(value)

    def set_language(self, language):
        self.text_widget.set_text(self.texts[language])
        self.set_value(self.value)

    def set_value(self, value):
        self.value = value
        if type(value) == list:
            self.value_widget.set_text(value[self.game.language])
        else:
            self.value_widget.set_text(value)
        self.render_surface()

    def set_surface(self):
        self.surface.fill((0, 0, 0, 0))
        self.text_widget.draw(self.surface)
        self.value_widget.draw(self.surface)


__all__ = ["TextButton", "TextButton2", "DoubleTextButton"]

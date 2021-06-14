import pygame as pg

from gui.widgets.text_widget import TextWidget
from gui.buttons.scaling_button import ScalingButton
from data.constants import *
from components.utils import H


class SliderButton(ScalingButton):
    def __init__(self, x, y, label_texts, font, font_size, sound_player, volume_type, min_alpha=220):

        super().__init__(x, y, H(940), H(50), 0.92, min_alpha,
                         label_texts, sound_player,
                         cursor=pg.SYSTEM_CURSOR_SIZEWE,
                         scaling_time=100)
        self.value = 1
        self.volume_type = volume_type

        self.line_w = H(340)
        self.line_h = H(7)
        self.slider_h = H(56)

        self.empty_line = pg.Rect(self.w//2 + H(40),
                                  (self.h - self.line_h)//2,
                                  self.line_w, self.line_h)

        self.filled_line = self.empty_line.copy()

        self.slider = pg.Rect(self.empty_line.right - H(6),
                              (self.h - H(46)) // 2,
                              H(12), H(46))

        self.slider_rect = pg.Rect(self.x + H(40),
                                   self.y - self.h // 2,
                                   self.line_w, self.h)

        self.text_widget = TextWidget(self.w // 2 - H(40), 0, font, font_size, WHITE, 2)


    @property
    def cursor_on_button(self):
        return self.slider_rect.collidepoint(pg.mouse.get_pos())

    def set_surface(self):
        self.surface.fill((0, 0, 0, 0))
        self.text_widget.draw(self.surface)
        pg.draw.rect(self.surface, GREY_2, self.empty_line, border_radius=H(3))
        pg.draw.rect(self.surface, WHITE, self.filled_line, border_radius=H(3))
        pg.draw.rect(self.surface, WHITE, self.slider, border_radius=H(6))

    def set_value(self, value):
        self.value = value
        self.slider.centerx = self.w // 2 + H(40) + value * self.line_w
        self.filled_line.w = value * self.line_w

    def reset(self, state):
        if self.volume_type == "music":
            self.set_value(self.sound_player.music_volume)
        elif self.volume_type == "sound":
            self.set_value(self.sound_player.sound_volume)
        super().reset(state)

    def set_volume(self):
        if self.volume_type == "music":
            self.sound_player.set_music_volume(self.value)
        elif self.volume_type == "sound":
            self.sound_player.set_sound_volume(self.value)

    def update_wait(self, dt):
        if self.is_pressed:
            self.update_size(dt, True)
        else:
            increasing = self.rect.collidepoint(pg.mouse.get_pos())
            self.update_size(dt, increasing)

        if self.is_pressed:
            x = pg.mouse.get_pos()[0]
            new_value = (x - self.x - H(40)) / self.line_w
            if new_value < 0:
                new_value = 0
            elif new_value > 1:
                new_value = 1
            if self.value != new_value:
                self.set_value(new_value)
                self.render_surface()
            self.set_volume()


__all__ = ["SliderButton"]

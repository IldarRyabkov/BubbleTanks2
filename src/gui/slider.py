import pygame as pg

from gui.text import Text
from gui.scaling_button import ScalingButton
from constants import *
from utils import H


class Slider(ScalingButton):
    def __init__(self, x, y, label_texts, font, font_size, sound_player):
        super().__init__(x, y, H(960), H(80), 0.92, 200, label_texts, sound_player)
        self.value = 1

        self.line_w = H(370)
        self.line_h = H(7)
        self.slider_h = H(56)

        self.empty_line = pg.Rect(self.w//2 + H(40), (self.h - self.line_h)//2, self.line_w, self.line_h)
        self.filled_line = self.empty_line.copy()
        self.slider_rect = pg.Rect(self.empty_line.right - H(6) , (self.h - H(46))//2, H(12), H(46))

        self.click_area = pg.Rect(self.x + H(40), self.y - self.h//2, self.line_w, self.h)

        self.zoom_area.w -= H(100)
        self.zoom_area.x += H(50)

        self.text_widget = Text(self.w//2 - H(40), 0, font, font_size, WHITE, 2)

        self.pressed = False

    @property
    def cursor_on_slider(self):
        return self.click_area.collidepoint(pg.mouse.get_pos())

    @property
    def cursor_on_button(self) -> bool:
        return super().cursor_on_button or self.pressed

    def render_surface(self):
        self.surface.fill((0, 0, 0, 0))
        self.text_widget.draw(self.surface)
        pg.draw.rect(self.surface, GREY_2, self.empty_line, border_radius=3)
        pg.draw.rect(self.surface, WHITE, self.filled_line, border_radius=3)
        pg.draw.rect(self.surface, WHITE, self.slider_rect, border_radius=6)
        self.set_alpha()
        self.set_scaled_surface()

    def handle(self, e_type):
        if e_type == pg.MOUSEBUTTONUP:
            self.pressed = False
        elif self.cursor_on_slider:
            self.pressed = True

    def reset(self, value=None):
        value = self.value if value is None else value
        self.set_value(value)
        self.pressed = False
        super().reset()

    def set_value(self, value):
        self.value = value
        self.slider_rect.centerx = self.w//2 + H(40) + value * self.line_w
        self.filled_line.w = value * self.line_w

    def update_wait(self, dt):
        super().update_wait(dt)
        if self.pressed:
            x = pg.mouse.get_pos()[0]
            new_value = (x - self.x - H(40)) / self.line_w
            if new_value < 0:
                new_value = 0
            elif new_value > 1:
                new_value = 1
            if self.value != new_value:
                self.set_value(new_value)
                self.render_surface()


__all__ = ["Slider"]

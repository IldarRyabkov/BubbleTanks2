import pygame as pg

from .text_widget import TextWidget
from components.utils import H


class KeyHint(TextWidget):
    def __init__(self, x, y, font, font_size, color):
        super().__init__(x, y, font, font_size, color)

    def set_text(self, text=''):
        super().set_text(text)
        key = self.text.split()[0]
        key_w, key_h = self.font.render(key, True, self.color).get_size()
        key_rect = pg.Rect(0, 0, round(key_w * 1.3), round(key_h * 1.3))
        key_rect.center = key_w//2 + H(15), key_h//2 + H(10)
        text_surface = self.lines[0][0]
        text_surface.set_alpha(230)
        surf_w, surf_h = text_surface.get_size()
        new_surface = pg.Surface((surf_w + H(15), surf_h + H(20)), pg.SRCALPHA)
        new_surface.blit(text_surface, (H(15), H(10)))
        pg.draw.rect(new_surface, (255, 255, 255, 230), key_rect, width=H(3), border_radius=H(10))
        self.lines[0][0] = new_surface



__all__ = ["KeyHint"]

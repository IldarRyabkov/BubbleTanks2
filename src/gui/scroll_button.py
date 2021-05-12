import pygame as pg

from gui.text import Text
from gui.scaling_button import ScalingButton
from data.paths import *
from data.colors import *
from utils import H


class ScrollButton(ScalingButton):
    """Button used to scroll through texts. """
    def __init__(self, x, y, scroll_texts, label_texts, sound_player):
        super().__init__(x, y, H(800), H(56), 0.92, 200, label_texts, sound_player)
        self.scroll_texts = scroll_texts
        self.cur_text = len(scroll_texts) - 1

        self.scroll_text_widget = Text(self.w*0.75 + H(10), H(8), FONT_1, H(44), WHITE, 1)
        self.scroll_text_widget.set_text(scroll_texts[-1])

        self.text_widget = Text(self.w//2 - H(40), H(8), FONT_1, H(44), WHITE, 2)

        self.arrows_image = pg.image.load(SCROLL_BUTTON).convert_alpha()
        self.arrows_image = pg.transform.scale(self.arrows_image, (self.w//2 - H(60), self.h))

        self.left_arrow_rect = pg.Rect(self.x + H(20),
                                       self.y - self.h//2 - H(20),
                                       H(60), self.h + H(40))

        self.right_arrow_rect = pg.Rect(self.x + self.w//2 - H(60),
                                        self.y - self.h//2 - H(20),
                                        H(60), self.h + H(40))

    @property
    def value(self):
        return self.scroll_texts[self.cur_text][0]

    @property
    def clicked(self):
        pos = pg.mouse.get_pos()
        left_arrow_clicked = self.left_arrow_rect.collidepoint(pos)
        right_arrow_clicked = self.right_arrow_rect.collidepoint(pos)
        if left_arrow_clicked or right_arrow_clicked:
            shift = -1 if left_arrow_clicked else 1
            self.cur_text = (self.cur_text + shift) % len(self.scroll_texts)
            self.scroll_text_widget.set_text([self.value])
            self.render_surface()
            super().handle_click()
            return True
        return False

    def render_surface(self):
        self.surface.fill((0, 0, 0, 0))
        self.text_widget.draw(self.surface)
        self.scroll_text_widget.draw(self.surface)
        self.surface.blit(self.arrows_image, (self.w//2 + H(40), 0))
        self.set_scaled_surface()


__all__ = ["ScrollButton"]

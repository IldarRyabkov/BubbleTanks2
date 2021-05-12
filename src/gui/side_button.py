import pygame as pg

from data.colors import WHITE
from data.paths import FONT_2, SIDE_BUTTON, SIDE_BUTTON_PRESSED
from utils import H


class SideButton:
    """A button that is used in the pause menu
    to switch to a specific window.
    """
    def __init__(self, x, y, texts, pressed):
        self.x = x
        self.y = y

        self.w = H(96)
        self.h = H(160)

        self.pressed = pressed

        self.texts = texts
        self.text_surface = None
        self.text_pos = None

        size = (self.w, self.h)
        self.bg = {
            False: pg.transform.scale(pg.image.load(SIDE_BUTTON).convert_alpha(), size),
            True: pg.transform.scale(pg.image.load(SIDE_BUTTON_PRESSED).convert_alpha(), size)
        }

    @property
    def clicked(self):
        x, y = pg.mouse.get_pos()
        return 0 <= x - self.x <= self.w and 0 <= y - self.y <= self.h

    def set_language(self, language):
        pg.font.init()
        text = self.texts[language][0]
        font = pg.font.Font(FONT_2, H(35) if len(text) < 10 else H(29))
        self.text_surface = pg.transform.rotate(font.render(text, True, WHITE), 90)
        self.text_pos = (self.x + (self.w - self.text_surface.get_width()) // 2,
                         self.y + (self.h - self.text_surface.get_height()) // 2)

    def draw(self, screen):
        screen.blit(self.bg[self.pressed], (self.x, self.y))
        screen.blit(self.text_surface, self.text_pos)


__all__ = ["SideButton"]

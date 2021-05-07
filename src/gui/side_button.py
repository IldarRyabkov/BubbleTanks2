import pygame as pg

from data.gui_texts import SIDE_BUTTON_TEXTS as TEXTS
from data.colors import WHITE
from data.paths import FONT_2, SIDE_BUTTON, SIDE_BUTTON_PRESSED
from utils import H


class SideButton:
    """A button that is used in the pause menu
    to switch to a specific window.
    """
    def __init__(self,
                 x: int,
                 y: int,
                 name: str,
                 clicked: bool):
        self.x = x
        self.y = y
        self.w = H(96)
        self.h = H(160)
        self.clicked = clicked
        self.name = name
        self.text = None
        self.text_pos = None
        size = (self.w, self.h)
        self.bg = {
            False: pg.transform.scale(pg.image.load(SIDE_BUTTON).convert_alpha(), size),
            True: pg.transform.scale(pg.image.load(SIDE_BUTTON_PRESSED).convert_alpha(), size)
        }

    @property
    def cursor_on_button(self):
        x, y = pg.mouse.get_pos()
        return 0 <= x - self.x <= self.w and 0 <= y - self.y <= self.h

    def set_language(self, language):
        pg.font.init()
        text = TEXTS[self.name][language]
        font = pg.font.Font(FONT_2, H(35) if len(text) < 10 else H(29))
        self.text = pg.transform.rotate(font.render(text, True, WHITE), 90)
        self.text_pos = (self.x + (self.w - self.text.get_width()) // 2,
                         self.y + (self.h - self.text.get_height()) // 2)

    def draw(self, screen):
        screen.blit(self.bg[self.clicked], (self.x, self.y))
        screen.blit(self.text, self.text_pos)


__all__ = ["SideButton"]

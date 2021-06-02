import pygame as pg

from constants import WHITE
from data.paths import *
from gui.button import Button
from utils import H


class SideButton(Button):
    """A button that is used in the pause menu
    to switch to a specific window.
    """
    def __init__(self, menu, x, y, texts, sound_player, action, selected=False):
        """(x, y) is topleft of the button. """
        super().__init__(pg.SYSTEM_CURSOR_HAND, sound_player, UI_CLICK, action)
        self.menu = menu

        self.x = x
        self.y = y
        self.w = H(96)
        self.h = H(160)

        self.selected = selected
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
        self.texts = texts
        self.text_surface = None
        self.text_pos = None

        size = (self.w, self.h)
        self.bg = {
            False: pg.transform.scale(pg.image.load(SIDE_BUTTON_BG).convert_alpha(), size),
            True: pg.transform.scale(pg.image.load(SIDE_BUTTON_PRESSED_BG).convert_alpha(), size)
        }

    def set_language(self, language):
        pg.font.init()
        text = self.texts[language]
        font = pg.font.Font(CALIBRI_BOLD, H(40) if len(text) < 10 else H(30))
        self.text_surface = pg.transform.rotate(font.render(text, True, WHITE), 90)
        self.text_pos = (self.x + (self.w - self.text_surface.get_width()) // 2,
                         self.y + (self.h - self.text_surface.get_height()) // 2)

    def draw(self, screen):
        screen.blit(self.bg[self.selected], (self.x, self.y))
        screen.blit(self.text_surface, self.text_pos)


__all__ = ["SideButton"]

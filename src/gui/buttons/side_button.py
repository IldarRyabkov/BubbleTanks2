import pygame as pg

from data.constants import *
from assets.paths import *
from gui.buttons.button import Button
from components.utils import H


class SideButton(Button):
    """A button that is used in the pause menu
    to switch to a specific window.
    """
    def __init__(self, menu, x, y, texts, sound_player, action, selected=False):
        """(x, y) is topleft of the button. """
        super().__init__(pg.SYSTEM_CURSOR_HAND, sound_player, BUTTON_CLICK, action)
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

        self.bg_surface = pg.image.load(SIDE_BUTTON_BG).convert_alpha()
        self.bg_surface = pg.transform.scale(self.bg_surface, (self.w, self.h))

    def set_language(self, language):
        pg.font.init()
        text = self.texts[language]
        font = pg.font.Font(CALIBRI_BOLD, H(40) if len(text) < 10 else H(30))
        self.text_surface = pg.transform.rotate(font.render(text, True, WHITE), 90)
        self.text_pos = (self.x + (self.w - self.text_surface.get_width()) // 2,
                         self.y + (self.h - self.text_surface.get_height()) // 2)

    def set_alpha(self, alpha):
        self.text_surface.set_alpha(alpha)
        self.bg_surface.set_alpha(alpha)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        if animation_state == WAIT:
            self.set_alpha(255)
        if self.menu.is_opening:
            self.set_alpha(round(255 * time_elapsed))
        elif self.menu.is_closing:
            self.set_alpha(round(255 - 255 * time_elapsed))

    def draw(self, screen, animation_state=WAIT):
        if self.selected:
            screen.blit(self.bg_surface, (self.x, self.y))
        screen.blit(self.text_surface, self.text_pos)


__all__ = ["SideButton"]

import pygame as pg

from constants import WHITE
from data.paths import FONT_3, SIDE_BUTTON_BG, SIDE_BUTTON_PRESSED_BG, UI_CLICK
from utils import H


class SideButton:
    """A button that is used in the pause menu
    to switch to a specific window.
    """
    def __init__(self, x, y, texts, sound_player, pressed=False):
        """(x, y) is topleft of the button. """
        self.x = x
        self.y = y

        self.w = H(96)
        self.h = H(160)

        self.pressed = pressed
        self.sound_player = sound_player
        self.click_area = pg.Rect(self.x, self.y, self.w, self.h)

        self.texts = texts
        self.text_surface = None
        self.text_pos = None

        size = (self.w, self.h)
        self.bg = {
            False: pg.transform.scale(pg.image.load(SIDE_BUTTON_BG).convert_alpha(), size),
            True: pg.transform.scale(pg.image.load(SIDE_BUTTON_PRESSED_BG).convert_alpha(), size)
        }

    @property
    def clicked(self):
        if not self.pressed and self.click_area.collidepoint(pg.mouse.get_pos()):
            self.sound_player.play_sound(UI_CLICK)
            return True
        return False

    def set_language(self, language):
        pg.font.init()
        text = self.texts[language]
        font = pg.font.Font(FONT_3, H(35) if len(text) < 10 else H(28))
        self.text_surface = pg.transform.rotate(font.render(text, True, WHITE), 90)
        self.text_pos = (self.x + (self.w - self.text_surface.get_width()) // 2,
                         self.y + (self.h - self.text_surface.get_height()) // 2)

    def draw(self, screen):
        screen.blit(self.bg[self.pressed], (self.x, self.y))
        screen.blit(self.text_surface, self.text_pos)


__all__ = ["SideButton"]

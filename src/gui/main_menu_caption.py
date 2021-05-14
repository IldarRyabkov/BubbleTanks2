import pygame as pg

from gui.text import Text
from data.colors import WHITE
from data.config import SCR_W2, OPEN, State
from data.paths import START_MENU_CAPTION_BG, FONT_1
from utils import H


class MainMenuCaption:
    def __init__(self):
        self.text = Text(SCR_W2, H(405), FONT_1, H(112), WHITE, 1)
        self.image = pg.image.load(START_MENU_CAPTION_BG).convert_alpha()
        self.surface = pg.transform.scale(self.image, (H(1280), H(240)))
        self.alpha = 255

    def set_format(self, state, text):
        if state == State.MAIN_MENU:
            self.text.y = H(405)
            self.text.set_font_size(H(112))
        elif state == State.EXIT_CONFIRMATION:
            self.text.y = H(320)
            self.text.set_font_size(H(70))
        else:
            self.text.y = H(100)
            self.text.set_font_size(H(80))

        self.text.set_text(text)
        if state == State.MAIN_MENU:
            scaled_h = 2*self.text.h + H(20)
        else:
            scaled_h = round(1.2 * self.text.h) + H(25)
        self.surface = pg.transform.scale(self.image, (self.text.w + H(60), scaled_h))
        self.text.set_alpha(self.alpha)
        self.surface.set_alpha(self.alpha)

    def update_alpha(self, animation_state, time_elapsed):
        if animation_state == OPEN:
            alpha = round(255 * time_elapsed)
        else:
            alpha = round(255 - 255 * time_elapsed)
        self.alpha = alpha
        self.text.set_alpha(alpha)
        self.surface.set_alpha(alpha)

    def draw(self, screen):
        x = SCR_W2 - self.surface.get_width() // 2
        y = self.text.y - self.surface.get_height() // 2 + self.text.h // 2.12
        screen.blit(self.surface, (x, y))
        self.text.draw(screen)


__all__ = ["MainMenuCaption"]

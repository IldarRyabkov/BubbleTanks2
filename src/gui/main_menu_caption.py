import pygame as pg

from gui.text_widget import TextWidget
from constants import *
from languages.texts import TEXTS
from data.paths import MAIN_MENU_CAPTION_BG, FONT_1
from utils import H


class State:
    MAIN_PAGE = 0
    SETTINGS = 1
    CREDITS = 2
    LANGUAGES = 3
    RESOLUTIONS = 4
    EXIT_CONFIRMATION = 5


class MainMenuCaption:
    def __init__(self, menu, game):
        self.menu = menu
        self.game = game

        self.text = TextWidget(SCR_W2, H(405), FONT_1, H(112), WHITE, 1)
        self.image = pg.image.load(MAIN_MENU_CAPTION_BG).convert_alpha()
        self.surface = pg.transform.scale(self.image, (H(1280), H(240)))
        self.alpha = 255

    def set_format(self):
        if self.menu.state == State.MAIN_PAGE:
            self.text.y = H(405)
            self.text.set_font_size(H(112))
        elif self.menu.state == State.EXIT_CONFIRMATION:
            self.text.y = H(320)
            self.text.set_font_size(H(70))
        else:
            self.text.y = H(60)
            self.text.set_font_size(H(80))

        self.text.set_text(TEXTS["main menu captions"][self.game.language][self.menu.state])
        if self.menu.state == State.MAIN_PAGE:
            scaled_h = 2*self.text.h + H(60)
        else:
            scaled_h = round(1.3 * self.text.h) + H(20)
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
        y = self.text.y - (self.surface.get_height() - self.text.h) // 1.9
        screen.blit(self.surface, (x, y))
        self.text.draw(screen)


__all__ = ["MainMenuCaption", "State"]

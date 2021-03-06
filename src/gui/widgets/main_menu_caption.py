import pygame as pg

from .text_widget import TextWidget
from .animated_widget import AnimatedWidget
from data.constants import *
from data.languages import TEXTS
from data.states import MainMenuStates as St
from assets.paths import MAIN_MENU_CAPTION_BG, FONT_1
from components.utils import H


class MainMenuCaption(AnimatedWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.game = menu.game

        self.text = TextWidget(SCR_W2, H(405), FONT_1, H(96), WHITE, 1)
        self.image = pg.image.load(MAIN_MENU_CAPTION_BG).convert_alpha()
        self.surface = pg.transform.scale(self.image, (H(1280), H(240)))
        self.alpha = 255

    def set_state(self, state):
        if state == St.SPLASH_SCREEN:
            self.text.y = H(370)
            self.text.set_font_size(H(120))
        elif state == St.MAIN_PAGE:
            self.text.y = H(150)
            self.text.set_font_size(H(96))
        elif state in (St.OVERRIDE_SAVE, St.DELETE_SAVE):
            self.text.y = H(330)
            self.text.set_font_size(H(60))
        elif state == St.EXIT:
            self.text.y = H(330)
            self.text.set_font_size(H(70))
        elif state == St.SETTINGS:
            self.text.y = H(120)
            self.text.set_font_size(H(70))
        elif state == St.CREDITS:
            self.text.y = H(70)
            self.text.set_font_size(H(70))
        elif state == St.RESOLUTIONS:
            self.text.y = H(60)
            self.text.set_font_size(H(62))
        else:
            self.text.y = H(90)
            self.text.set_font_size(H(70))

        self.text.set_text(TEXTS["main menu captions"][self.game.language][state])
        if state == St.MAIN_PAGE:
            scaled_h = 2*self.text.h + H(60)
        elif state == St.SPLASH_SCREEN:
            scaled_h = 2 * self.text.h + H(60)
        else:
            scaled_h = round(1.5 * self.text.h) + H(20)
        self.surface = pg.transform.scale(self.image, (self.text.w + H(60), scaled_h))
        self.text.set_alpha(self.alpha)
        self.surface.set_alpha(self.alpha)

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if animation_state == WAIT:
            return
        if animation_state == OPEN:
            alpha = round(255 * time_elapsed)
        else:
            alpha = round(255 - 255 * time_elapsed)
        self.alpha = alpha
        self.text.set_alpha(alpha)
        self.surface.set_alpha(alpha)

    def draw(self, screen, animation_state=WAIT):
        x = SCR_W2 - self.surface.get_width() // 2
        y = self.text.y - (self.surface.get_height() - self.text.h) // 1.9
        screen.blit(self.surface, (x, y))
        self.text.draw(screen)


__all__ = ["MainMenuCaption"]

import pygame as pg

from data.colors import WHITE, COLOR_KEY
from data.config import *
from data.paths import *
import data.languages.english as eng
import data.languages.russian as rus


class StartMenuCaption:
    def __init__(self):
        self.image = pg.image.load(START_MENU_CAPTION_BG).convert_alpha()
        self.bg = pg.transform.scale(self.image, (SCR_W, int(4/15 * SCR_H)))
        self.text_surface = None
        self.set_language("English")

    def set_language(self, language):
        pg.font.init()
        font = pg.font.Font(FONT_1, int(7/60 * SCR_H))
        if language == "English":
            caption = font.render(eng.START_MENU_CAPTION, True, WHITE)
        else:
            caption = font.render(rus.START_MENU_CAPTION, True, WHITE)
        self.text_surface = pg.Surface((caption.get_size()))
        self.text_surface.fill(COLOR_KEY)
        self.text_surface.set_colorkey(COLOR_KEY)
        self.text_surface.blit(caption, (0, 0))

    def update_alpha(self, time, state):
        if state == START_MENU_HIDE:
            alpha = int(255 * (1 - time / START_MENU_ANIMATION_TIME))
        else:
            alpha = int(255 * time / START_MENU_ANIMATION_TIME)
        self.text_surface.set_alpha(alpha)
        self.bg.set_alpha(alpha)

    def reset(self):
        self.text_surface.set_alpha(255)
        self.bg.set_alpha(255)

    def draw(self, surface):
        surface.blit(self.bg, (0, int(11/30 * SCR_H)))
        surface.blit(self.text_surface, (1 / 32 * SCR_W, int(9 / 20 * SCR_H)))

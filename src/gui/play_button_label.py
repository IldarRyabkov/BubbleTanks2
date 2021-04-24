import pygame as pg
import numpy as np

from data.config import SCR_W2, SCR_H
from data.paths import FONT_1
import data.languages.english as eng
import data.languages.russian as rus


class PlayButtonLabel:
    COLOR_MIN = np.array([39., 146., 197.])
    COLOR_MAX = np.array([255., 255., 255.])
    COLOR_DELTA = 0.005 * (COLOR_MAX - COLOR_MIN)
    pos = None
    text = None
    text_surface = None

    def __init__(self):
        self.color = self.COLOR_MIN.copy()
        pg.font.init()
        self.font = pg.font.Font(FONT_1, int(36 * SCR_H/600))
        self.set_language("English")
        self.text_surface = self.font.render("", True, self.color)

    def set_language(self, language):
        text = eng.PLAY_BUTTON if language == "English" else rus.PLAY_BUTTON
        self.set_pos(text)
        self.text = text
        self.text_surface = self.font.render(text, True, self.color)

    def set_pos(self, text):
        pg.font.init()
        font = pg.font.Font(FONT_1, int(36 * SCR_H/600))
        x = SCR_W2 - font.size(text)[0] // 2
        y = 0.72 * SCR_H - font.size(text)[1] // 2
        self.pos = x, y

    def update_text_surface(self, text=None):
        text = self.text if text is None else text
        self.text_surface = self.font.render(text, True, self.color)

    def scale(self, k, dt):
        self.color += self.COLOR_DELTA * k * dt

    def maximize(self):
        self.color = self.COLOR_MAX.copy()
        self.update_text_surface()

    def minimize(self):
        self.color = self.COLOR_MIN.copy()
        self.update_text_surface("")

    def draw(self, surface):
        surface.blit(self.text_surface, self.pos)
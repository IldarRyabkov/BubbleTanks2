import pygame as pg
from math import hypot

from data.config import *
from data.paths import RUS_FLAG, ENG_FLAG


ENGLISH_BUTTON_POS = 1/15 * SCR_H, 21/20 * SCR_H
RUSSIAN_BUTTON_POS = 7/40 * SCR_H, 21/20 * SCR_H


class LanguageButton:
    VELOCITY = 0.44  * SCR_H/600
    R_MAX = 7/120  * SCR_H
    R_MIN = 5/120  * SCR_H

    def __init__(self, language: str):
        self.language = language
        self.surface = None
        if language == "English":
            self.x, self.y = ENGLISH_BUTTON_POS
            self.image = pg.image.load(ENG_FLAG).convert_alpha()
            self.clicked = True
        else:
            self.x, self.y = RUSSIAN_BUTTON_POS
            self.image = pg.image.load(RUS_FLAG).convert_alpha()
            self.clicked = False
        self.r = self.R_MIN

    def cursor_on_button(self) -> bool:
        x, y = pg.mouse.get_pos()
        return hypot(x - self.x, y - self.y) <= self.r

    def update_size(self, dt):
        cursor_on_button = self.cursor_on_button()
        k = 1 if cursor_on_button else -1
        self.r += 0.12 * k * dt
        if k == 1 and self.r > self.R_MAX:
            self.r = self.R_MAX
        elif k == -1 and self.r < self.R_MIN:
            self.r = self.R_MIN
        diam = int(2 * self.r)
        self.surface = pg.transform.scale(self.image, (diam, diam))

    def update(self, dt, animation_time, state):
        self.update_size(dt)
        if state == START_MENU_HIDE and \
                START_MENU_ANIMATION_TIME * 0.5 <= animation_time <= START_MENU_ANIMATION_TIME * 2/3:
            self.y += self.VELOCITY * dt

        elif state == START_MENU_SHOW and \
                START_MENU_ANIMATION_TIME * 5/6 <= animation_time <= START_MENU_ANIMATION_TIME:
            self.y -= self.VELOCITY * dt

    def reset(self):
        self.r = self.R_MIN
        if self.language == "English":
            self.x, self.y = ENGLISH_BUTTON_POS
        else:
            self.x, self.y = RUSSIAN_BUTTON_POS

    def draw(self, screen):
        screen.blit(self.surface, (int(self.x - self.r), int(self.y - self.r)))
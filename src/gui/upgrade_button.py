import pygame as pg
from math import copysign

from data.colors import *
from data.paths import (FONT_1, FONT_2, UPGRADE_BUTTON_WIDE_TRANSPARENT,
                        UPGRADE_BUTTON_TRANSPARENT, UPGRADE_BUTTON_WIDE,
                        UPGRADE_BUTTON)
from data.config import SCR_W, SCR_H, UPGRADE_MENU_ANIMATION_TIME
from gui.text_box import TextBox


def set_labels(texts, tank_name):
    labels = list()
    pg.font.init()
    font = pg.font.Font(FONT_1, 48)
    labels.append(font.render(texts[0], True, UPG_LABEL_COLOR))
    font = pg.font.Font(FONT_2, 31)
    labels.append(font.render(tank_name, True, BLACK))
    labels.append(font.render(texts[1], True, BLACK))
    labels.append(font.render(texts[2], True, BLACK))
    return labels


def set_texts(text_1, text_2, text_3, center_x):
    texts = list()
    texts.append(TextBox(text_1, None, 31, False, BLACK, (center_x, 312)))
    texts.append(TextBox(text_2, None, 31, False, BLACK, (center_x, 432)))
    texts.append(TextBox(text_3, None, 31, False, BLACK, (8, 536), False))
    return texts


class UpgradeButton:
    def __init__(self, text_0, text_1, text_2, text_3, text_4,
                 text_5, labels, button_type, player_state):

        self.player_state = player_state
        self.button_type = button_type

        self.w = 352 if self.button_type in [1, 2, 3] else 480
        self.h = 736
        self.w2, self.h2 = self.w//2, self.h//2

        if self.button_type in [1, 4]:
            self.x, self.y = -self.w, 160
            self.X0, self.Y0 = -self.w, 160
            self.X1 = 48 if self.button_type == 1 else 104
            self.Y1 = 160
        elif self.button_type == 2:
            self.x, self.y = 464, SCR_H
            self.X0, self.Y0 = 464, SCR_H
            self.X1, self.Y1 = 464, 160
        elif self.button_type in [3, 5]:
            self.x, self.y = SCR_W, 160
            self.X0, self.Y0 = SCR_W, 160
            self.X1 = SCR_W-self.w-48 if self.button_type == 3 else SCR_W-self.w-104
            self.Y1 = 160

        self.vel_x = (self.X1 - self.X0) / UPGRADE_MENU_ANIMATION_TIME
        self.vel_x_sign = copysign(1, self.vel_x)
        self.vel_y = (self.Y1 - self.Y0) / UPGRADE_MENU_ANIMATION_TIME
        self.vel_y_sign = copysign(1, self.vel_y)

        self.labels = set_labels(labels, tank_name=text_0)
        self.texts = set_texts(text_1, text_2, text_3, self.w2)

        if self.button_type in (1, 2, 3):
            self.bg = pg.image.load(UPGRADE_BUTTON).convert_alpha()
            self.bg_transparent = pg.image.load(UPGRADE_BUTTON_TRANSPARENT).convert_alpha()
        else:
            self.bg = pg.image.load(UPGRADE_BUTTON_WIDE).convert_alpha()
            self.bg_transparent = pg.image.load(UPGRADE_BUTTON_WIDE_TRANSPARENT).convert_alpha()
        self.set_bg()

    def set_bg(self):
        for bg in self.bg, self.bg_transparent:
            bg.blit(self.labels[0], ((self.w-self.labels[0].get_size()[0])//2, 6))
            bg.blit(self.labels[1], ((self.w-self.labels[1].get_size()[0])//2, 160))
            bg.blit(self.labels[2], ((self.w-self.labels[2].get_size()[0])//2, 264))
            bg.blit(self.labels[3], ((self.w-self.labels[3].get_size()[0])//2, 384))
            for text in self.texts:
                text.draw(bg)

    def cursor_on_button(self, pos):
        return self.x <= pos[0] <= self.x+self.w and self.y <= pos[1] <= self.y+self.h

    def update(self, dt):
        self.x += self.vel_x * dt
        if self.vel_x_sign * self.x > self.vel_x_sign * self.X1:
            self.x = self.X1
        elif self.vel_x_sign * self.x < self.vel_x_sign * self.X0:
            self.x = self.X0

        self.y += self.vel_y * dt
        if self.vel_y_sign * self.y > self.vel_y_sign * self.Y1:
            self.y = self.Y1
        elif self.vel_y_sign * self.y < self.vel_y_sign * self.Y0:
            self.y = self.Y0

    def draw(self, surface):
        if self.cursor_on_button(pg.mouse.get_pos()):
            surface.blit(self.bg, (int(self.x), int(self.y)))
        else:
            surface.blit(self.bg_transparent, (int(self.x), int(self.y)))
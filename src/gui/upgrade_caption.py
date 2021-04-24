from math import copysign
import pygame as pg

from data.config import UPGRADE_MENU_ANIMATION_TIME
from data.paths import UPGRADE_CAPTION_RUS, UPGRADE_CAPTION_ENG


class UpgradeCaption:
    def __init__(self):
        self.x = 48
        self.y = -128
        self.Y0 = -128
        self.Y1 = 16
        self.vel_y = (self.Y1 - self.Y0) / UPGRADE_MENU_ANIMATION_TIME
        self.vel_y_sign = copysign(1, self.vel_y)
        self.caption = None

    def set_language(self, language):
        img = UPGRADE_CAPTION_ENG if language == "English" else UPGRADE_CAPTION_RUS
        self.caption = pg.image.load(img).convert_alpha()

    def reset_velocity(self):
        self.vel_y = abs(self.vel_y)

    def update_pos(self, dt):
        self.y += self.vel_y * dt
        if self.vel_y_sign * self.y > self.vel_y_sign * self.Y1:
            self.y = self.Y1
        elif self.vel_y_sign * self.y < self.vel_y_sign * self.Y0:
            self.y = self.Y0

    def draw(self, surface):
        surface.blit(self.caption, (self.x, self.y))
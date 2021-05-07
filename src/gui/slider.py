import pygame as pg

from data.colors import *
from utils import H


class Slider:
    def __init__(self, x: int, y: int):
        self.value = 1
        self.x = x
        self.y = y
        self.w = H(400)
        self.h = H(10)
        self.circle_r = int(self.h * 2.5)
        self.circle_x = self.x + self.w - self.circle_r
        self.clicked = False
        self.click_area = pg.Rect(self.x,
                                  self.y + self.h // 2 - self.circle_r,
                                  self.w,
                                  self.circle_r * 2)

    def handle(self, e_type):
        if e_type == pg.MOUSEBUTTONUP:
            self.clicked = False
        elif self.click_area.collidepoint(*pg.mouse.get_pos()):
            self.clicked = True

    def update(self):
        if self.clicked:
            x = pg.mouse.get_pos()[0]
            x_min = self.x + self.circle_r
            if x < x_min:
                self.circle_x = x_min
            else:
                self.circle_x = min(self.x + self.w - self.circle_r, x)
            self.value = (self.circle_x - x_min) / (self.w - 2 * self.circle_r)

    def draw(self, screen):
        r = self.h // 2
        pg.draw.circle(screen, WHITE, (self.x + self.w - r, self.y + r), r)
        pg.draw.rect(screen, WHITE, pg.Rect(self.x + r, self.y, self.w - self.h, self.h))
        pg.draw.circle(screen, BLUE, (self.x + r, self.y + r), r)
        pg.draw.rect(screen, BLUE, pg.Rect(self.x + r, self.y, self.circle_x - self.x, self.h))
        pg.draw.circle(screen, BLUE, (self.circle_x, self.y + r), self.circle_r)
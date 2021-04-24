import pygame as pg
import numpy as np

from gui.play_button_label import PlayButtonLabel
from gui.play_button_triangle import PlayButtonTriangle
from data.config import *

class PlayButtonData:
    K = 0.005
    A_MIN = 3/40 * SCR_H
    A_MAX = 1.75 * A_MIN
    B_MIN = 7/120 * SCR_H
    B_MAX = 1.75 * B_MIN
    COLOR_MIN = np.array([125., 199., 240.])
    COLOR_MAX = np.array([176., 213., 231.])
    COLOR_DELTA = K * (COLOR_MAX - COLOR_MIN)
    A_DELTA = K * (A_MAX - A_MIN)
    B_DELTA = K * (B_MAX - B_MIN)
    VELOCITY = 0.44 * SCR_H/600


class PlayButton(PlayButtonData):
    def __init__(self):
        self.scaling = False
        self.visible = True
        self.x = SCR_W2
        self.y = SCR_H + self.B_MIN
        self.a = self.A_MIN
        self.b = self.B_MIN
        self.color = self.COLOR_MIN.copy()

        self.label = PlayButtonLabel()
        self.triangle = PlayButtonTriangle(self.x, self.y)

    def set_language(self, language):
        self.label.set_language(language)

    def set_pos(self, state):
        if state == START_MENU_HIDE:
            self.x = SCR_W2
            self.y = 0.875 * SCR_H
        elif state == START_MENU_SHOW:
            self.x = SCR_W2
            self.y = SCR_H + self.b
        self.triangle.set_pos(self.x, self.y)

    def cursor_on_button(self) -> bool:
        x, y = pg.mouse.get_pos()
        return (self.x - x) * (self.x - x) / (self.a * self.a) + \
               (self.y - y) * (self.y - y) / (self.b * self.b) <= 1

    def reset(self):
        self.a = self.A_MIN
        self.b = self.B_MIN
        self.scaling = False
        self.visible = True
        self.set_pos(START_MENU_SHOW)
        self.label.minimize()
        self.triangle.minimize()

    def scale(self, k, dt):
        self.a += self.A_DELTA * k * dt
        self.b += self.B_DELTA * k * dt
        self.color += self.COLOR_DELTA * k * dt

    def maximize(self):
        self.a = self.A_MAX
        self.b = self.B_MAX
        self.color = self.COLOR_MAX.copy()

    def minimize(self):
        self.a = self.A_MIN
        self.b = self.B_MIN
        self.color = self.COLOR_MIN.copy()

    def update_size(self, k, dt):
        self.scale(k, dt)
        self.triangle.scale(k, dt)
        self.label.scale(k, dt)

        if k > 0 and self.a > self.A_MAX:
            self.maximize()
            self.triangle.maximize()
            self.label.maximize()
            self.scaling = False

        elif k < 0 and self.a < self.A_MIN:
            self.minimize()
            self.triangle.minimize()
            self.label.minimize()
            self.scaling = False

        else:
            self.label.update_text_surface()
            self.scaling = True

    def move(self, dy):
        self.y += dy
        self.triangle.pos[1] += dy

    def update(self, dt, animation_time, state):
        if state == START_MENU_WAIT:
            k = 1 if self.cursor_on_button() else -1
            self.update_size(k, dt)

        elif state == START_MENU_HIDE:
            if animation_time < 0.2 * START_MENU_ANIMATION_TIME:
                self.visible = True if (animation_time // 50) % 2 else False

            elif animation_time < 0.5 * START_MENU_ANIMATION_TIME:
                self.update_size(-1, dt)

            elif animation_time <= START_MENU_ANIMATION_TIME * 2/3:
                dy = self.VELOCITY * dt
                self.move(dy)

        elif state == START_MENU_SHOW:
            if START_MENU_ANIMATION_TIME * 5/6 <= animation_time\
                    <= START_MENU_ANIMATION_TIME:
                dy = -self.VELOCITY * dt
                self.move(dy)

    def draw(self, surface):
        if self.visible:
            rect = pg.Rect(int(self.x - self.a),
                           int(self.y - self.b),
                           int(2 * self.a),
                           int(2 * self.b))
            pg.draw.ellipse(surface, self.color, rect)
            self.triangle.draw(surface)
        self.label.draw(surface)

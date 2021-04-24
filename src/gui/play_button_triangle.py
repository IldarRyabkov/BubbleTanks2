import numpy as np
import pygame as pg

from data.colors import WHITE
from data.config import SCR_H


class TriangleData:
    COLOR_MIN = np.array([70., 163., 210.])
    COLOR_MAX = np.array([113., 186., 223.])
    COLOR_DELTA = 0.005 * (COLOR_MAX - COLOR_MIN)

    DOTS_MIN = np.array([[-8.0, -15.0], [-8.0, 15.0], [8.0, 0.0]]) * SCR_H/600
    DOTS_MAX = 1.75 * DOTS_MIN
    DOTS_DELTA = 0.005 * (DOTS_MAX - DOTS_MIN)

    EDGE_DOTS_MIN = np.array([[-11.0, -23.0], [-11.0, 23.0], [13.0, 0.0]]) * SCR_H/600
    EDGE_DOTS_MAX = 1.75 * EDGE_DOTS_MIN
    EDGE_DOTS_DELTA = 0.005 * (EDGE_DOTS_MAX - EDGE_DOTS_MIN)


class PlayButtonTriangle(TriangleData):
    pos = None
    dots = None
    edge_dots = None
    color = None

    def __init__(self, x, y):
        self.set_pos(x, y)
        self.minimize()

    def set_pos(self, x, y):
        self.pos = np.array([x, y], dtype=float)

    def scale(self, k, dt):
        self.dots += self.DOTS_DELTA * k * dt
        self.edge_dots += self.EDGE_DOTS_DELTA * k * dt
        self.color += self.COLOR_DELTA * k * dt

    def maximize(self):
        self.dots = self.DOTS_MAX.copy()
        self.edge_dots = self.EDGE_DOTS_MAX.copy()
        self.color = self.COLOR_MAX.copy()

    def minimize(self):
        self.dots = self.DOTS_MIN.copy()
        self.edge_dots = self.EDGE_DOTS_MIN.copy()
        self.color = self.COLOR_MIN.copy()

    def draw(self, surface):
        pg.draw.polygon(surface, WHITE, self.edge_dots + self.pos)
        pg.draw.polygon(surface, self.color, self.dots + self.pos)
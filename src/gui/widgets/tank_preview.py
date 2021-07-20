import pygame as pg
from math import cos, sin

from components.utils import H, HF
from components.circle import make_circles_list
from data.player_tanks import PLAYER_TANKS
from data.guns import GUNS
from data.constants import *
from gui.widgets.widget import Widget


class TankPreview(Widget):
    """Widget that shows player's tank look. """
    def __init__(self, screen_rect, x, y, no_background=False):
        super().__init__()
        self.screen_rect = screen_rect
        self.x = x
        self.y = y
        self.dx = 0
        self.circles = []
        self.guns = []
        self.no_background = no_background

    def set(self, tank):
        """Sets new widget data according to the given tank"""
        preview_data = PLAYER_TANKS[tank]["preview"]
        scale = preview_data["scale"]
        state = preview_data["health state"]
        self.dx = HF(preview_data["dx"])
        self.init_circles(tank, scale, state)
        self.init_guns(tank, scale, state)

    def init_circles(self, tank, scale, state):
        tank_data = PLAYER_TANKS[tank]
        circles_data = []
        for (left, right), indexes in tank_data["circles states"].items():
            if left <= state <= right:
                circles_data = [tank_data["circles"][i] for i in indexes]
                break
        self.circles = make_circles_list(self.screen_rect, circles_data, scale)

    def init_guns(self, tank, scale, state):
        tank_data = PLAYER_TANKS[tank]
        guns_data = []
        for (left, right), indexes in tank_data["guns states"].items():
            if left <= state <= right:
                guns_data = [tank_data["guns"][i] for i in indexes]
                break
        self.guns = [self.make_gun(data, scale) for data in guns_data]

    def make_gun(self, data, scale):
        gun_params = GUNS[data["name"]]
        distance = HF(data["distance"]) * scale
        angle = data["angle"]
        circles = make_circles_list(self.screen_rect, gun_params["circles"], data["scale"] * scale)
        return Gun(distance, angle, circles)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        x = self.x + self.dx
        for circle in self.circles:
            circle.update(x, self.y, dt, 0)
        for gun in self.guns:
            gun.update(x, self.y, dt)

    def draw(self, screen, animation_state=WAIT):
        if not self.no_background:
            pg.draw.circle(screen, WHITE, (self.x, self.y), H(129))
            pg.draw.circle(screen, TANK_BG_COLOR, (self.x, self.y), H(123))
        for circle in self.circles:
            circle.draw(screen)
        for gun in self.guns:
            gun.draw(screen)


class Gun:
    def __init__(self, distance, angle, circles):
        self.distance = distance
        self.angle = angle
        self.circles = circles

    def update(self, xo, yo, dt):
        x = xo + self.distance * cos(self.angle)
        y = yo - self.distance * sin(self.angle)
        for circle in self.circles:
            circle.update(x, y, dt, 0)

    def draw(self, screen, dx=0, dy=0):
        for circle in self.circles:
            circle.draw(screen, dx, dy)


__all__ = ["TankPreview"]

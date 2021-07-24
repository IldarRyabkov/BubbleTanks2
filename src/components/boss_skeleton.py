from math import cos, sin
import pygame as pg

from components.circle import make_circles_list
from components.utils import HF, H
from data.shapes import SHAPES


class SkeletonPart:
    def __init__(self, screen_rect, data: dict):
        self.screen_rect = screen_rect
        self.rect = pg.Rect(0, 0, H(data["width"]), H(data["height"]))
        self.distance = HF(data["distance"])
        self.angle = data["angle"]
        self.circles = make_circles_list(screen_rect, data["circles"])
        self.x = 0
        self.y = 0

    @property
    def is_on_screen(self):
        return self.rect.colliderect(self.screen_rect)

    def move_to(self, x, y):
        self.x = x + self.distance * cos(self.angle)
        self.y = y - self.distance * sin(self.angle)
        for circle in self.circles:
            circle.move_to(self.x, self.y)
        self.rect.center = self.x, self.y

    def draw(self, screen, dx, dy):
        if self.is_on_screen:
            for circle in self.circles:
                if circle.is_on_screen:
                    circle.draw(screen, dx, dy)


class BossSkeleton:
    def __init__(self, screen_rect):
        self.parts = [SkeletonPart(screen_rect, SHAPES[name])
                      for name in SHAPES if name.startswith("skeleton")]

    def move_to(self, x, y):
        for part in self.parts:
            part.move_to(x, y)

    def draw(self, screen, dx, dy):
        for part in self.parts:
            part.draw(screen, dx, dy)


__all__ = ["BossSkeleton"]

import pygame as pg

from .widget import Widget
from data.constants import WAIT


class Mask(Widget):
    def __init__(self, menu, surface):
        super().__init__()
        self.menu = menu
        self.size = 10
        self.index = -1
        self.surfaces = self.create_surfaces(surface)

    def create_surfaces(self, origin: pg.Surface):
        surfaces = []
        for i in range(self.size + 1):
            alpha = round(255 * i / self.size)
            origin.set_alpha(alpha)
            surface = pg.Surface(origin.get_size(), pg.SRCALPHA)
            surface.blit(origin, (0, 0))
            surfaces.append(surface)
        return surfaces

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        if self.menu.is_opening:
            self.index = round(self.size * time_elapsed)
        elif self.menu.is_closing:
            self.index = round(self.size * (1 - time_elapsed))

    def draw(self, screen, animation_state=WAIT):
        screen.blit(self.surfaces[self.index], (0, 0))


_all__ = ["Mask"]

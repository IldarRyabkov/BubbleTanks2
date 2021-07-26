import pygame as pg

from .widget import Widget
from data.constants import WAIT


class Mask(Widget):
    def __init__(self, menu, surface):
        super().__init__()
        self.menu = menu
        self.n_frames = 11
        self.index = -1
        self.frames = self.create_frames(surface)

    def create_frames(self, origin: pg.Surface):
        frames = []
        for i in range(self.n_frames):
            alpha = round(255 * i / (self.n_frames - 1))
            origin.set_alpha(alpha)
            surface = pg.Surface(origin.get_size(), pg.SRCALPHA)
            surface.blit(origin, (0, 0))
            frames.append(surface)
        return frames

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        if self.menu.is_opening:
            self.index = min(self.n_frames - 1, int(self.n_frames * time_elapsed))
        elif self.menu.is_closing:
            self.index = min(self.n_frames - 1, int(self.n_frames * (1 - time_elapsed)))
        else:
            self.index = self.n_frames - 1

    def draw(self, screen, animation_state=WAIT):
        screen.blit(self.frames[self.index], (0, 0))


_all__ = ["Mask"]

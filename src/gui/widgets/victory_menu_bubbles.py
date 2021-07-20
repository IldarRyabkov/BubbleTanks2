import pygame as pg

from components.bubble import Bubble
from components.utils import *
from data.constants import *
from gui.widgets.animated_widget import AnimatedWidget


class VictoryMenuBubbles(AnimatedWidget):
    def __init__(self, menu, screen_rect, y):
        super().__init__()
        self.menu = menu
        self.screen_rect = screen_rect

        self.bubbles = (
            Bubble(self.screen_rect, SCR_W2 - H(192), y, 0, 0, "ultra"),
            Bubble(self.screen_rect, SCR_W2 + H(192), y, 0, 0, "ultra"),
            Bubble(self.screen_rect, SCR_W2, y, 0, 0, "ultra")
        )
        for bubble in self.bubbles:
            bubble.vel = 0

        self.surface = pg.Surface((H(500), H(100)), pg.SRCALPHA)
        self.surface_pos = SCR_W2 - H(250), y - H(50)

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        for bubble in self.bubbles:
            bubble.update_body(dt)
        if self.menu.is_opening:
            self.surface.set_alpha(round(255 * time_elapsed))
        elif self.menu.is_closing:
            self.surface.set_alpha(round(255 - 255 * time_elapsed))

    def draw(self, screen, animation_state=WAIT):
        if self.menu.is_closing or self.menu.is_opening:
            self.surface.fill((0, 0, 0, 0))
            for bubble in self.bubbles:
                bubble.draw(self.surface, *self.surface_pos)
            screen.blit(self.surface, self.surface_pos)
        else:
            for bubble in self.bubbles:
                bubble.draw(screen)


__all__ = ["VictoryMenuBubbles"]

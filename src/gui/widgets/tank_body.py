import pygame as pg

from components.body import Body
from components.utils import H
from data.tank_bodies import TANK_BODIES
from data.constants import *
from gui.widgets.widget import Widget


class TankBody(Widget):
    """Widget that shows player's tank look. """
    def __init__(self, x, y, no_background=False):
        super().__init__()
        self.x = x
        self.y = y
        self.body = None
        self.no_background=no_background

    def set_body(self, tank):
        self.body = Body(TANK_BODIES[tank])

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        self.body.update(self.x, self.y, dt, target_x=9000, target_y=self.y)

    def draw(self, screen, animation_state=WAIT):
        if not self.no_background:
            pg.draw.circle(screen, WHITE, (self.x, self.y), H(129))
            pg.draw.circle(screen, TANK_BG_COLOR, (self.x, self.y), H(123))
        self.body.draw(screen)


__all__ = ["TankBody"]

import pygame as pg

from body import Body
from data.tank_bodies import TANK_BODIES
from utils import H
from constants import *


class TankBody:
    """Tank body used in stats window to show player's tank look. """
    def __init__(self, xo, player):
        self.player = player
        self.pos = (xo + H(940), H(370))
        self.body = None

    def set_body(self):
        self.body = Body(TANK_BODIES[self.player.tank])

    def update(self, dt, animation_state, time_elapsed):
        self.body.update(*self.pos, dt, target_x=9000)

    def draw(self, screen):
        pg.draw.circle(screen, WHITE, self.pos, H(129))
        pg.draw.circle(screen, TANK_BG_COLOR, self.pos, H(123))
        self.body.draw(screen)


__all__ = ["TankBody"]

from numpy import array
from random import uniform

from constants import SCR_W2, SCR_H2
from utils import HF


class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = array([0., 0.])
        self.shaking = False
        self.shaking_offset = array([0., 0.])
        self.shaking_time = 0
        self.shaking_duration = 0

    def start_shaking(self, duration):
        self.shaking = True
        self.shaking_time = 0
        self.shaking_duration = duration

    def stop_shaking(self):
        self.shaking = False
        self.shaking_offset = array([0., 0.])
        self.shaking_time = 0

    def update(self, dt):
        if self.shaking:
            dx = uniform(-HF(0.9), HF(0.9)) * dt
            dy = uniform(-HF(0.9), HF(0.9)) * dt
            self.shaking_offset = array([dx, dy])
            self.shaking_time += dt
            if self.shaking_time >= self.shaking_duration:
                self.stop_shaking()

        player_pos = array([self.player.x - SCR_W2, self.player.y - SCR_H2])
        self.offset = player_pos + self.shaking_offset


__all__ = ["Camera"]

from random import uniform

from data.constants import *
from .utils import *


class Camera:
    def __init__(self, player):
        self.player = player
        self.dx = 0
        self.dy = 0
        self.shaking = False
        self.shaking_dx = 0
        self.shaking_dy = 0
        self.shaking_time = 0
        self.shaking_duration = 0

    @property
    def offset(self):
        return self.dx, self.dy

    def start_shaking(self, duration):
        self.shaking = True
        self.shaking_time = 0
        self.shaking_duration = duration

    def stop_shaking(self):
        self.shaking = False
        self.shaking_dx = 0
        self.shaking_dy = 0
        self.shaking_time = 0

    def update(self, dt):
        if self.shaking:
            self.shaking_dx = uniform(-HF(0.9), HF(0.9)) * dt
            self.shaking_dy = uniform(-HF(0.9), HF(0.9)) * dt
            self.shaking_time += dt
            if self.shaking_time >= self.shaking_duration:
                self.stop_shaking()

        self.dx = self.player.x - SCR_W2 + self.shaking_dx
        self.dy = self.player.y - SCR_H2 + self.shaking_dy


__all__ = ["Camera"]

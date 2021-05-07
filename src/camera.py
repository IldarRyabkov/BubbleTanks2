from numpy import array

from data.config import SCR_W2, SCR_H2
from utils import HF


class Camera:
    def __init__(self):
        self.offset = array([0, 0])
        self.shaking = False
        self.shaking_offset = array([0, 0])
        self.shaking_vel = 0
        self.shaking_time = 0
        self.shaking_temp_time = 0
        self.shaking_duration = 0

    @property
    def dx(self):
        return self.offset[0]

    @property
    def dy(self):
        return self.offset[1]

    def start_shaking(self, duration):
        self.shaking = True
        self.shaking_vel = HF(16) / (0.25 * duration)
        self.shaking_duration = duration

    def stop_shaking(self):
        self.shaking = False
        self.shaking_offset = array([0, 0])
        self.shaking_time = 0
        self.shaking_temp_time = 0

    def update_shaking_direction(self, dt):
        self.shaking_temp_time += dt
        if self.shaking_temp_time >= 0.25 * self.shaking_duration:
            self.shaking_temp_time = 0
            self.shaking_vel *= -1

    def shake(self, dt):
        self.shaking_offset += self.shaking_vel * dt
        self.update_shaking_direction(dt)
        self.shaking_time += dt
        if self.shaking_time >= self.shaking_duration:
            self.stop_shaking()

    def update(self, x, y, dt):
        if self.shaking:
            self.shake(dt)
        self.offset = array([x - SCR_W2, y - SCR_H2]) + self.shaking_offset


__all__ = ["Camera"]

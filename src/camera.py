from data.config import SCR_W2, SCR_H2, SCR_H
import numpy as np


class Camera:
    def __init__(self):
        self.offset = np.array([0, 0])
        self.dx = 0
        self.dy = 0
        self.shaking = False
        self.shaking_dx = 0
        self.shaking_dy = 0
        self.shaking_vel = 0
        self.shaking_time = 0
        self.shaking_temp_time = 0
        self.shaking_duration = 0

    def start_shaking(self, duration):
        self.shaking = True
        self.shaking_vel = 1/60 * SCR_H / (0.25 * duration)
        self.shaking_duration = duration

    def stop_shaking(self):
        self.shaking = False
        self.shaking_dx = 0
        self.shaking_dy = 0
        self.shaking_time = 0
        self.shaking_temp_time = 0

    def update_shaking_direction(self, dt):
        self.shaking_temp_time += dt
        if self.shaking_temp_time >= 0.25 * self.shaking_duration:
            self.shaking_temp_time = 0
            self.shaking_vel *= -1

    def shake(self, dt):
        self.shaking_dx += self.shaking_vel * dt
        self.shaking_dy += self.shaking_vel * dt

        self.update_shaking_direction(dt)

        self.shaking_time += dt
        if self.shaking_time >= self.shaking_duration:
            self.stop_shaking()

    def update(self, x, y, dt):
        if self.shaking:
            self.shake(dt)
        self.dx = x - SCR_W2 + self.shaking_dx
        self.dy = y - SCR_H2 + self.shaking_dy
        self.offset = np.array([self.dx, self.dy])
from math import pi

from objects.circle import Circle
from utils import calculate_angle


class Body:
    def __init__(self, data):
        self.angle = 0
        self.circles = [Circle(*params) for params in data]

    def rotate(self, dest_angle, dt):
        while self.angle > pi:
            self.angle -= 2 * pi
        while self.angle < -pi:
            self.angle += 2 * pi
        d_angle = min(0.0002 * pi * dt, abs(dest_angle - self.angle))
        if abs(dest_angle - self.angle) >= pi:
            d_angle *= -1
        if dest_angle < self.angle:
            d_angle *= -1
        self.angle += d_angle

        for circle in self.circles:
            circle.angle += d_angle

    def move(self, dx, dy):
        for circle in self.circles:
            circle.move(dx, dy)

    def move_to(self, x, y):
        for circle in self.circles:
            circle.update(x, y)

    def update(self, x, y, dt=0, target=(0, 0), gamma=0):
        beta = calculate_angle(x, y, target[0], target[1])
        for circle in self.circles:
            circle.update(x, y, dt, target, beta, gamma)

    def draw(self, surface, dx=0, dy=0):
        for circle in self.circles:
            circle.draw(surface, dx, dy)


__all__ = ["Body"]

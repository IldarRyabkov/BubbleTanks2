from math import pi

from circle import Circle
from utils import calculate_angle


class Body:
    def __init__(self, data):
        self.angle = 0
        self.circles = [Circle(*params) for params in data]

    def rotate(self, destination_angle, dt):
        """Method is called when player's tank body should be
        rotated due to tank movement.
        Rotates body to the given destination angle.
        """
        # make sure that -pi <= self.angle <= pi for correct calculations
        if self.angle > pi: self.angle %= -2*pi
        elif self.angle < -pi: self.angle %= 2*pi

        # calculate delta_angle the body should turn
        delta_angle = min(0.0002 * pi * dt, abs(destination_angle - self.angle))
        if destination_angle < self.angle:
            delta_angle *= -1
        if abs(destination_angle - self.angle) > pi:
            delta_angle *= -1
        self.angle += delta_angle

    def move(self, dx, dy):
        for circle in self.circles:
            circle.move(dx, dy)

    def move_to(self, x, y):
        for circle in self.circles:
            circle.update(x, y)

    def update(self, x, y, dt=0, target=(0, 0)):
        angle_to_target = calculate_angle(x, y, *target)
        for circle in self.circles:
            circle.update(x, y, dt, target, angle_to_target, self.angle)

    def draw(self, surface, dx=0, dy=0):
        for circle in self.circles:
            circle.draw(surface, dx, dy)


__all__ = ["Body"]

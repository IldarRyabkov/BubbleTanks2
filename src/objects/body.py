from math import pi

from objects.circle import Circle
from utils import calculate_angle


class Body:
    def __init__(self, data):
        self.circles = list()
        self.angle = 0
        self.circles = [Circle(*params) for params in data]
        self.randomize_body_scale()

    def randomize_body_scale(self):
        randomize = Circle.randomize_scaling_phase
        for circle in self.circles:
            randomize(circle)

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
        move_circle = Circle.move
        for circle in self.circles:
            move_circle(circle, dx, dy)

    def update(self, x, y, dt=0, target=(0, 0), gamma=0):
        beta = calculate_angle(x, y, target[0], target[1])
        update_circle = Circle.update
        for circle in self.circles:
            update_circle(circle, x, y, dt, target, beta, gamma)

    def draw(self, surface, dx=0, dy=0):
        draw_circle = Circle.draw
        for circle in self.circles:
            draw_circle(circle, surface, dx, dy)
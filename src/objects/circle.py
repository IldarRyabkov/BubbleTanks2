import pygame as pg
from random import uniform
from math import pi, sin ,cos

from data.colors import WHITE, GLARE_COLORS
from utils import calculate_angle, HF


class Glare:
    """Effect of a circle. Each circle has 4 glares. """
    def __init__(self, color, angle, radius_coeff):
        self.x = 0
        self.y = 0
        self.radius = 0
        self.color = color
        self.angle = angle
        self.radius_coeff = radius_coeff

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self, circle_x, circle_y, circle_radius, circle_angle):
        self.x = circle_x + 0.65 * circle_radius * cos(self.angle + circle_angle)
        self.y = circle_y - 0.65 * circle_radius * sin(self.angle + circle_angle)
        self.radius = self.radius_coeff * circle_radius

    def draw(self, surface, dx, dy):
        pg.draw.circle(surface,
                       self.color,
                       (round(self.x - dx), round(self.y - dy)),
                       round(self.radius))


class Circle:
    """Base element for drawing mobs, bullets, bubbles etc. """
    def __init__(self,
                 radius: float,
                 edge: float,
                 color: tuple,
                 dist: float,
                 angle: float,
                 scaling: bool,
                 scaling_speed: float,
                 scaling_amplitude:float,
                 visible: bool,
                 aiming=False,
                 aiming_dist=0,
                 aiming_angle=0,
                 swinging=False,
                 swing_angle=0,
                 rotating=False,
                 rotating_dist=0,
                 rotating_angle=0):
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.max_radius = radius
        self.radius = radius
        self.edge = edge
        self.color = color

        # полярные координаты, которые используются для вычисления
        # позиции круга относительна центра тела моба, этот круг
        # совершает некоторое движение
        self.dist = dist
        self.angle = angle

        # полярные координаты, которые используются для вычисления
        # позиции круга относительна центра тела моба, если для этого
        # круга происходит автоматическая ориентировка относительно
        # некоторой заданной точки (курсора, позиции другого моба и тд)
        self.aiming = aiming
        if self.aiming:
            self.aiming_dist = aiming_dist
            self.aiming_angle = aiming_angle

        # у масштабируемого круга происходят автоматические колебания радиуса
        self.scaling = scaling
        if self.scaling:
            self.scaling_amplitude = scaling_amplitude
            self.scaling_speed = scaling_speed
            self.scaling_phase = uniform(0, 1)

        self.swinging = swinging
        if self.swinging:
            self.swing_dist = 0
            self.swing_angle = swing_angle
            self.swing_direction = 1
            self.swing_vel = HF(0.57)
            self.swing_max_dist = HF(92)

        self.rotating = rotating
        if self.rotating:
            self.rotating_angle = rotating_angle
            self.rotating_dist = rotating_dist

        self.visible = visible

        glare_angle = aiming_angle if self.aiming else angle
        k = pi if glare_angle > 0 else -pi
        b = pi if glare_angle != 0 else 0
        self.glares = (
            Glare(GLARE_COLORS[color][0], b + 0.9 * k, 0.25),
            Glare(GLARE_COLORS[color][0], b + 0.6 * k, 0.17),
            Glare(GLARE_COLORS[color][1], b - 0.25 * k, 0.25),
            Glare(GLARE_COLORS[color][1], b - 0.5 * k, 0.17)
        )

    def update_glares(self, angle: float):
        for glare in self.glares:
            glare.update(self.x, self.y, self.radius - self.edge, angle)

    def scale_radius(self, dt: int):
        d_phase = dt * self.scaling_speed / self.scaling_amplitude
        self.scaling_phase = (self.scaling_phase + d_phase) % 1
        if self.scaling_phase > 0.75:
            d_phase = self.scaling_phase - 1
        elif self.scaling_phase > 0.25:
            d_phase = 0.5 - self.scaling_phase
        else:
            d_phase = self.scaling_phase
        dr = self.scaling_amplitude * d_phase
        self.radius = self.max_radius + dr

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        for glare in self.glares:
            glare.move(dx, dy)

    def swing(self, dt: int, angle: float):
        dr = self.swing_vel * dt

        if self.swing_direction == 1:
            if abs(self.swing_dist + dr) >= abs(self.swing_max_dist):
                self.swing_dist = self.swing_max_dist
                self.swing_direction *= -1
            else:
                self.swing_dist += dr
        else:
            if abs(self.swing_dist) <= abs(dr):
                self.swing_dist = 0
                self.swing_direction *= -1
            else:
                self.swing_dist -= dr
        dx = self.swing_dist * cos(self.swing_angle + angle)
        dy = -self.swing_dist * sin(self.swing_angle + angle)
        self.move(dx, dy)

    def rotate(self, dt: int):
        self.rotating_angle += 2 * pi * dt / 1000
        self.x += self.rotating_dist * cos(self.rotating_angle)
        self.y -= self.rotating_dist * sin(self.rotating_angle)

    def update(self, x, y, dt=0, target=(0, 0), beta=0, gamma=0):
        if self.visible:
            if self.scaling:
                self.scale_radius(dt)

            angle = self.angle + gamma
            self.x = x + self.dist * cos(angle)
            self.y = y - self.dist * sin(angle)

            if self.aiming:
                aiming_angle = calculate_angle(self.x, self.y, target[0], target[1])
                angle = self.aiming_angle + aiming_angle
                self.x += self.aiming_dist * cos(angle)
                self.y -= self.aiming_dist * sin(angle)

            if self.rotating:
                self.rotate(dt)

            if self.swinging:
                self.swing(dt, (beta if self.aiming else gamma))

            self.x += self.dx
            self.y += self.dy

            if self.radius >= 8:
                self.update_glares(angle)

    def draw(self, surface, dx, dy):
        if self.visible:
            x, y, r = round(self.x - dx), round(self.y - dy), round(self.radius)
            if self.edge:
                pg.draw.circle(surface, WHITE, (x, y), r)

            pg.draw.circle(surface, self.color, (x, y), round(r - self.edge))

            if self.radius >= 8:
                for glare in self.glares:
                    glare.draw(surface, dx, dy)

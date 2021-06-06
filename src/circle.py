import pygame as pg
from random import uniform
from math import pi, sin ,cos

from constants import WHITE, GLARE_COLORS
from utils import calculate_angle, HF


_min_radius = HF(6)  # if radius of circle is less than this radius, its glares aren't updated and drawn


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
                 is_scaling=False,
                 scaling_amplitude=0,
                 is_visible=True,
                 is_aiming=False,
                 aiming_dist=0,
                 aiming_angle=0,
                 is_swinging=False,
                 swing_angle=0,
                 swing_dist=0,
                 is_rotating=False,
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
        self.edge_color = WHITE

        # polar coordinates, which are used to calculate the
        # offset of the circle from the center of the body
        self.distance = dist
        self.angle = angle

        # Polar coordinates, which are used to calculate the additional offset
        # of the circle, if this circle is automatically oriented relative to
        # some specified point. Usually such a circle is an element of the enemy's
        # tank cannon, which is automatically directed at the player, or it is an
        # element of the player's tank, which automatically turns towards the cursor position
        self.is_aiming = is_aiming
        self.aiming_distance = aiming_dist
        self.aiming_angle = aiming_angle

        # The scaled circle performs automatic radius fluctuations
        self.is_scaling = is_scaling
        self.scaling_amplitude = scaling_amplitude
        self.scaling_phase_speed = uniform(0.0015, 0.0019)
        self.scaling_phase = uniform(0, 1)

        # The swinging circle additionally performs an automatic swinging motion
        # back and forth in a given direction. Usually such a circle is an element
        # of the body of a mob that releases mines.
        self.is_swinging = is_swinging
        self.swing_distance = 0
        self.swing_distance_max = swing_dist
        self.swing_angle = swing_angle
        self.swing_vel = swing_dist / 160

        # The rotating circle additionally performs an automatic rotating movement
        self.is_rotating = is_rotating
        self.rotating_angle = rotating_angle
        self.rotating_distance = rotating_dist

        # If a circle is not visible, it won't be updated and drawn
        self.is_visible = is_visible

        # Each circle has 4 glares
        glare_angle = aiming_angle if self.is_aiming else angle
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
        self.scaling_phase = (self.scaling_phase + dt * self.scaling_phase_speed) % 1
        if self.scaling_phase > 0.75: d_phase = self.scaling_phase - 1
        elif self.scaling_phase > 0.25: d_phase = 0.5 - self.scaling_phase
        else:  d_phase = self.scaling_phase
        self.radius = self.max_radius + self.scaling_amplitude * d_phase

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        for glare in self.glares:
            glare.move(dx, dy)

    def swing(self, dt: int, angle: float):
        self.swing_distance += self.swing_vel * dt
        if self.swing_distance > self.swing_distance_max:
            self.swing_distance = self.swing_distance_max
            self.swing_vel *= -1
        elif self.swing_distance < 0:
            self.swing_distance = 0
            self.swing_vel *= -1
        dx = self.swing_distance * cos(self.swing_angle + angle)
        dy = -self.swing_distance * sin(self.swing_angle + angle)
        self.move(dx, dy)

    def update(self, body_x, body_y, dt=0, target_x=0, target_y=0, angle_to_target=0, body_angle=0):
        if not self.is_visible:
            return

        if self.is_scaling:
            self.scale_radius(dt)

        angle = self.angle + body_angle
        self.x = body_x + self.distance * cos(angle)
        self.y = body_y - self.distance * sin(angle)

        if self.is_aiming:
            angle = calculate_angle(self.x, self.y, target_x, target_y) + self.aiming_angle
            self.x += self.aiming_distance * cos(angle)
            self.y -= self.aiming_distance * sin(angle)

        if self.is_rotating:
            self.rotating_angle += 0.002 * pi * dt
            self.x += self.rotating_distance * cos(self.rotating_angle)
            self.y -= self.rotating_distance * sin(self.rotating_angle)

        if self.is_swinging:
            self.swing(dt, (angle_to_target if self.is_aiming else body_angle))

        self.x += self.dx
        self.y += self.dy

        if self.radius >= _min_radius:
            self.update_glares(angle)

    def draw(self, surface, dx, dy):
        if not self.is_visible:
            return
        pos, r = (round(self.x - dx), round(self.y - dy)), round(self.radius)
        pg.draw.circle(surface, self.edge_color, pos, r)

        pg.draw.circle(surface, self.color, pos, r - round(self.edge))

        if self.radius >= _min_radius:
            for glare in self.glares:
                glare.draw(surface, dx, dy)


__all__ = ["Circle"]

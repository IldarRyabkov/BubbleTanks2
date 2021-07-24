from math import cos, sin, pi
from random import uniform
import pygame as pg

from data.constants import *
from components.utils import HF


class StaticGlare:
    def __init__(self, color, angle, circle_radius, radius_coeff, offset_factor):
        self.x = 0
        self.y = 0
        self.radius = round(circle_radius * radius_coeff)
        self.color = color
        self.x_offset = offset_factor * circle_radius * cos(angle)
        self.y_offset = -offset_factor * circle_radius * sin(angle)

    def move_to(self, x, y):
        self.x = x + self.x_offset
        self.y = y + self.y_offset

    def draw(self, surface, dx, dy):
        pg.draw.circle(surface, self.color, (round(self.x - dx), round(self.y - dy)), self.radius)


class StaticCircle:
    def __init__(self, screen_rect, color, radius, edge_factor, distance, angle, glares_angle):
        self.x = 0
        self.y = 0
        self.distance = distance
        self.angle = angle
        self.screen_rect = screen_rect
        self.rect = pg.Rect(0, 0, round(2*radius), round(2*radius))
        self.color = color
        self.edge_color = WHITE
        self.radius = radius
        self.edge = edge_factor * radius
        inner_radius = self.radius - self.edge
        self.glares = (
            StaticGlare(GLARE_COLORS[self.color][0], 0.88 * pi + glares_angle, inner_radius, 0.21, 0.64),
            StaticGlare(GLARE_COLORS[self.color][0], 0.6 * pi + glares_angle, inner_radius, 0.16, 0.63),
            StaticGlare(GLARE_COLORS[self.color][1], -0.21 * pi + glares_angle, inner_radius, 0.21, 0.54),
            StaticGlare(GLARE_COLORS[self.color][1], -0.5 * pi + glares_angle, inner_radius, 0.16, 0.52)
        )

    @property
    def is_on_screen(self):
        return self.rect.colliderect(self.screen_rect)

    def move_to(self, xo, yo):
        self.x = xo + self.distance * cos(self.angle)
        self.y = yo - self.distance * sin(self.angle)
        for glare in self.glares:
            glare.move_to(self.x, self.y)
        self.rect.center = self.x, self.y

    def draw(self, screen, dx, dy):
        pos = round(self.x - dx), round(self.y - dy)
        pg.draw.circle(screen, self.edge_color, pos, self.radius)
        pg.draw.circle(screen, self.color, pos, self.radius - self.edge)
        if self.radius >= 6:
            for glare in self.glares:
                glare.draw(screen, dx, dy)


class Glare:
    """Glare of a circle. Each circle has 4 glares. """
    def __init__(self, color, angle, radius_coeff, offset_factor):
        self.x = 0
        self.y = 0
        self.radius = 0
        self.color = color
        self.angle = angle
        self.radius_coeff = radius_coeff
        self.offset_factor = offset_factor

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self, circle_x, circle_y, circle_radius, circle_angle):
        self.x = circle_x + self.offset_factor * circle_radius * cos(self.angle + circle_angle)
        self.y = circle_y - self.offset_factor * circle_radius * sin(self.angle + circle_angle)
        self.radius = self.radius_coeff * circle_radius

    def draw(self, surface, dx, dy):
        pg.draw.circle(surface, self.color, (round(self.x - dx), round(self.y - dy)), self.radius)


class Circle:
    def __init__(self, screen_rect, color, radius, edge_factor, distance, angle, scale=1, edge_color=WHITE):
        self.x = 0
        self.y = 0
        self.radius = radius * scale
        self.max_radius = self.radius
        self.screen_rect = screen_rect
        self.rect = pg.Rect(0, 0, round(2*self.max_radius), round(2*self.max_radius))
        self.edge = edge_factor * self.radius
        self.distance = distance * scale
        self.angle = angle
        self.edge_color = edge_color
        self.color = color

        k = pi if angle >= 0 else -pi
        b = pi if angle != 0 else 0
        self.glares = (
            Glare(GLARE_COLORS[self.color][0], b + 0.88 * k, 0.23, 0.64),
            Glare(GLARE_COLORS[self.color][0], b + 0.6 * k, 0.18, 0.63),
            Glare(GLARE_COLORS[self.color][1], b - 0.21 * k, 0.23, 0.54),
            Glare(GLARE_COLORS[self.color][1], b - 0.5 * k, 0.18, 0.52)
        )

    def become_infected(self):
        if self.color not in INFECTION_COLORS:
            return
        self.color = INFECTION_COLORS[self.color]
        self.edge_color = INFECTION_EDGE_COLOR
        for glare in self.glares:
            glare.color = INFECTION_GLARE_COLORS[glare.color]

    @property
    def is_on_screen(self):
        return self.rect.colliderect(self.screen_rect)

    def update_glares(self, angle_to_target):
        angle = self.angle + angle_to_target
        if self.radius >= 6:
            for glare in self.glares:
                glare.update(self.x, self.y, self.radius - self.edge, angle)

    def update_pos(self, x, y, dt, angle_to_target):
        angle = self.angle + angle_to_target
        self.x = x + self.distance * cos(angle)
        self.y = y - self.distance * sin(angle)
        self.rect.center = self.x, self.y

    def update(self, x, y, dt, angle_to_target):
        self.update_pos(x, y, dt, angle_to_target)
        self.update_glares(angle_to_target)

    def draw(self, surface, dx=0, dy=0):
        r = round(self.radius)
        pos = round(self.x - dx), round(self.y - dy)
        pg.draw.circle(surface, self.edge_color, pos, r)
        pg.draw.circle(surface, self.color, pos, r - self.edge)
        if self.radius >= 6:
            for glare in self.glares:
                glare.draw(surface, dx, dy)


class ScalingCircle(Circle):
    def __init__(self, screen_rect, color, radius, edge_factor,
                 amplitude_factor, distance, angle, scale=1, edge_color=WHITE):
        super().__init__(screen_rect, color, radius, edge_factor, distance, angle, scale=scale, edge_color=edge_color)
        self.phase = uniform(0, 1)
        self.phase_speed = uniform(0.0019, 0.0023)
        self.amplitude = amplitude_factor * self.radius

    def update_pos(self, x, y, dt, angle_to_target):
        angle = self.angle + angle_to_target
        self.x = x + self.distance * cos(angle)
        self.y = y - self.distance * sin(angle)

        self.phase = (self.phase + dt * self.phase_speed) % (4/3)
        k = min(0, 2 * abs(self.phase - 2/3) - 1)
        self.radius = self.max_radius + k * self.amplitude
        self.rect.center = self.x, self.y


class LoopingCircle(Circle):
    def __init__(self, screen_rect, distance, angle, loop_angle, scale=1):
        super().__init__(screen_rect, BLUE, HF(16.863), 8/75, distance, angle, scale)
        self.max_offset = HF(39.079) * 6 * scale
        self.offsets = [i * HF(39.079) for i in range(6)]
        self.loop_vel = self.max_offset / 540
        self.loop_angle = loop_angle
        self.loop_rotation = loop_angle

    @property
    def is_on_screen(self):
        return True

    def update_pos(self, x, y, dt, angle_to_target):
        self.loop_rotation = self.loop_angle + angle_to_target
        angle = self.angle + angle_to_target
        self.x = x + self.distance * cos(angle)
        self.y = y - self.distance * sin(angle)
        dr = self.loop_vel * dt
        for i in range(6):
            self.offsets[i] = (self.offsets[i] + dr) % self.max_offset
        self.rect.center = self.x, self.y

    def update_glares(self, angle_to_target):
        for glare in self.glares:
            glare.update(self.x, self.y, self.radius - self.edge, self.loop_rotation)

    def draw(self, surface, dx=0, dy=0):
        cosa = cos(self.loop_rotation)
        sina = sin(self.loop_rotation)
        for offset in self.offsets:
            loop_dx = offset * cosa
            loop_dy = -offset * sina
            glare_dx = dx - loop_dx
            glare_dy = dy - loop_dy
            pos = round(self.x - dx + loop_dx), round(self.y - dy + loop_dy)
            pg.draw.circle(surface, self.edge_color, pos, self.radius)
            pg.draw.circle(surface, self.color, pos, self.radius - self.edge)
            for glare in self.glares:
                glare.draw(surface, glare_dx, glare_dy)


class SwingingCircle(Circle):
    def __init__(self, screen_rect, color, radius, edge_factor, distance,
                 angle, swing_distance_max, swing_angle, scale=1):

        super().__init__(screen_rect, color, radius, edge_factor, distance, angle, scale=scale)
        self.swing_distance = 0
        self.swing_distance_max = swing_distance_max * scale
        self.swing_angle = swing_angle
        self.swing_vel = self.swing_distance_max / 160

    def update_pos(self, x, y, dt, angle_to_target):
        self.x = x + self.distance * cos(self.angle + angle_to_target)
        self.y = y - self.distance * sin(self.angle + angle_to_target)
        self.swing_distance += self.swing_vel * dt
        if self.swing_distance > self.swing_distance_max:
            self.swing_distance = self.swing_distance_max
            self.swing_vel *= -1
        elif self.swing_distance < 0:
            self.swing_distance = 0
            self.swing_vel *= -1
        self.x += self.swing_distance * cos(self.swing_angle + angle_to_target)
        self.y -= self.swing_distance * sin(self.swing_angle + angle_to_target)
        self.rect.center = self.x, self.y


class RotatingCircle(Circle):
    def __init__(self, screen_rect, color, radius, distance, angle, rot_distance, rot_angle, scale=1):
        super().__init__(screen_rect, color, radius, 8/75, distance, angle, scale=scale)
        self.rot_distance = rot_distance * scale
        self.rot_angle = rot_angle

    def update_pos(self, x, y, dt, angle_to_target):
        self.x = x + self.distance * cos(self.angle + angle_to_target)
        self.y = y - self.distance * sin(self.angle + angle_to_target)

        self.rot_angle += 0.00628 * dt
        self.x += self.rot_distance * cos(self.rot_angle)
        self.y -= self.rot_distance * sin(self.rot_angle)
        self.rect.center = self.x, self.y


class DisplacebleCircle(ScalingCircle):
    def __init__(self, screen_rect, color, radius, distance, angle, scale=1):
        super().__init__(screen_rect, color, radius, 8/75, 0.347, distance, angle, scale)
        self.dx = 0
        self.dy = 0

    def draw(self, surface, dx=0, dy=0):
        dx -= self.dx
        dy -= self.dy
        super().draw(surface, dx, dy)


def make_circle(data, scale=1, screen_rect=None):
    if data["type"] == "scaling":
        return ScalingCircle(screen_rect, COLORS[data["color"]], HF(data["radius"]),
                             data["edge factor"], data["amplitude factor"],
                             HF(data["distance"]), data["angle"], scale=scale)

    if data["type"] == "blue":
        return ScalingCircle(screen_rect, BLUE, HF(data["radius"]), 8/75, 0.347,
                             HF(data["distance"]), data["angle"],
                             scale=scale)

    if data["type"] == "thick_blue":
        return ScalingCircle(screen_rect, BLUE, HF(data["radius"]), 1/22, 0.177,
                             HF(data["distance"]), data["angle"],
                             scale=scale)

    if data["type"] == "orange":
        return ScalingCircle(screen_rect, ORANGE, HF(data["radius"]), 8/75, 0.347,
                             HF(data["distance"]), data["angle"],
                             scale=scale)

    if data["type"] == "small bubble":
        return ScalingCircle(screen_rect, BUBBLE_COLOR, HF(13), 8/75, 0.429, 0, 0, scale=scale)

    if data["type"] == "medium bubble":
        return ScalingCircle(screen_rect, BUBBLE_COLOR, HF(16.911), 8/75, 0.429, 0, 0, scale=scale)

    if data["type"] == "large bubble":
        return ScalingCircle(screen_rect, BUBBLE_COLOR, HF(23.885), 8/75, 0.112, 0, 0, scale=scale)

    if data["type"] == "ultra bubble":
        return ScalingCircle(screen_rect, BUBBLE_COLOR_2, HF(30.764), 8/75, 0.112, 0, 0, scale=scale)

    if data["type"] == "swinging":
        edge_factor = data["edge factor"] if "edge factor" in data else 8/75
        return SwingingCircle(screen_rect, COLORS[data["color"]], HF(data["radius"]),
                              edge_factor, HF(data["distance"]), data["angle"],
                              HF(data["swing distance"]), data["swing angle"],
                              scale=scale)

    if data["type"] == "rotating":
        return RotatingCircle(screen_rect, COLORS[data["color"]], HF(data["radius"]),
                              HF(data["distance"]), data["angle"],
                              HF(data["rot distance"]), data["rot angle"],
                              scale=scale)

    if data["type"] == "displaceable":
        return DisplacebleCircle(screen_rect, COLORS[data["color"]], HF(data["radius"]),
                                 HF(data["distance"]), data["angle"], scale=scale)

    if data["type"] == "fixed":
        return Circle(screen_rect, COLORS[data["color"]], HF(data["radius"]),
                      data["edge factor"], HF(data["distance"]), data["angle"], scale=scale)

    if data["type"] == "looping":
        return LoopingCircle(screen_rect, HF(data["distance"]),
                             data["angle"], data["loop angle"], scale=scale)

    if data["type"] == "confusion":
        return ScalingCircle(screen_rect, COLORS["confusion"], HF(data["radius"]),
                             0.053, 0.177, HF(data["distance"]),
                             data["angle"], scale=scale, edge_color=CONFUSION_EDGE_COLOR)

    if data["type"] == "static":
        return StaticCircle(screen_rect, COLORS[data["color"]], HF(data["radius"]),
                            data["edge factor"], HF(data["distance"]), data["angle"],
                            data["glares angle"])


def make_circles_list(screen_rect: pg.Rect, circle_data: list, scale=1) -> list:
    return [make_circle(data, scale, screen_rect) for data in circle_data]


__all__ = ["make_circles_list", "make_circle"]

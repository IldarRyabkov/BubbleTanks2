from random import uniform
from math import hypot, cos, sin
import pygame as pg

from objects.body import Body
from utils import circle_collidepoint, calculate_angle
from data.config import ROOM_RADIUS, SCR_W, SCR_H, SCR_W2, SCR_H2
from data.bubble import *
from data.paths import BUBBLE_HALO


class Bubble:
    def __init__(self,
                 x,
                 y,
                 angle=0,
                 gravitation_radius=0,
                 bubble_type="small"):
        self.x = x
        self.y = y
        self.radius = BUBBLES[bubble_type]["radius"]
        self.health = BUBBLES[bubble_type]["health"]
        self.vel = uniform(0.7, 1.7) * BUBBLE_MAX_VEL
        self.acc = BUBBLE_ACC
        self.angle = angle
        self.gravitation_radius = gravitation_radius
        self.body = Body(BUBBLES[bubble_type]["body"])
        self.base_halo = None
        self.halo = None
        if bubble_type == "big":
            self.base_halo = pg.image.load(BUBBLE_HALO).convert_alpha()
            self.update_halo()

    @property
    def is_outside(self):
        return not circle_collidepoint(SCR_W2, SCR_H2, ROOM_RADIUS, self.x, self.y)

    def in_gravity_zone(self, player_x, player_y):
        return hypot(self.x - player_x, self.y - player_y) <= self.gravitation_radius

    def is_on_screen(self, dx, dy):
        return (-self.radius <= self.x - dx <= SCR_W + self.radius and
                -self.radius <= self.y - dy <= SCR_H + self.radius)

    def maximize_gravity(self):
        self.vel = 2 * BUBBLE_MAX_VEL
        self.gravitation_radius = 2 * ROOM_RADIUS

    def go_to_player(self, x, y, dt):
        self.acc = BUBBLE_ACC
        self.angle = calculate_angle(self.x, self.y, x, y)
        dr = self.vel * dt + self.acc * dt*dt / 2
        dist = hypot(self.x-x, self.y-y)
        if dr > dist:
            self.x = x
            self.y = y
        else:
            self.x += dr * cos(self.angle)
            self.y -= dr * sin(self.angle)
        self.vel += self.acc * dt
        if self.vel >= BUBBLE_MAX_VEL:
            self.vel = BUBBLE_MAX_VEL
            self.acc = 0

    def slow_down(self, dt):
        self.acc = -BUBBLE_ACC
        dr = self.vel * dt + self.acc * dt*dt / 2
        self.x += dr * cos(self.angle)
        self.y -= dr * sin(self.angle)
        dv = self.acc * dt
        if self.vel * (self.vel + dv) < 0:
            self.vel = 0
            self.acc = 0
        else:
            self.vel += dv

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.body.move(dx, dy)

    def update_halo(self):
        diam = round(2.9 * self.body.circles[0].radius)
        self.halo = pg.transform.scale(self.base_halo, (diam, diam))

    def update_body(self, dt):
        self.body.update(self.x, self.y, dt)
        if self.halo is not None:
            self.update_halo()

    def update(self, x, y, dt):
        if self.vel or self.is_on_screen(x - SCR_W2, y - SCR_H2):
            if self.in_gravity_zone(x, y):
                self.go_to_player(x, y, dt)
            elif self.vel:
                self.slow_down(dt)
            self.update_body(dt)

    def draw(self, surface, dx=0, dy=0):
        if self.is_on_screen(dx, dy):
            self.body.draw(surface, dx, dy)
            if self.halo is not None:
                radius = self.halo.get_width() / 2
                x = round(self.x - radius - dx)
                y = round(self.y - radius - dy)
                surface.blit(self.halo, (x, y))

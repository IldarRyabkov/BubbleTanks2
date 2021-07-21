from random import uniform
from math import hypot, cos, sin
import pygame as pg

from components.simple_body import Body
from components.utils import *
from data.constants import *
from data.bubbles import BUBBLES
from assets.paths import BUBBLE_HALO


class Bubble:
    BUBBLE_MAX_VEL = HF(0.7)
    BUBBLE_ACC = HF(0.0024)

    def __init__(self,
                 screen_rect,
                 x,
                 y,
                 angle=0,
                 gravitation_radius=0,
                 bubble_type="medium"):
        self.x = x
        self.y = y

        self.body = Body(self, screen_rect, BUBBLES[bubble_type]["circles"])
        self.radius = self.body.circles[0].max_radius
        self.rect = pg.Rect(0, 0, round(2*self.radius), round(2*self.radius))
        self.rect.center = x, y
        self.screen_rect = screen_rect
        self.health = BUBBLES[bubble_type]["health"]
        self.vel = uniform(0.7, 1.7) * self.BUBBLE_MAX_VEL
        self.acc = -self.BUBBLE_ACC
        self.gravity_vel = 0
        self.max_gravity_vel = self.BUBBLE_MAX_VEL
        self.gravity_acc = self.BUBBLE_ACC
        self.angle = angle
        self.gravity_radius = gravitation_radius

        self.base_halo = None
        self.halo = None
        if bubble_type == "ultra":
            self.base_halo = pg.image.load(BUBBLE_HALO).convert_alpha()
            self.update_halo()

    @property
    def is_outside(self):
        return not circle_collidepoint(SCR_W2, SCR_H2, ROOM_RADIUS, self.x, self.y)

    @property
    def is_on_screen(self):
        return self.rect.colliderect(self.screen_rect)

    def in_gravity_zone(self, player_x, player_y):
        return hypot(self.x - player_x, self.y - player_y) <= self.gravity_radius

    def maximize_gravity(self):
        self.max_gravity_vel = 2 * self.BUBBLE_MAX_VEL
        self.gravity_acc = 5 * self.BUBBLE_ACC
        self.gravity_radius = 2 * ROOM_RADIUS

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.center = self.x, self.y

    def update_halo(self):
        diam = round(2.9 * self.body.circles[0].radius)
        self.halo = pg.transform.scale(self.base_halo, (diam, diam))

    def update_body(self, dt):
        self.body.update_shape(dt)
        if self.halo is not None:
            self.update_halo()

    def update(self, player_x, player_y, dt):
        # update bubble accelerations first
        if self.vel == 0:
            self.acc = 0
        if self.in_gravity_zone(player_x, player_y):
            self.gravity_acc = self.BUBBLE_ACC
        elif self.gravity_vel != 0:
            self.gravity_acc = -self.BUBBLE_ACC
        else:
            self.gravity_acc = 0

        # Then calculate new coordinates using the formula for uniformly accelerated rectilinear motion
        gravity_dr = self.gravity_vel * dt + self.gravity_acc * dt*dt/2
        if gravity_dr > hypot(self.x - player_x, self.y - player_y):
            # if the displacement of the bubble to the player is greater than the
            # distance to the player, then the bubble has passed through the player
            self.x = player_x
            self.y = player_y
        else:
            # Otherwise, a displacement is added to the coordinates as a result of the sum
            # of two movements: the movement of the bubble due to the initial impulse,
            # and movement due to the attraction to the player.
            dr = self.vel * dt + self.acc * dt * dt / 2
            gravity_angle = calculate_angle(self.x, self.y, player_x, player_y)
            self.x += dr * cos(self.angle) + gravity_dr * cos(gravity_angle)
            self.y -= dr * sin(self.angle) + gravity_dr * sin(gravity_angle)

        # After that we update velocities
        self.vel = max(0, self.vel + self.acc * dt)
        if self.gravity_acc > 0:
            self.gravity_vel = min(self.max_gravity_vel, self.gravity_vel + self.gravity_acc * dt)
        else:
            self.gravity_vel = max(0, self.gravity_vel + self.gravity_acc * dt)

        self.rect.center = self.x, self.y
        self.update_body(dt)

    def draw(self, surface, dx=0, dy=0):
        if self.is_on_screen:
            self.body.draw(surface, dx, dy)
            if self.halo is not None:
                radius = self.halo.get_width() / 2
                x = round(self.x - radius - dx)
                y = round(self.y - radius - dy)
                surface.blit(self.halo, (x, y))


__all__ = ["Bubble"]

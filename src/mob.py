from random import uniform, choice
from numpy import sign
from pygame import Rect

from utils import *
from mob_guns import get_gun
from base_mob import BaseMob
from data.mobs import FROZEN_BODY


class Mob(BaseMob):
    def __init__(self, game, screen_rect, name, x, y, health, health_states, bubbles, radius,
                 body, gun_type, angular_vel, body_size, trajectory, random_shift=0):

        super().__init__(x, y, health, health, health_states, radius, body, FROZEN_BODY)

        self.game = game
        self.player = game.player
        self.name = name
        self.gun = get_gun(gun_type, self, game)
        self.bubbles = bubbles
        self.body_rect = Rect(0, 0, body_size, body_size)
        self.screen_rect = screen_rect

        self.xo = x
        self.yo = y

        self.randomize_pos(H(random_shift))
        self.polar_angle = uniform(0, 1000)
        self.angular_vel = angular_vel * uniform(0.9, 1.1) * choice([-1, 1])
        self.trajectory = trajectory

        self.is_paralyzed = False
        self.paralyzed_time = 0

    def shift(self, delta_angle):
        return self.trajectory(self.xo, self.yo, self.polar_angle + delta_angle)

    def randomize_pos(self, shift):
        dx, dy = choice([-shift, shift]), choice([-shift, shift])
        self.x += dx
        self.y += dy
        self.xo += dx
        self.yo += dy

    def update_body_angle(self, dt):
        delta_angle = sign(self.angular_vel) * 0.01
        self.body.angle = calculate_angle(self.x, self.y, *self.shift(delta_angle))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.xo += dx
        self.yo += dy
        self.body.move(dx, dy)
        self.body_rect = self.body_rect.move(dx, dy)

    def update_pos(self, dt):
        self.polar_angle += self.angular_vel * dt
        self.x, self.y = self.trajectory(self.xo, self.yo, self.polar_angle)
        self.body_rect.center = self.x, self.y

    def update_body(self, dt):
        if self.body_rect.colliderect(self.screen_rect):
            self.body.update(self.x, self.y, dt, self.player.x, self.player.y)
        self.body.update_frozen_state(dt)

    def make_paralyzed(self):
        self.is_paralyzed = True
        self.paralyzed_time = 0

    def update_paralyzed_state(self, dt):
        self.paralyzed_time += dt
        if self.paralyzed_time >= 2000:
            self.paralyzed_time = 0
            self.is_paralyzed = False

    def update(self, dt):
        if not self.is_paralyzed:
            if not self.body.is_frozen:
                self.update_pos(dt)
            self.update_body_angle(dt)
            self.gun.update(dt)

        self.update_body(dt)
        self.update_paralyzed_state(dt)

    def draw(self, screen, dx, dy):
        if self.body_rect.colliderect(self.screen_rect):
            self.body.draw(screen, dx, dy)

__all__ = ["Mob"]

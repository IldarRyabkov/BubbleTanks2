import random
import numpy as np
from pygame import Rect

from utils import circle_collidepoint, calculate_angle
from entities.mob_guns import get_gun
from objects.base_mob import BaseMob


class Mob(BaseMob):
    def __init__(self,
                 name,
                 x,
                 y,
                 health,
                 health_states,
                 bubbles,
                 radius,
                 body,
                 gun_type,
                 angular_vel,
                 body_size,
                 trajectory,
                 random_shift=0):

        super().__init__(health, health, health_states, radius, body)
        self.name = name
        self.gun = get_gun(gun_type)
        self.pos_0 = np.array([x, y], dtype=float)
        self.pos = np.array([x, y], dtype=float)
        self.randomize_pos(random_shift)
        self.polar_angle = random.uniform(0, 1000)
        self.angular_vel = random.choice([-angular_vel * random.uniform(0.9, 1.1),
                                          angular_vel * random.uniform(0.9, 1.1)])
        self.trajectory = trajectory
        self.gamma = 0
        self.bubbles = bubbles
        self.body_rect = Rect(0, 0, body_size, body_size)
        self.is_paralysed = False
        self.is_frozen = False
        self.frost_time = 0
        self.paralyzed_time = 0

    def randomize_pos(self, shift):
        d_pos = np.array([random.choice([-shift, shift]),
                          random.choice([-shift, shift])])
        self.pos += d_pos
        self.pos_0 += d_pos

    def collide_bullet(self, x, y, r):
        return circle_collidepoint(*self.pos, self.radius + r, x, y)

    def count_gamma(self):
        d_angle = np.sign(self.angular_vel) * 0.01
        pos = self.trajectory(self.pos_0, self.polar_angle + d_angle)
        return calculate_angle(*self.pos, *pos)

    def move(self, dx, dy):
        self.pos += np.array([dx, dy])
        self.pos_0 += np.array([dx, dy])
        self.body.move(dx, dy)
        self.body_rect = self.body_rect.move(dx, dy)

    def update_pos(self, dt):
        self.polar_angle += self.angular_vel * dt
        self.pos = self.trajectory(self.pos_0, self.polar_angle)
        self.body_rect.center = tuple(self.pos)

    def update_body(self, screen_rect, dt, target=(0, 0)):
        if self.body_rect.colliderect(screen_rect):
            self.body.update(*self.pos, dt, target, self.gamma)

    def make_paralysed(self):
        self.is_paralysed = True
        self.paralyzed_time = 0

    def make_body_frozen(self):
        for i in range(-10, 0):
            self.body.circles[i].visible = True

    def make_body_unfrozen(self):
        for i in range(-10, 0):
            self.body.circles[i].visible = False

    def update_paralysed_state(self, dt):
        if self.is_paralysed:
            self.paralyzed_time += dt
            if self.paralyzed_time >= 2000:
                self.paralyzed_time = 0
                self.is_paralysed = False

    def update(self, target, bullets, screen_rect, dt):
        if not self.is_paralysed:
            if not self.is_frozen:
                self.update_pos(dt)

            self.gun.update_time(dt)
            self.gamma = self.count_gamma()
            self.gun.add_bullets(*self.pos, target, bullets, self.gamma)

        self.update_body(screen_rect, dt, target)
        self.update_paralysed_state(dt)
        self.update_frozen_state(dt)

    def draw(self, surface, dx, dy, screen_rect):
        if self.body_rect.colliderect(screen_rect):
            self.body.draw(surface, dx, dy)

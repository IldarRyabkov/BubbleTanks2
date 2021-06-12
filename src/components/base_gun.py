from math import sin, cos

from data.bullets import BULLET_BODIES
from .bullets import RegularBullet


class BaseGun:
    """A parent class got player's gun and mob guns. """
    def __init__(self, owner, game, cooldown_time, distance, bullet_vel, bullet_dmg, bullet_name):
        self.owner = owner
        self.game = game

        self.cooldown_time = cooldown_time
        self.time = cooldown_time
        self.distance = distance
        self.bullet_vel = bullet_vel
        self.bullet_dmg = bullet_dmg
        self.bullet_body = BULLET_BODIES[bullet_name]
        self.bullet_type = RegularBullet

    @staticmethod
    def offset(distance, angle):
        return distance * cos(angle), -distance * sin(angle)

    def gun_pos(self, angle):
        return self.owner.x + self.distance * cos(angle), self.owner.y - self.distance * sin(angle)

    def update_params(self, owner_health):
        pass

    def update_time(self, dt):
        self.time += dt

    def update(self, dt):
        pass

    def make_bullet(self, x, y, angle, bullet):
        return bullet(x, y, self.bullet_dmg, self.bullet_vel, angle, self.bullet_body)

    def generate_bullets(self):
        pass

__all__ = ["BaseGun"]

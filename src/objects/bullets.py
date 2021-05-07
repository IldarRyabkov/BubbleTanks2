from math import cos, sin, pi, hypot
from random import uniform
import pygame as pg

from data.config import *
from data.bullets import *
from data.colors import *
from objects.body import Body
from utils import circle_collidepoint, calculate_angle, H, HF


class Bullet:
    """ a parent class for all bullets classes """
    def __init__(self, x, y, radius, damage, vel, angle, body):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = vel
        self.vel_x = vel * cos(angle)
        self.vel_y = -vel * sin(angle)
        self.damage = damage
        self.hit_effect = self.set_hit_effect(damage)
        self.body = Body(body) if isinstance(body, list) else body
        self.hit_the_target = False

    @property
    def is_outside(self):
        return not circle_collidepoint(SCR_W2, SCR_H2, ROOM_RADIUS, self.x, self.y)

    @staticmethod
    def set_hit_effect(damage):
        if damage <= -5: return 'BigHitLines'
        if damage: return 'SmallHitLines'
        return 'VioletHitCircle'

    def update_pos(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

    def update_body(self, dt):
        self.body.update(self.x, self.y, dt)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.body.move(dx, dy)

    def draw(self, surface, dx, dy):
        self.body.draw(surface, dx, dy)


class RegularBullet(Bullet):
    """ A bullet with uniform rectilinear motion """
    def __init__(self, x, y, damage, vel, angle, body):
        Bullet.__init__(self, x, y, 0.8 * body[0][0], damage, vel, angle, body)
        self.body.update(self.x, self.y, 0)

    def update_color(self, dt):
        pass

    def update(self, dt):
        self.update_pos(dt)
        self.update_body(dt)
        self.update_color(dt)


class ExplodingBullet(RegularBullet):
    """
     Bullet moves evenly and rectilinearly and explodes
     from contact with the enemy, damaging others.

    """
    def __init__(self, x, y, angle):
        super().__init__(x, y, -20, HF(1.1), angle, BULLETS["BigBullet_1"])

        # bullet switches colors periodically
        self.colors = {1: DARK_RED, -1: LIGHT_RED}
        self.color_switch = 1
        self.T = 80
        self.color_time = 0

    def change_color(self):
        self.color_switch *= -1
        self.body.circles[0].color = self.colors[self.color_switch]

    def update_color(self, dt):
        self.color_time += dt
        if self.color_time >= 0.75 * self.T and self.color_switch == 1:
            self.change_color()
        elif self.color_time >= self.T and self.color_switch == -1:
            self.change_color()
            self.color_time -= self.T


class BombBullet(Bullet):
    """A bullet which is not moving and has a specific body update"""
    def __init__(self, x, y, body):
        Bullet.__init__(self, x, y, HF(18), -10, 0, 0, body)

        angle = uniform(0, 2 * pi)
        for circle in self.body.circles:
            circle.angle += angle
        self.body.update(self.x, self.y, 0)

        # bullet switches colors periodically
        self.colors = {1: self.body.circles[0].color, -1: LIGHT_RED}
        self.color_switch = 1
        self.T = 240
        self.color_time = uniform(0, self.T)

    def change_color(self):
        self.color_switch *= -1
        self.body.circles[3].color = self.colors[self.color_switch]

    def update_color(self, dt):
        self.color_time += dt
        if self.color_time >= 0.75 * self.T and self.color_switch == 1:
            self.change_color()
        elif self.color_time >= self.T and self.color_switch == -1:
            self.change_color()
            self.color_time -= self.T

    def update(self, dt):
        self.update_color(dt)


class Shuriken(Bullet):
    """
    Bullet has two states: 'orbiting', when it rotates around the player;
                           'not orbiting', when it moves as a regular bullet.
    Initially bullet is orbiting. If some target intersects with bullet's searching area,
    bullet starts moving evenly and rectilinearly to a target's position.

    """
    def __init__(self, x, y):
        Bullet.__init__(self, x, y, HF(12), -7, HF(1.6), 0, BULLETS["Shuriken"])
        self.dist = HF(128)
        self.is_orbiting = True
        self.angle = 0
        self.angular_vel = -0.002 * pi
        self.health = 1
        self.search_area_rect = pg.Rect(self.x - H(250), self.y - H(250), H(500), H(500))
        self.update_polar_coords(x, y)
        self.hit_effect = 'RedHitCircle'

    def is_near_mob(self, mob):
        return self.search_area_rect.colliderect(mob.body_rect)

    def update_polar_coords(self, x, y, dt=0):
        self.angle += self.angular_vel * dt
        while self.angle < 0:
            self.angle += 2 * pi

        self.x = x + self.dist * cos(self.angle)
        self.y = y -  self.dist * sin(self.angle)
        self.search_area_rect.center = (self.x, self.y)
        self.body.update(self.x, self.y, 0)

    def set_vel(self, mob):
        """
        Method is called when a target intersected with shiriken searching area.
        Sets x- and y- velocity components according to target position.

        """

        if mob.is_paralysed or mob.is_frozen:
            target = mob.pos
        else:
            dt = hypot(self.x - mob.pos[0], self.y - mob.pos[1]) / self.vel
            target = mob.trajectory(mob.pos_0, mob.polar_angle + mob.angular_vel * dt)
        angle = calculate_angle(self.x, self.y, *target)
        self.vel_x = self.vel * cos(angle)
        self.vel_y = -self.vel * sin(angle)

    def update_pos(self, dt):
        super().update_pos(dt)
        self.search_area_rect.center = (self.x, self.y)
        self.body.update(self.x, self.y, 0)

    def check_targets(self, mobs):
        for mob in mobs:
            if self.is_near_mob(mob):
                self.is_orbiting = False
                self.set_vel(mob)
                break

    def update(self, dt, x, y, mobs):
        if self.is_orbiting:
            self.update_polar_coords(x, y, dt)
            self.check_targets(mobs)
        else:
            self.update_pos(dt)


class HomingMissile(Bullet):
    """ A bullet which moves with constant velocity and follows a moving target.
        Therefore, the x- and y-components of velocity are changing. """
    def __init__(self, x, y, radius, damage, vel, body):
        Bullet.__init__(self, x, y, radius, damage, vel, 0, body)

        self.body.update(self.x, self.y, 0)
        self.health = 1
        self.hit_effect = 'RedHitCircle'

    def collide_bullet(self, x, y, r):
        return circle_collidepoint(self.x, self.y, self.radius + r, x, y)

    def handle_injure(self, damage):
        self.health += damage

    def update_vel(self, angle):
        self.vel_x = self.vel * cos(angle)
        self.vel_y = -self.vel * sin(angle)

    def update(self, dt, target_x=0, target_y=0):
        angle = calculate_angle(self.x, self.y, target_x, target_y)
        self.update_vel(angle)
        self.update_pos(dt)
        self.body.update(self.x, self.y, dt, [target_x, target_y])


class DrillingBullet(Bullet):
    """ A bullet that can pass through many enemies. """
    def __init__(self, x, y, damage, vel, angle, body):
        Bullet.__init__(self, x, y, HF(12), damage, vel, angle, body)

        self.body = pg.transform.rotate(body, angle * 180 / pi)
        self.x = x - self.body.get_width() / 2
        self.y = y - self.body.get_height() / 2
        self.attacked_mobs = []  # contains IDs of mobs attacked by this bullet

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update_body(self, dt):
        pass

    def update(self, dt):
        self.update_pos(dt)

    def draw(self, surface, dx, dy):
        surface.blit(self.body, (int(self.x-dx), int(self.y-dy)))


class FrangibleBullet(Bullet):
    """
     Bullet moves evenly and rectilinearly until its timer achieves fragmentation time.
     After this bullet explodes to form fragments scattering in all directions.
     If bullet collides with an object before fragmentation_time, it deals
     damage as a regular bullet and then disappears.

    """
    def __init__(self, x, y, angle, body):
        Bullet.__init__(self, x, y, HF(20), -40, HF(0.8), angle, body)
        self.body.update(self.x, self.y, 0)
        self.timer = 0
        self.fragmentation_time = 1000

    def create_fragments(self, fragments):
        for i in range(0, 360, 12):
            fragments.append(DrillingBullet(self.x, self.y, -8, HF(2.1), i * pi / 180, BULLETS["SniperBullet"]))

    def update(self, dt, fragments):
        self.update_pos(dt)
        self.body.update(self.x, self.y, dt)

        self.timer = min(self.timer + dt, self.fragmentation_time)
        if self.timer == self.fragmentation_time:
            self.hit_the_target = True
            self.create_fragments(fragments)


__all__ = [

    "RegularBullet",
    "ExplodingBullet",
    "BombBullet",
    "Shuriken",
    "HomingMissile",
    "DrillingBullet",
    "FrangibleBullet"

]
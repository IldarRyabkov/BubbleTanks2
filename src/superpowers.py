import pygame as pg
from math import cos, sin, hypot, pi
import numpy as np
from random import uniform

from objects.bullets import (FrangibleBullet, Shuriken, HomingMissile,
                             BombBullet, RegularBullet, ExplodingBullet)
from data.config import *
from special_effects import add_effect
from data.bullets import (HOMING_MISSILE_BODY_1, BIG_BUL_BODY_1,
                          STICKY_BUL_BODY, BOMB_BUL_BODY_1, GIANT_BUL_BODY)
from objects.body import Body
from data.paths import THUNDER
from utils import calculate_angle

TWO_MISSILES_COORDS = (104, 0.43*pi), (104, -0.43*pi)
THREE_MISSILES_COORDS = (106, 0.88*pi), (106, -0.88*pi), (101, 0)
FOUR_MISSILES_COORDS = (114, 0.55 * pi), (114, -0.55 * pi), (147, 0.8 * pi), (147, -0.8 * pi)


class SuperPower:
    def __init__(self, cooldown_time):
        self.cooldown_time = cooldown_time
        self.time = cooldown_time
        self.on = False
        self.name = type(self).__name__

    def update_time(self, dt):
        self.time = min([self.time + dt, self.cooldown_time])

    def activate(self, *args, **kwargs):
        pass

    def update(self, *params):
        self.update_time(params[0])
        if self.time == self.cooldown_time and self.on:
            self.activate(*params[1::])


class HomingMissiles(SuperPower):
    def __init__(self, coords):
        SuperPower.__init__(self, cooldown_time=2000)
        self.coords = coords

    def get_missiles_coords(self, pos, body_angle):
        if len(self.coords) != 4:
            body_angle = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        coords = list()
        for r, angle in self.coords:
            coords.append(pos + np.array([r * cos(body_angle + angle),
                                          -r * sin(body_angle + angle)]))
        return coords

    def activate(self, pos, bullets, health, body_angle):
        self.time = 0
        missiles_coords = self.get_missiles_coords(pos, body_angle)
        for pos in missiles_coords:
            bullets.append(HomingMissile(*pos, 11, -5, 0.88,
                                         Body(HOMING_MISSILE_BODY_1)))


class NoneSuperPower(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=0)

    def update(self, *args, **kwargs):
        pass


class Armor(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=1000)

    def activate(self, armor_on, top_effects):
        armor_on[0] = True
        self.time = 0
        add_effect('Armor', top_effects, SCR_W2 - 160, SCR_H2 - 160, 160)

    def update_armor_state(self, armor_on):
        if self.time >= 0.5 * self.cooldown_time and armor_on[0]:
            armor_on[0] = False

    def update(self, dt, armor_on, top_effects):
        super().update(dt, armor_on, top_effects)
        self.update_armor_state(armor_on)


class Bombs(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=1000)

    @staticmethod
    def get_bullet_pos(pos):
        mouse_pos = pg.mouse.get_pos()
        angle = calculate_angle(SCR_W2, SCR_H2, *mouse_pos)
        return pos + np.array([-102 * cos(angle), 102 * sin(angle)])

    def activate(self, pos, bullets):
        self.time = 0
        bullet_pos = self.get_bullet_pos(pos)
        bullets.append(BombBullet(*bullet_pos, Body(BOMB_BUL_BODY_1)))


class ParalysingExplosion(SuperPower):
    def __init__(self, size: str):
        if size == "big":
            self.dist = 0
            self.radius = 720
        else:
            self.dist = 75
            self.radius = 480
        SuperPower.__init__(self, cooldown_time=2000)

    def get_explosion_pos(self, pos):
        mouse_pos = pg.mouse.get_pos()
        angle = calculate_angle(SCR_W2, SCR_H2, *mouse_pos)
        return pos + np.array([-self.dist * cos(angle), self.dist * sin(angle)])

    def activate(self, pos, mobs, top_effects, bottom_effects, camera, sound_player):
        self.time = 0
        explosion_pos = self.get_explosion_pos(pos)
        for mob in mobs:
            if hypot(explosion_pos[0] - mob.x, explosion_pos[1] - mob.y) <= self.radius:
                mob.make_paralysed()
                add_effect('StarsAroundMob', top_effects, mob.x, mob.y, mob.radius)
        explosion = 'ParalyzingExplosion' if self.radius == 480 else 'BigParalyzingExplosion'
        add_effect(explosion, bottom_effects, *explosion_pos)
        add_effect('Flash', top_effects)
        camera.start_shaking(250)
        sound_player.play_sound(THUNDER)


class PowerfulExplosion(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=2000)

    @staticmethod
    def get_explosion_pos(pos):
        mouse_pos = pg.mouse.get_pos()
        alpha = calculate_angle(SCR_W2, SCR_H2, *mouse_pos)
        return pos + np.array([-78 * cos(alpha), 78 * sin(alpha)])

    def activate(self, pos, mobs, top_effects, bottom_effects, camera, sound_player):
        coords = self.get_explosion_pos(pos)
        self.time = 0
        for mob in mobs:
            if hypot(coords[0] - mob.x, coords[1] - mob.y) <= 250:
                mob.health -= 20
                mob.update_body_look()
                add_effect('BulletHitLines', top_effects, mob.x, mob.y)
        add_effect('PowerfulExplosion', bottom_effects, *coords)
        add_effect('Flash', top_effects)
        camera.start_shaking(250)
        sound_player.play_sound(THUNDER)


class Teleportation(SuperPower):
    def __init__(self, cooldown):
        SuperPower.__init__(self, cooldown_time=cooldown)

    @staticmethod
    def teleportation_offset():
        mouse_pos = pg.mouse.get_pos()
        return np.array(mouse_pos) - np.array([SCR_W2, SCR_H2])

    def activate(self, pos, top_effects, camera):
        self.time = 0
        add_effect('TeleportationFlash', top_effects, *pos)
        pos += self.teleportation_offset()
        camera.update(*pos, 0)


class Ghost(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=0)

        self.dist = 0
        self.vel = 0.8
        self.offsets = ((0.53, -0.94 * pi),
                        (0.2,  -0.95 * pi),
                        (0.24, -0.92 * pi),
                        (0.18, 0.25 * pi),
                        (0.6,  -0.17 * pi),
                        (0.18, 0.75 * pi),
                        (0.36, -0.63 * pi),
                        (0.4,  pi),
                        (0.5,  -0.95 * pi),
                        (0.25, 0.32 * pi),
                        (0.44, -0.3 * pi),
                        (0.57, 0.34 * pi),
                        (0.6,  -0.18 * pi),
                        (0.3,  0.25 * pi),
                        (0.62, -0.43 * pi),
                        (0.45, 0.94 * pi),
                        (0.59, -0.07 * pi),
                        (0.3,  -0.3 * pi),)

    def update_body(self, body):
        beta = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())

        for i in range(1, len(body.circles)-6):
            body.circles[i].dx = self.offsets[i-1][0] * self.dist * cos(beta + self.offsets[i-1][1])
            body.circles[i].dy = -self.offsets[i-1][0] * self.dist * sin(beta + self.offsets[i-1][1])

    def update(self, dt, invisible, body):
        if self.on:
            invisible[0] = True
            self.update_body(body)
            if self.dist != 160:
                self.dist = min(self.dist + self.vel * dt, 160)

        elif self.dist:
            self.dist = max(self.dist - self.vel * dt, 0)
            self.update_body(body)
            if self.dist == 0:
                invisible[0] = False


class ExplosionStar(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=2000)

    def activate(self, pos, bullets):
        self.time = 0
        beta = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        coords = pos + np.array([82 * cos(beta), -82 * sin(beta)])
        bullets.append(FrangibleBullet(*coords, beta, Body(BIG_BUL_BODY_1)))


class Shurikens(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=333)

    def update(self, dt, pos, shurikens):
        self.time = min(self.cooldown_time, self.time + dt)
        if len(shurikens) < 5 and self.time == self.cooldown_time:
            shurikens.append(Shuriken(*pos, uniform(0, 2*pi)))
            self.time = 0


class StickyCannon(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=300)

    def activate(self, x, y, gamma, target, bullets):
        self.time -= self.cooldown_time
        xo, yo = x + 128 * cos(gamma), y - 128 * sin(gamma)
        angle = calculate_angle(xo, yo, *target)
        pos = (xo + 54 * cos(angle), yo - 54 * sin(angle))
        bullets.append(RegularBullet(*pos, 0, 1.1, angle, Body(STICKY_BUL_BODY)))


class PowerfulCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=1500)

    def activate(self, x, y, target, bullets):
        self.time -= self.cooldown_time
        angle = calculate_angle(x, y, *target)
        pos = (x + 192 * cos(angle), y - 192 * sin(angle))
        bullets.append(ExplodingBullet(*pos, angle))


class StickyExplosion(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=1750)

    def activate(self, pos, bullets):
        self.time -= self.cooldown_time
        for i in range(36):
            angle = i * pi/18
            bullets.append(RegularBullet(*pos, 0, 1.1, angle, Body(STICKY_BUL_BODY)))


class GiantCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=5000)

    def activate(self, x, y, bullets, angle, camera):
        self.time -= self.cooldown_time
        bullets.append(RegularBullet(x, y, 80, 1.0, angle, Body(GIANT_BUL_BODY)))
        camera.start_shaking(500)


def get_superpower(name):
    if name is None: return NoneSuperPower()
    if name == 'Armor': return Armor()
    if name == 'Bombs': return Bombs()
    if name == 'Paralysing_explosion': return ParalysingExplosion("small")
    if name == 'BigParalyzingExplosion': return ParalysingExplosion("big")
    if name == 'Powerful_explosion': return PowerfulExplosion()
    if name == 'Fast_teleportation': return Teleportation(350)
    if name == 'Teleportation': return Teleportation(1200)
    if name == 'Ghost': return Ghost()
    if name == 'TwoHomingMissiles': return HomingMissiles(TWO_MISSILES_COORDS)
    if name == 'ThreeHomingMissiles': return HomingMissiles(THREE_MISSILES_COORDS)
    if name == 'FourHomingMissiles': return HomingMissiles(FOUR_MISSILES_COORDS)
    if name == 'ExplosionStar': return ExplosionStar()
    if name == 'Shurikens': return Shurikens()
    if name == 'StickyCannon': return StickyCannon()
    if name == 'PowerfulCannon': return PowerfulCannon()
    if name == 'StickyExplosion': return StickyExplosion()
    if name == 'GiantCannon': return GiantCannon()

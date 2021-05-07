import pygame as pg
from math import cos, sin, hypot, pi
import numpy as np

from objects.bullets import *
from data.config import *
from data.bullets import *
from data.paths import THUNDER
from entities.special_effects import add_effect
from utils import calculate_angle, HF


TWO_MISSILES_COORDS = (
    (HF(92), 0.43*pi),
    (HF(92), -0.43*pi)
)
THREE_MISSILES_COORDS = (
    (HF(94), 0.88*pi),
    (HF(94), -0.88*pi),
    (HF(90), 0)
)
FOUR_MISSILES_COORDS = (
    (HF(101), 0.55 * pi),
    (HF(101), -0.55 * pi),
    (HF(131), 0.8 * pi),
    (HF(131), -0.8 * pi)
)


class SuperPower:
    """Parent class for all superpowers. """
    def __init__(self, cooldown_time):
        self.cooldown_time = cooldown_time
        self.time = cooldown_time
        self.on = False

    def update_time(self, dt):
        self.time = min([self.time + dt, self.cooldown_time])

    def activate(self, *args, **kwargs):
        pass

    def update(self, *args):
        dt, *params = args
        self.update_time(dt)
        if self.time == self.cooldown_time and self.on:
            self.time = 0
            self.activate(*params)


class HomingMissiles(SuperPower):
    def __init__(self, coords):
        super().__init__(cooldown_time=2000)
        self.coords = coords

    def get_missiles_coords(self, pos, body_angle):
        if len(self.coords) != 4:
            body_angle = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        coords = []
        for r, angle in self.coords:
            coords.append(pos + np.array([r * cos(body_angle + angle), -r * sin(body_angle + angle)]))
        return coords

    def activate(self, pos, bullets, health, body_angle):
        missiles_coords = self.get_missiles_coords(pos, body_angle)
        for pos in missiles_coords:
            bullets.append(HomingMissile(*pos, HF(10), -5, HF(0.93), BULLETS["HomingMissile_1"]))


class NoneSuperPower(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=0)

    def update(self, *args, **kwargs):
        pass


class Armor(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=1000)
        self.r = HF(160)

    def activate(self, top_effects):
        add_effect('Armor', top_effects, SCR_W2 - self.r, SCR_H2 - self.r, self.r)


class Bombs(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=1000)

    @staticmethod
    def get_bullet_pos(pos):
        mouse_pos = pg.mouse.get_pos()
        angle = calculate_angle(SCR_W2, SCR_H2, *mouse_pos)
        return pos + np.array([-HF(91) * cos(angle), HF(91) * sin(angle)])

    def activate(self, pos, bullets):
        bullet_pos = self.get_bullet_pos(pos)
        bullets.append(BombBullet(*bullet_pos, BULLETS["BombBullet_1"]))


class ParalysingExplosion(SuperPower):
    def __init__(self, dist, radius, effect):
        super().__init__(cooldown_time=2000)
        self.dist = dist
        self.radius = radius
        self.effect = effect

    def activate(self, pos, mobs, top_effects, bottom_effects, camera, sound_player):
        mouse_pos = pg.mouse.get_pos()
        angle = calculate_angle(SCR_W2, SCR_H2, *mouse_pos)
        explosion_pos = pos + np.array([-self.dist * cos(angle), self.dist * sin(angle)])

        for mob in mobs:
            if hypot(*(explosion_pos - mob.pos)) <= self.radius:
                mob.make_paralysed()
                add_effect('StarsAroundMob', top_effects, *mob.pos, mob.radius)

        add_effect(self.effect, bottom_effects, *explosion_pos)
        add_effect('Flash', top_effects)
        camera.start_shaking(250)
        sound_player.play_sound(THUNDER)


class PowerfulExplosion(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)

    def activate(self, pos, mobs, top_effects, bottom_effects, camera, sound_player):
        mouse_pos = pg.mouse.get_pos()
        alpha = calculate_angle(SCR_W2, SCR_H2, *mouse_pos)
        explosion_pos = pos + np.array([-HF(69) * cos(alpha), HF(69) * sin(alpha)])

        for mob in mobs:
            if hypot(*(explosion_pos - mob.pos)) <= HF(500):
                mob.health -= 20
                mob.update_body_look()
                add_effect('BulletHitLines', top_effects, *mob.pos)

        add_effect('PowerfulExplosion', bottom_effects, *explosion_pos)
        add_effect('Flash', top_effects)
        camera.start_shaking(250)
        sound_player.play_sound(THUNDER)


class Teleportation(SuperPower):
    def __init__(self, cooldown):
        super().__init__(cooldown_time=cooldown)

    def activate(self, pos, top_effects, camera):
        add_effect('TeleportationFlash', top_effects, *pos)
        mouse_pos = pg.mouse.get_pos()
        teleportation_offset = np.array(mouse_pos) - np.array([SCR_W2, SCR_H2])
        pos += teleportation_offset
        camera.update(*pos, 0)


class Ghost(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=0)
        self.dist = 0
        self.vel = HF(0.7)
        self.offsets = (
            (0.53, -0.94 * pi),
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
            (0.3,  -0.3 * pi)
        )

    def update_body(self, body):
        beta = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        for i, (k, angle) in enumerate(self.offsets):
            body.circles[i + 1].dx = k * self.dist * cos(beta + angle)
            body.circles[i + 1].dy = -k * self.dist * sin(beta + angle)

    def update(self, dt, body):
        if self.on:
            self.update_body(body)
            self.dist = min(self.dist + self.vel * dt, HF(142))
        elif self.dist:
            self.dist = max(self.dist - self.vel * dt, 0)
            self.update_body(body)


class ExplosionStar(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2500)

    def activate(self, pos, bullets):
        beta = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        coords = pos + np.array([HF(73) * cos(beta), -HF(73) * sin(beta)])
        bullets.append(FrangibleBullet(*coords, beta, BULLETS["BigBullet_1"]))


class Shurikens(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=0)
        self.shurikens_cooldown = 200

    def update(self, dt, pos, shurikens):
        self.time = min(self.shurikens_cooldown, self.time + dt)
        if len(shurikens) < 5 and self.time == self.shurikens_cooldown:
            shurikens.append(Shuriken(*pos))
            self.time = 0


class StickyCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=300)

    def activate(self, x, y, gamma, target, bullets):
        xo, yo = x + HF(114) * cos(gamma), y - HF(114) * sin(gamma)
        angle = calculate_angle(xo, yo, *target)
        pos = (xo + HF(48) * cos(angle), yo - HF(48) * sin(angle))
        bullets.append(RegularBullet(*pos, 0, HF(1.1), angle, BULLETS["StickyBullet"]))


class PowerfulCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)

    def activate(self, x, y, target, bullets):
        angle = calculate_angle(x, y, *target)
        pos = (x + HF(171) * cos(angle), y - HF(171) * sin(angle))
        bullets.append(ExplodingBullet(*pos, angle))


class StickyExplosion(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2500)

    def activate(self, pos, bullets):
        for i in range(36):
            angle = i * pi/18
            bullets.append(RegularBullet(*pos, 0, HF(1.1), angle, BULLETS["StickyBullet"]))


class GiantCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=3000)

    def activate(self, x, y, bullets, camera):
        angle = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        bullets.append(RegularBullet(x, y, -50, HF(1.4), angle, BULLETS["GiantBullet"]))
        camera.start_shaking(500)


def get_superpower(name):
    if name is None: return NoneSuperPower()
    if name == 'Armor': return Armor()
    if name == 'Bombs': return Bombs()
    if name == 'Paralysing_explosion': return ParalysingExplosion(HF(67), HF(480), name)
    if name == 'BigParalyzingExplosion': return ParalysingExplosion(0, HF(720), name)
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


__all__ = [

    "HomingMissiles",
    "NoneSuperPower",
    "Armor",
    "Bombs",
    "ParalysingExplosion",
    "PowerfulExplosion",
    "Teleportation",
    "Ghost",
    "ExplosionStar",
    "Shurikens",
    "StickyCannon",
    "PowerfulCannon",
    "StickyExplosion",
    "GiantCannon",
    "get_superpower"

]

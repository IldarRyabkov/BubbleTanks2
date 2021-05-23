import pygame as pg
from math import cos, sin, hypot, pi
import numpy as np

from bullets import *
from constants import *
from data.bullets import *
from data.paths import THUNDER, MOB_DEATH, PLAYER_BULLET_SHOT
from special_effects import add_effect
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
SIX_MISSILES_COORDS = (
    (HF(142), 0.5 * pi),
    (HF(132), 0.65 * pi),
    (HF(132), 0.35 * pi),
    (HF(142), -0.5 * pi),
    (HF(132), -0.65 * pi),
    (HF(132), -0.35 * pi),
)


class SuperPower:
    """Parent class for all superpowers. """
    def __init__(self, cooldown_time):
        self.cooldown_time = cooldown_time
        self.time = cooldown_time
        self.on = False
        self.game = None
        self.player = None

    def update_time(self, dt):
        self.time = min([self.time + dt, self.cooldown_time])

    def activate(self):
        pass

    def update(self, dt):
        self.update_time(dt)
        if self.time == self.cooldown_time and self.on:
            self.time = 0
            self.activate()


class HomingMissiles(SuperPower):
    def __init__(self, coords):
        super().__init__(cooldown_time=2000)
        self.coords = coords

    def activate(self):
        for r, angle in self.coords:
            start_angle = self.player.body.angle + angle
            start_pos = self.player.pos + np.array([r * cos(start_angle), -r * sin(start_angle)])
            bullet = HomingMissile(*start_pos, start_angle, 0.05, HF(10), -5,
                                   HF(0.75), BULLET_BODIES["HomingMissile_1"])
            self.player.homing_bullets.append(bullet)


class NoneSuperPower(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=0)

    def update(self, *args, **kwargs):
        pass


class Armor(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=1000)
        self.r = HF(160)

    def activate(self):
        add_effect('Armor', self.game.room.top_effects, SCR_W2 - self.r, SCR_H2 - self.r, self.r)


class Mines(SuperPower):
    def __init__(self):
        SuperPower.__init__(self, cooldown_time=1000)
        self.dist = HF(91)

    def activate(self):
        angle = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        offset = np.array([-self.dist * cos(angle), self.dist * sin(angle)])
        mine_pos = self.player.pos + offset
        self.player.bullets.append(Mine(*mine_pos, BULLET_BODIES["BombBullet_1"]))
        self.game.sound_player.play_sound(PLAYER_BULLET_SHOT)


class ParalysingExplosion(SuperPower):
    def __init__(self, dist, radius, effect):
        super().__init__(cooldown_time=2000)
        self.dist = dist
        self.radius = radius
        self.effect = effect

    def activate(self):
        angle = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        offset = np.array([-self.dist * cos(angle), self.dist * sin(angle)])
        explosion_pos = self.player.pos + offset

        for mob in self.game.room.mobs:
            if hypot(*(explosion_pos - mob.pos)) <= self.radius:
                mob.make_paralysed()
                add_effect('StarsAroundMob', self.game.room.top_effects, *mob.pos, mob.radius)

        add_effect(self.effect, self.game.room.bottom_effects, *explosion_pos)
        add_effect('Flash', self.game.room.top_effects)
        self.game.camera.start_shaking(250)
        self.game.sound_player.play_sound(THUNDER)


class PowerfulExplosion(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)
        self.dist = HF(69)

    def activate(self):
        alpha = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        offset = np.array([-self.dist * cos(alpha), self.dist * sin(alpha)])
        explosion_pos = self.player.pos + offset

        self.game.sound_player.unlock()
        for mob in self.game.room.mobs:
            if hypot(*(explosion_pos - mob.pos)) <= HF(600):
                mob.health -= 30
                mob.update_body_look()
                if mob.health <= 0:
                    self.game.sound_player.play_sound(MOB_DEATH, False)
                add_effect('BigHitLines', self.game.room.top_effects, *mob.pos)

        add_effect('PowerfulExplosion', self.game.room.bottom_effects, *explosion_pos)
        add_effect('Flash', self.game.room.top_effects)
        self.game.camera.start_shaking(250)
        self.game.sound_player.play_sound(THUNDER)


class Teleportation(SuperPower):
    def __init__(self, cooldown):
        super().__init__(cooldown_time=cooldown)

    def activate(self):
        add_effect('TeleportationFlash', self.game.room.top_effects, *self.player.pos)
        add_effect('Flash', self.game.room.top_effects)
        offset = np.array(pg.mouse.get_pos()) - np.array([SCR_W2, SCR_H2])
        self.player.pos += offset
        self.game.camera.update(*self.player.pos, 0)


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

    def update_body(self):
        body = self.player.body
        for i, (k, angle) in enumerate(self.offsets):
            body.circles[i + 1].dx = k * self.dist * cos(body.angle + angle)
            body.circles[i + 1].dy = -k * self.dist * sin(body.angle + angle)

    def update(self, dt):
        if self.on:
            self.update_body()
            self.dist = min(self.dist + self.vel * dt, HF(142))
        elif self.dist:
            self.dist = max(self.dist - self.vel * dt, 0)
            self.update_body()


class ExplosionStar(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2500)
        self.dist = HF(73)

    def activate(self):
        body_angle = self.player.body.angle
        offset = np.array([self.dist * cos(body_angle), -self.dist * sin(body_angle)])
        pos = self.player.pos + offset
        self.player.bullets.append(FrangibleBullet(*pos, body_angle, BULLET_BODIES["BigBullet_1"]))


class Shurikens(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=0)
        self.shurikens_cooldown = 200

    def update(self, dt):
        self.time = min(self.shurikens_cooldown, self.time + dt)
        if len(self.player.shurikens) < 5 and self.time == self.shurikens_cooldown:
            self.player.shurikens.append(Shuriken(*self.player.pos))
            self.time = 0


class StickyCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=350)
        self.gun_dist = HF(114)
        self.dist = HF(48)

    def activate(self):
        gun_offset =  np.array([self.gun_dist * cos(self.player.body.angle),
                                      -self.gun_dist * sin(self.player.body.angle)])
        gun_pos = self.player.pos + gun_offset
        angle = calculate_angle(*gun_pos, *self.player.get_mouse_pos())
        offset = np.array([self.dist * cos(angle), -self.dist * sin(angle)])
        pos = gun_pos + offset
        self.player.bullets.append(RegularBullet(*pos, 0, HF(1.1), angle, BULLET_BODIES["StickyBullet"]))
        self.game.sound_player.play_sound(PLAYER_BULLET_SHOT)


class PowerfulCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)
        self.dist = HF(171)

    def activate(self):
        angle = self.player.body.angle
        offset = np.array([self.dist * cos(angle), -self.dist * sin(angle)])
        pos = self.player.pos + offset
        self.player.bullets.append(ExplodingBullet(*pos, angle))


class StickyExplosion(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)

    def activate(self):
        x, y = self.player.pos
        for i in range(36):
            angle = i * pi/18
            bullet = RegularBullet(x, y, 0, HF(1.1), angle, BULLET_BODIES["StickyBullet"])
            self.player.bullets.append(bullet)


class GiantCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=3000)

    def activate(self):
        bullet = RegularBullet(*self.player.pos, -50, HF(0.8),
                               self.player.body.angle,
                               BULLET_BODIES["GiantBullet"])
        self.player.bullets.append(bullet)
        add_effect("Flash", self.game.room.top_effects)
        self.game.camera.start_shaking(250)


def get_superpower(name):
    if name is None: return NoneSuperPower()
    if name == 'Armor': return Armor()
    if name == 'Bombs': return Mines()
    if name == 'ParalyzingExplosion': return ParalysingExplosion(HF(67), HF(480), name)
    if name == 'BigParalyzingExplosion': return ParalysingExplosion(0, HF(720), name)
    if name == 'Powerful_explosion': return PowerfulExplosion()
    if name == 'Fast_teleportation': return Teleportation(350)
    if name == 'Teleportation': return Teleportation(1200)
    if name == 'Ghost': return Ghost()
    if name == 'TwoHomingMissiles': return HomingMissiles(TWO_MISSILES_COORDS)
    if name == 'ThreeHomingMissiles': return HomingMissiles(THREE_MISSILES_COORDS)
    if name == 'FourHomingMissiles': return HomingMissiles(FOUR_MISSILES_COORDS)
    if name == 'SixHomingMissiles': return HomingMissiles(SIX_MISSILES_COORDS)
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
    "Mines",
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

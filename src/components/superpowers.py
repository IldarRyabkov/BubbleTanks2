import pygame as pg
from math import cos, sin, hypot, pi

from data.constants import *
from data.bullets import *
from assets.paths import *

from .special_effects import *
from .bullets import *
from .utils import *


two_seekers_coords = (
    (HF(92), 0.43*pi),
    (HF(92), -0.43*pi)
)
three_seekers_coords = (
    (HF(94), 0.88*pi),
    (HF(94), -0.88*pi),
    (HF(90), 0)
)
four_seekers_coords = (
    (HF(101), 0.55 * pi),
    (HF(101), -0.55 * pi),
    (HF(131), 0.8 * pi),
    (HF(131), -0.8 * pi)
)
six_seekers_coords = (
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
        self.update_during_transportation = self.update_time

    def update_params(self, health):
        pass

    def update_time(self, dt):
        self.time += dt

    def activate(self):
        pass

    def update(self, dt):
        self.update_time(dt)
        if self.time >= self.cooldown_time and self.on:
            self.time = 0
            self.activate()
# _________________________________________________________________________________________________


class Seekers(SuperPower):
    def __init__(self, coords=()):
        super().__init__(cooldown_time=2000)
        self.coords = coords

    def activate(self):
        for r, angle in self.coords:
            start_angle = self.player.body.angle + angle
            x = self.player.x + r * cos(start_angle)
            y = self.player.y - r * sin(start_angle)
            seeker = PlayerSeeker(x, y, start_angle)
            self.player.seekers.append(seeker)
# _________________________________________________________________________________________________


class TwoSeekers(Seekers):
    def __init__(self):
        super().__init__(two_seekers_coords)
        self.coords_states = (
            (400, ((HF(66), 0.31*pi), (HF(66), -0.31*pi))),
            (298, ((HF(93), 0.56*pi), (HF(93), -0.56*pi))),
            (248, ((HF(70), 0.785*pi), (HF(70), -0.785*pi))),
            (118, ((HF(79), 0.75*pi), (HF(79), -0.75*pi))),
            (108, ((HF(77), 0.695*pi), (HF(77), -0.695*pi))),
            (98, ((HF(92), 0.43*pi), (HF(92), -0.43*pi)))
        )

    def update_params(self, player_health):
        for health, coords in self.coords_states:
            if player_health <= health:
                self.coords = coords
            else:
                break
# _________________________________________________________________________________________________


class NoneSuperPower(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=0)

    def update(self, *args, **kwargs):
        pass
# _________________________________________________________________________________________________


class Shield(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=1000)
        self.r = HF(160)

    @property
    def shield_on(self) -> bool:
        return self.time < 0.4 * self.cooldown_time

    def activate(self):
        add_effect('Armor', self.game.room.top_effects, SCR_W2 - self.r, SCR_H2 - self.r, self.r)
# _________________________________________________________________________________________________


class Mines(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=1000)
        self.dist = -HF(91)
        self.mine_body = BULLET_BODIES["BombBullet_1"]

    def activate(self):
        angle = self.player.body.angle
        x = self.player.x + self.dist * cos(angle)
        y = self.player.y - self.dist * sin(angle)
        self.player.mines.append(Mine(x, y, self.mine_body))
        self.game.sound_player.play_sound(SHOOT)
# _________________________________________________________________________________________________


class ParalysingExplosion(SuperPower):
    def __init__(self, dist, radius, effect):
        super().__init__(cooldown_time=2000)
        self.dist = dist
        self.radius = radius
        self.effect = effect

    def activate(self):
        angle = self.player.body.angle
        x = self.player.x + self.dist * cos(angle)
        y = self.player.y - self.dist * sin(angle)
        for mob in self.game.room.mobs:
            if hypot(x - mob.x, y - mob.y) <= self.radius:
                mob.make_paralyzed()
                add_effect('StarsAroundMob', self.game.room.top_effects, mob.x, mob.y, mob.radius)
        add_effect(self.effect, self.game.room.bottom_effects, x, y)
        add_effect('Flash', self.game.room.top_effects)
        self.game.camera.start_shaking(300)
# _________________________________________________________________________________________________


class PowerfulExplosion(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)
        self.dist = -HF(69)
        self.radius = HF(600)

    def activate(self):
        angle = self.player.body.angle
        x = self.player.x + self.dist * cos(angle)
        y = self.player.y - self.dist * sin(angle)
        self.game.sound_player.unlock()
        for mob in self.game.room.mobs:
            if hypot(x - mob.x, y - mob.y) <= self.radius:
                mob.health -= 30
                mob.update_body_look()
                if mob.health <= 0:
                    self.game.sound_player.play_sound(ENEMY_DEATH, False)
                add_effect('BigHitLines', self.game.room.top_effects, mob.x, mob.y)

        add_effect('PowerfulExplosion', self.game.room.bottom_effects, x, y)
        add_effect('Flash', self.game.room.top_effects)
        self.game.camera.start_shaking(250)
# _________________________________________________________________________________________________


class Teleportation(SuperPower):
    def __init__(self, cooldown):
        super().__init__(cooldown_time=cooldown)

    def activate(self):
        add_effect('TeleportationFlash', self.game.room.top_effects, self.player.x, self.player.y)
        add_effect('Flash', self.game.room.top_effects)
        x, y = pg.mouse.get_pos()
        self.player.x += x - SCR_W2
        self.player.y += y - SCR_H2
        self.game.camera.update(dt=0)
# _________________________________________________________________________________________________


class Ghost(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=0)
        self.update_during_transportation = self.update
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

    @property
    def disassembled(self):
        return self.on or self.dist != 0

    def update_body(self):
        body = self.player.body
        body_angle = body.angle
        for i, (k, angle) in enumerate(self.offsets):
            body.circles[i + 1].dx = k * self.dist * cos(body_angle + angle)
            body.circles[i + 1].dy = -k * self.dist * sin(body_angle + angle)

    def update(self, dt):
        if self.on:
            self.update_body()
            self.dist = min(self.dist + self.vel * dt, HF(142))
        elif self.dist:
            self.dist = max(self.dist - self.vel * dt, 0)
            self.update_body()
# _________________________________________________________________________________________________


class ExplosionStar(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2500)
        self.dist = HF(73)

    def activate(self):
        body_angle = self.player.body.angle
        x = self.player.x + self.dist * cos(body_angle)
        y = self.player.y - self.dist * sin(body_angle)
        self.player.bullets.append(FrangibleBullet(x, y, body_angle, BULLET_BODIES["BigBullet_1"]))
# _________________________________________________________________________________________________


class OrbitalSeekers(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=200)

    def update(self, dt):
        self.update_time(dt)
        if self.time >= self.cooldown_time and len(self.player.orbital_seekers) < 5:
            self.time = 0
            self.player.orbital_seekers.append(OrbitalSeeker(self.player.x, self.player.y))
# _________________________________________________________________________________________________


class DoomsdayInfect(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)
        self.dist = HF(90)

    def activate(self):
        body_angle = self.player.body.angle
        x = self.player.x + self.dist * cos(body_angle)
        y = self.player.y - self.dist * sin(body_angle)
        self.player.seekers.append(PlayerVirus(x, y, body_angle))


class StickyCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=350)
        self.cannon_dist = HF(102)
        self.dist = HF(48)

    def activate(self):
        body_angle = self.player.body.angle
        cannon_x = self.player.x + self.cannon_dist * cos(body_angle)
        cannon_y = self.player.y - self.cannon_dist * sin(body_angle)
        angle = calculate_angle(cannon_x, cannon_y, *self.player.get_mouse_pos())
        cannon_x += self.dist * cos(angle)
        cannon_y -= self.dist * sin(angle)
        self.player.bullets.append(RegularBullet(cannon_x, cannon_y, 0, HF(1.1),
                                                 angle, BULLET_BODIES["StickyBullet"]))
        self.game.sound_player.play_sound(SHOOT)
# _________________________________________________________________________________________________


class PowerfulCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)
        self.dist = HF(171)

    def activate(self):
        angle = self.player.body.angle
        x = self.player.x + self.dist * cos(angle)
        y = self.player.y - self.dist * sin(angle)
        self.player.bullets.append(ExplodingBullet(x, y, angle))
# _________________________________________________________________________________________________


class StickyExplosion(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)

    def activate(self):
        x = self.player.x
        y = self.player.y
        for i in range(36):
            angle = i * pi/18
            bullet = RegularBullet(x, y, 0, HF(1.1), angle, BULLET_BODIES["StickyBullet"])
            self.player.bullets.append(bullet)
# _________________________________________________________________________________________________


class DroneConversion(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=2000)
        self.dist = -HF(160)
        self.effect_radius = HF(950)

    def activate(self):
        for seeker in self.game.room.seekers:
            seeker.hit_the_target = True
            player_seeker = PlayerSeeker(seeker.x, seeker.y, seeker.body.angle)
            self.player.seekers.append(player_seeker)

        angle = self.player.body.angle
        x = self.player.x + self.dist * cos(angle)
        y = self.player.y - self.dist * sin(angle)
        add_effect("DroneConversion", self.game.room.top_effects, x, y)
        add_effect('Flash', self.game.room.top_effects)
        self.game.camera.start_shaking(600)
# _________________________________________________________________________________________________


class GiantCannon(SuperPower):
    def __init__(self):
        super().__init__(cooldown_time=3000)

    def activate(self):
        bullet = RegularBullet(self.player.x, self.player.y, -50, HF(0.8),
                               self.player.body.angle, BULLET_BODIES["GiantBullet"])
        self.player.bullets.append(bullet)
        add_effect("Flash", self.game.room.top_effects)
        self.game.camera.start_shaking(750)
        self.game.sound_player.play_sound(SHOOT)
# _________________________________________________________________________________________________


def get_superpower(name):
    if name is None: return NoneSuperPower()
    if name == 'Armor': return Shield()
    if name == 'Bombs': return Mines()
    if name == 'ParalyzingExplosion': return ParalysingExplosion(-HF(67), HF(480), name)
    if name == 'BigParalyzingExplosion': return ParalysingExplosion(-HF(20), HF(600), name)
    if name == 'Powerful_explosion': return PowerfulExplosion()
    if name == 'Fast_teleportation': return Teleportation(350)
    if name == 'Teleportation': return Teleportation(1200)
    if name == 'Ghost': return Ghost()
    if name == 'TwoHomingMissiles': return TwoSeekers()
    if name == 'ThreeHomingMissiles': return Seekers(three_seekers_coords)
    if name == 'FourHomingMissiles': return Seekers(four_seekers_coords)
    if name == 'SixHomingMissiles': return Seekers(six_seekers_coords)
    if name == 'ExplosionStar': return ExplosionStar()
    if name == 'Shurikens': return OrbitalSeekers()
    if name == 'DoomsdayInfect': return DoomsdayInfect()
    if name == 'StickyCannon': return StickyCannon()
    if name == 'PowerfulCannon': return PowerfulCannon()
    if name == 'StickyExplosion': return StickyExplosion()
    if name == 'DroneConversion': return DroneConversion()
    if name == 'GiantCannon': return GiantCannon()


__all__ = [

    "Seekers",
    "NoneSuperPower",
    "Shield",
    "Mines",
    "ParalysingExplosion",
    "PowerfulExplosion",
    "Teleportation",
    "Ghost",
    "ExplosionStar",
    "OrbitalSeekers",
    "StickyCannon",
    "PowerfulCannon",
    "StickyExplosion",
    "GiantCannon",
    "DoomsdayInfect",
    "get_superpower"

]

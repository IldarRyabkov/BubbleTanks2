import pygame as pg
from math import cos, sin, hypot, pi

from data.constants import *
from data.superpowers.seekers import SEEKERS_COORDS
from data.superpowers.disassemble import CIRCLE_OFFSETS
from assets.paths import *

from .special_effects import *
from .bullets import *
from .utils import *


class SuperPower:
    """Parent class for all superpowers. """
    def __init__(self, game, player, cooldown):
        self.game = game
        self.screen_rect = self.game.rect
        self.player = player
        self.on = False
        self.state = 0
        self.cooldown = cooldown
        self.time = cooldown
        self.update_during_transportation = self.update_time

    def update_state(self, state):
        """Method is called when player's health has changed.
        Updates superpower state according to new player's health."""
        self.state = state

    def update_time(self, dt):
        self.time += dt

    def activate(self):
        pass

    def update(self, dt):
        self.update_time(dt)
        if self.time >= self.cooldown and self.on:
            self.time = 0
            self.activate()
# _________________________________________________________________________________________________


class Seekers(SuperPower):
    def __init__(self, game, player, coords: dict):
        super().__init__(game, player, 2000)
        self.coords = coords
        self.seeker_vel = HF(0.72)

    def activate(self):
        for r, angle in self.coords[self.state]:
            start_angle = self.player.body.angle + angle
            x = self.player.x + r * cos(start_angle)
            y = self.player.y - r * sin(start_angle)
            seeker = Seeker(self.game, "ally seeker", self.screen_rect, x, y,
                            start_angle, 0.01, -5, self.seeker_vel)
            seeker.update(0)
            self.player.seekers.append(seeker)
# _________________________________________________________________________________________________


class TwoSeekers(Seekers):
    def __init__(self, game, player):
        super().__init__(game, player, SEEKERS_COORDS["two_seekers"])
# _________________________________________________________________________________________________


class ThreeSeekers(Seekers):
    def __init__(self, game, player):
        super().__init__(game, player, SEEKERS_COORDS["three_seekers"])
# _________________________________________________________________________________________________


class FourSeekers(Seekers):
    def __init__(self, game, player):
        super().__init__(game, player, SEEKERS_COORDS["four_seekers"])
# _________________________________________________________________________________________________


class AllySwarm(Seekers):
    def __init__(self, game, player):
        super().__init__(game, player, SEEKERS_COORDS["six_seekers"])
# _________________________________________________________________________________________________


class NoneSuperPower(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 0)

    def update(self, dt):
        pass
# _________________________________________________________________________________________________


class Shield(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 1200)
        self.r = HF(160)

    @property
    def shield_on(self) -> bool:
        return self.time <= 500

    def activate(self):
        add_effect('Shield', self.game.room.top_effects, SCR_W2, SCR_H2)
# _________________________________________________________________________________________________


class Mines(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 800)
        self.gun = player.weapons.current_guns[0]

    def activate(self):
        self.gun.shoot_mine()
        self.game.sound_player.play_sound(SHOOT)
# _________________________________________________________________________________________________


class BaseStunBurst(SuperPower):
    def __init__(self, game, player, offset, radius, effect, cooldown):
        super().__init__(game, player, cooldown)
        self.offset = offset
        self.radius = radius
        self.effect = effect

    def activate(self):
        angle = self.player.body.angle
        x = self.player.x + self.offset * cos(angle)
        y = self.player.y - self.offset * sin(angle)
        for enemy in self.game.room.mobs:
            if hypot(x - enemy.x, y - enemy.y) <= self.radius:
                enemy.become_stunned()
                add_effect('StarsAroundMob', self.game.room.top_effects, enemy.x, enemy.y, enemy.radius)
        add_effect(self.effect, self.game.room.bottom_effects, x, y)
        add_effect('Flash', self.game.room.top_effects)
        self.game.camera.start_shaking(300)
# _________________________________________________________________________________________________


class StunBurst(BaseStunBurst):
    def __init__(self, game, player):
        super().__init__(game, player, -HF(58.64), HF(400), "StunBurst", 2400)
# _________________________________________________________________________________________________


class StunBurstLarge(BaseStunBurst):
    def __init__(self, game, player):
        super().__init__(game, player, -HF(17.834), HF(550), 'StunBurstLarge', 2500)
# _________________________________________________________________________________________________


class AreaBurst(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 2000)
        self.offset = -HF(73.368)
        self.radius = HF(360)

    def update_state(self, state):
        super().update_state(state)
        if state <= 218:
            self.offset = -HF(73.368)
        else:
            self.offset = -HF(28.413)

    def activate(self):
        angle = self.player.body.angle
        x = self.player.x + self.offset * cos(angle)
        y = self.player.y - self.offset * sin(angle)
        for enemy in self.game.room.mobs:
            if hypot(x - enemy.x, y - enemy.y) <= self.radius:
                enemy.receive_damage(-30, play_sound=False)
                add_effect('BigHitaaaasLines', self.game.room.top_effects, enemy.x, enemy.y)

        add_effect('DamageBurstLarge', self.game.room.bottom_effects, x, y)
        add_effect('Flash', self.game.room.top_effects)
        self.game.camera.start_shaking(250)
# _________________________________________________________________________________________________


class Teleport(SuperPower):
    def __init__(self, game, player, cooldown_time=1600):
        super().__init__(game, player, cooldown_time)

    def activate(self):
        add_effect('Teleport', self.game.room.top_effects, self.player.x, self.player.y)
        add_effect('Flash', self.game.room.top_effects)
        x, y = pg.mouse.get_pos()
        self.player.x += x - SCR_W2
        self.player.y += y - SCR_H2
        self.game.camera.update(self.player.x, self.player.y, 0)
# _________________________________________________________________________________________________


class UpgradedTeleport(Teleport):
    def __init__(self, game, player):
        super().__init__(game, player, cooldown_time=300)
# _________________________________________________________________________________________________


class Disassemble(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 0)
        self.update_during_transportation = self.update
        self.disassembly_factor = 0
        self.disassembly_vel = HF(0.006)

    @property
    def disassembled(self):
        return self.on or self.disassembly_factor != 0

    def update_body(self):
        circles = self.player.body.current_circles
        body_angle = self.player.body.angle
        for i, (max_distance, angle) in enumerate(CIRCLE_OFFSETS):
            dr = self.disassembly_factor * max_distance
            circles[i + 1].dx = dr * cos(body_angle + angle)
            circles[i + 1].dy = -dr * sin(body_angle + angle)

    def update(self, dt):
        if self.on:
            self.update_body()
            self.disassembly_factor = min(self.disassembly_factor + self.disassembly_vel * dt, 1)
        elif self.disassembly_factor != 0:
            self.disassembly_factor = max(self.disassembly_factor - self.disassembly_vel * dt, 0)
            self.update_body()
# _________________________________________________________________________________________________


class StarBurstCannon(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 3000)
        self.offset = HF(90.076)

    def activate(self):
        body_angle = self.player.body.angle
        x = self.player.x + self.offset * cos(body_angle)
        y = self.player.y - self.offset * sin(body_angle)
        bullet = FrangibleBullet(self.player, self.screen_rect, x, y, body_angle)
        self.player.bullets.append(bullet)
# _________________________________________________________________________________________________


class OrbitalSeekers(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 240)

    def update(self, dt):
        self.update_time(dt)
        if self.time >= self.cooldown and len(self.player.orbital_seekers) < 5:
            self.time = 0
            seeker = AllyOrbitalSeeker(self.game, self.screen_rect, self.player.x, self.player.y)
            seeker.update(0)
            self.player.orbital_seekers.append(seeker)
# _________________________________________________________________________________________________


class DoomsdayInfect(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 4000)
        self.dist = HF(104.887)

    def activate(self):
        body_angle = self.player.body.angle
        x = self.player.x + self.dist * cos(body_angle)
        y = self.player.y - self.dist * sin(body_angle)
        self.player.seekers.append(AllyInfector(self.game, self.screen_rect, x, y, body_angle))
# _________________________________________________________________________________________________


class StickyCannon(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 400)
        self.gun = player.weapons.current_guns[2]

    def activate(self):
        self.gun.shoot_single()
        self.game.sound_player.play_sound(SHOOT)
# _________________________________________________________________________________________________


class AreaBurstCannon(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 2000)
        self.offset = HF(171)

    def activate(self):
        angle = self.player.body.angle
        x = self.player.x + self.offset * cos(angle)
        y = self.player.y - self.offset * sin(angle)
        self.player.bullets.append(ExplodingBullet(self.screen_rect, x, y, angle))
# _________________________________________________________________________________________________


class StickyBurst(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 2000)
        self.offset = -HF(41.16)

    def activate(self):
        body_angle = self.player.body.angle
        x = self.player.x + self.offset * cos(body_angle)
        y = self.player.y - self.offset * sin(body_angle)
        for i in range(36):
            angle = i * pi/18
            bullet = RegularBullet("sticky", self.screen_rect, x, y, 0, HF(0.9), angle)
            self.player.bullets.append(bullet)
# _________________________________________________________________________________________________


class DroneConversion(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 2000)
        self.offset = -HF(131.788)
        self.effect_radius = HF(950)
        self.seeker_vel = HF(0.72)

    def activate(self):
        for seeker in self.game.room.seekers:
            seeker.killed = True
            ally_seeker = Seeker(self.game, "ally seeker", self.screen_rect, seeker.x,
                                 seeker.y, -seeker.angle, 0.01, -5, self.seeker_vel)
            seeker.update(0)
            self.player.seekers.append(ally_seeker)
        self.game.room.seekers.clear()

        body_angle = self.player.body.angle
        x = self.player.x + self.offset * cos(body_angle)
        y = self.player.y - self.offset * sin(body_angle)
        add_effect("Conversion", self.game.room.top_effects, x, y)
        add_effect("Flash", self.game.room.top_effects)
        self.game.camera.start_shaking(600)
# _________________________________________________________________________________________________


class MassiveCannon(SuperPower):
    def __init__(self, game, player):
        super().__init__(game, player, 2000)
        self.offset = HF(34.458)

    def activate(self):
        angle = self.player.body.angle
        x = self.player.x + self.offset * cos(angle)
        y = self.player.y - self.offset * sin(angle)
        bullet = RegularBullet("massive bullet", self.screen_rect, x, y, -200, HF(0.9), angle)
        self.player.bullets.append(bullet)
        add_effect("Flash", self.game.room.top_effects, *self.player.get_mouse_pos())
        self.game.camera.start_shaking(750)
        self.game.sound_player.play_sound(SHOOT)
# _________________________________________________________________________________________________


_superpowers = {
    (0, 0): NoneSuperPower,
    (1, 0): NoneSuperPower,
    (1, 1): NoneSuperPower,
    (1, 2): NoneSuperPower,
    (2, 0): Shield,
    (2, 1): Shield,
    (2, 2): Mines,
    (2, 3): Mines,
    (3, 0): Teleport,
    (3, 1): TwoSeekers,
    (3, 2): StunBurst,
    (3, 3): AreaBurst,
    (3, 4): StickyCannon,
    (3, 5): FourSeekers,
    (4, 0): UpgradedTeleport,
    (4, 1): StarBurstCannon,
    (4, 2): ThreeSeekers,
    (4, 3): AreaBurstCannon,
    (4, 4): StickyBurst,
    (4, 5): StunBurstLarge,
    (5, 0): Disassemble,
    (5, 1): OrbitalSeekers,
    (5, 2): DoomsdayInfect,
    (5, 3): DroneConversion,
    (5, 4): MassiveCannon,
    (5, 5): AllySwarm
}


def get_superpower(tank, game, player):
    return _superpowers[tank](game, player)


__all__ = [

    "Seekers",
    "NoneSuperPower",
    "Shield",
    "Mines",
    "StunBurst",
    "StunBurstLarge",
    "AreaBurst",
    "Teleport",
    "UpgradedTeleport",
    "Disassemble",
    "StarBurstCannon",
    "OrbitalSeekers",
    "StickyCannon",
    "AreaBurstCannon",
    "StickyBurst",
    "MassiveCannon",
    "DoomsdayInfect",
    "get_superpower"

]

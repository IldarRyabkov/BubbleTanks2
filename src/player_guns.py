from math import pi, hypot
from random import uniform
import pygame as pg

from bullets import *
from data.bullets import BULLET_BODIES
from data.paths import PLAYER_BULLET_SHOT
from utils import *
from constants import *
from base_gun import BaseGun


#_________________________________________________________________________________________________

class Gun(BaseGun):
    def __init__(self, *args):
        super().__init__(*args)

    def update(self, dt):
        self.update_time(dt)
        if self.time >= self.cooldown_time and not self.owner.disassembled and self.owner.shooting:
            self.time = 0
            self.generate_bullets()
            self.game.sound_player.play_sound(PLAYER_BULLET_SHOT)

    def generate_bullets(self):
        angle = calculate_angle(SCR_W2, SCR_H2, *pg.mouse.get_pos())
        x, y = self.gun_pos(angle)
        bullet = self.make_bullet(x, y, angle, self.bullet_type)
        self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class AutoGun(Gun):
    def __init__(self, player, game, cooldown_time, distance, bullet_vel,
                 bullet_dmg, bullet_name, cooldown_time_auto, bullet_auto_coords):

        super().__init__(player, game, cooldown_time, distance, bullet_vel, bullet_dmg, bullet_name)

        self.time_auto = 0
        self.cooldown_time_auto = cooldown_time_auto
        self.bullet_vel_auto = HF(2.4)
        self.bullet_dmg_auto = -1
        self.bullet_body_auto = BULLET_BODIES["SmallBullet_1"]
        self.bullet_auto_coords = bullet_auto_coords

    def generate_bullets_auto(self):
        body_angle = self.owner.body.angle
        player_x = self.owner.x
        player_y = self.owner.y
        mob = min(self.game.room.mobs, key=lambda m: hypot(self.owner.x - m.x, self.owner.y - m.y))

        for distance, angle in self.bullet_auto_coords:
            dx, dy = self.offset(distance, body_angle + angle)
            x = player_x + dx
            y = player_y + dy

            if mob.is_paralyzed or mob.body.is_frozen:
                mob_x, mob_y = mob.x, mob.y
            else:
                dt = hypot(x - mob.x, y - mob.y) / self.bullet_vel_auto
                mob_x, mob_y = mob.shift(mob.angular_vel * dt)

            bullet_angle = calculate_angle(x, y, mob_x, mob_y)
            bullet = RegularBullet(x, y, self.bullet_dmg_auto, self.bullet_vel_auto,
                                   bullet_angle, self.bullet_body_auto)
            self.owner.bullets.append(bullet)

    def update_time(self, dt):
        super().update_time(dt)
        self.time_auto += dt

    def update(self, dt):
        super().update(dt)
        if self.time_auto >= self.cooldown_time_auto and self.game.room.mobs:
            self.time_auto = 0
            self.generate_bullets_auto()
            self.game.sound_player.play_sound(PLAYER_BULLET_SHOT)

#_________________________________________________________________________________________________

class Gun00(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 300, HF(23), HF(1.6), -1, 'SmallBullet_1')

#_________________________________________________________________________________________________

class Gun10(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 100, HF(23), HF(1.6), -1, 'SmallBullet_1')

#_________________________________________________________________________________________________

class Gun11(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 175, HF(23), HF(1.6), -1, 'SmallBullet_1')
        self.bullet_distance = HF(10)

    def generate_bullets(self):
        angle = self.owner.body.angle
        xo, yo = self.gun_pos(angle)
        dy, dx = self.offset(self.bullet_distance, angle)
        for k in (-1, 1):
            bullet = self.make_bullet(xo - k*dx, yo + k*dy, angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun12(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 300, HF(23), HF(1.2), -5, 'BigBullet_1')

#_________________________________________________________________________________________________

class Gun20(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 125, HF(23), HF(1.6), -1, 'SmallBullet_1')
        self.bullet_distance = HF(21)

    def generate_bullets(self):
        angle = self.owner.body.angle
        xo, yo = self.gun_pos(angle)
        for k in (-1, 0, 1):
            bullet_angle = angle - k * 0.17 * pi
            dy, dx = self.offset(self.bullet_distance, bullet_angle)
            bullet = self.make_bullet(xo - k*dx, yo + k*dy, bullet_angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun21(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 150, HF(64), HF(1.6), -1, 'SmallBullet_1')
        self.bullet_distance = HF(21)

    def generate_bullets(self):
        angle = self.owner.body.angle
        xo, yo = self.gun_pos(angle)
        dy, dx = self.offset(self.bullet_distance, angle)
        for k in (-1, 0, 1):
            bullet = self.make_bullet(xo - k*dx, yo + k*dy, angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun23(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 150, HF(64), HF(1.6), -1, 'SmallBullet_1')

    def generate_bullets(self):
        angle = self.owner.body.angle
        xo, yo = self.gun_pos(angle)
        dy1, dx1 = self.offset(HF(21), angle)
        dy2, dx2 = self.offset(HF(42), angle)
        dx3, dy3 = self.offset(HF(5), angle)
        for dx, dy in (0, 0), (-dx1, dy1), (dx1, -dy1), (-dx2-dx3, dy2-dy3), (dx2-dx3, -dy2-dy3):
            bullet = self.make_bullet(xo + dx, yo + dy, angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun30(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 350, HF(14), HF(2.1), -10, 'SniperBullet')
        self.bullet_type = DrillingBullet

#_________________________________________________________________________________________________

class Gun31(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 75, HF(28), HF(1.6), -2, 'SmallBullet_1')

#_________________________________________________________________________________________________

class Gun32(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 150, HF(90), HF(1.6), -1, 'SmallBullet_1')
        self.bullet_offsets = (
            (0, 0),
            (HF(11), -0.075*pi),
            (-HF(11), 0.075*pi),
            (HF(21), -0.15*pi),
            (-HF(21), 0.15*pi)
        )

    def generate_bullets(self):
        angle = self.owner.body.angle
        xo, yo = self.gun_pos(angle)
        for distance, delta_angle in self.bullet_offsets:
            bullet_angle = angle + delta_angle
            dy, dx = self.offset(distance, bullet_angle)
            bullet = self.make_bullet(xo - dx, yo + dy, bullet_angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun34(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 300, HF(114), HF(1.1), -5, 'BigBullet_1')

    def generate_bullets(self):
        angle = self.owner.body.angle
        for k in (-1, 1):
            xo, yo = self.gun_pos(angle + k * 0.76 * pi)
            bullet_angle = calculate_angle(xo, yo, *self.owner.get_mouse_pos())
            dx, dy = self.offset(HF(57), bullet_angle)
            bullet = self.make_bullet(xo + dx, yo + dy, bullet_angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun35(AutoGun):
    def __init__(self, player, game):
        coords = ((HF(124), 0.25 * pi), (HF(124), -0.25 * pi))
        super().__init__(player, game, 200, HF(43), HF(1.2), -5, 'BigBullet_1', 200, coords)

#_________________________________________________________________________________________________

class Gun40(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 425, HF(28), HF(2.1), -15, 'SniperBullet')
        self.bullet_type = DrillingBullet

#_________________________________________________________________________________________________

class Gun41(Gun11):
    def __init__(self, player, game):
        super().__init__(player, game)
        self.cooldown_time = 80

#_________________________________________________________________________________________________

class Gun42(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 200, HF(14), HF(1.6), -1, 'SmallBullet_1')
        self.bullet_distance = HF(76)

    def generate_bullets(self):
        angle = self.owner.body.angle
        xo, yo = self.gun_pos(angle)
        big_bullet = RegularBullet(xo, yo, -5, HF(1.2), angle, BULLET_BODIES["BigBullet_1"])
        self.owner.bullets.append(big_bullet)
        for k in (-1, 1):
            dx, dy = self.offset(self.bullet_distance, angle + k * 0.48 * pi)
            bullet = self.make_bullet(xo + dx, yo + dy, angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun43(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 150, HF(28), HF(1.45), -3, 'MediumBullet_1')

    def generate_bullets(self):
        angle = self.owner.body.angle
        for k in (-1, 1):
            xo, yo = self.gun_pos(angle + k * 0.74 * pi)
            bullet = self.make_bullet(xo, yo, angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun44(AutoGun):
    def __init__(self, player, game):
        coords = ((HF(137), 0.25 * pi), (HF(137), -0.25 * pi))
        super().__init__(player, game, 230, HF(128), HF(1.1), -5, 'BigBullet_1', 200, coords)
        self.bullet_distance = HF(57)

    def generate_bullets(self):
        angle = self.owner.body.angle
        for k in (-1, 1):
            xo, yo = self.gun_pos(angle + k * 0.75 * pi)
            bullet_angle = calculate_angle(xo, yo, *self.owner.get_mouse_pos())
            dx, dy = self.offset(HF(57), bullet_angle)
            bullet = self.make_bullet(xo + dx, yo + dy, bullet_angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun45(AutoGun):
    def __init__(self, player, game):
        coords = ((HF(176), 0.3 * pi), (HF(176), -0.3 * pi), (HF(176), 0))
        super().__init__(player, game, 300, HF(142), HF(1.2), -5, 'BigBullet_1', 300, coords)

    def generate_bullets(self):
        angle = self.owner.body.angle
        for k in (-1, 1):
            xo, yo = self.gun_pos(angle + k * 0.78 * pi)
            bullet_angle = calculate_angle(xo, yo, *self.owner.get_mouse_pos())
            dx, dy = self.offset(HF(57), bullet_angle)
            bullet = self.make_bullet(xo + dx, yo + dy, bullet_angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

class Gun50(Gun40):
    def __init__(self, player, game):
        super().__init__(player, game)
        self.cooldown_time = 500
        self.distance = HF(57)
        self.bullet_dmg = -15

#_________________________________________________________________________________________________

class Gun51(Gun21):
    def __init__(self, player, game):
        super().__init__(player, game)
        self.cooldown_time = 100
        self.distance = HF(21)

#_________________________________________________________________________________________________

class Gun53(Gun):
    def __init__(self, player, game):
        super().__init__(player, game, 1100, HF(140), 0, 0, 'BigDrone')

    def generate_bullets(self):
        xo, yo = self.gun_pos(self.owner.body.angle)
        angle = uniform(0, 2*pi)
        drone = Drone(xo, yo, angle, "BigDrone", self.owner)
        self.owner.drones.append(drone)

#_________________________________________________________________________________________________

class Gun54(AutoGun):
    def __init__(self, player, game):
        coords = (
            (HF(173), 0.22 * pi), (HF(173), -0.22 * pi),
            (HF(248), 0.43 * pi), (HF(248), -0.43 * pi),
            (HF(248), 0.6 * pi), (HF(248), -0.6 * pi)
        )
        super().__init__(player, game, 220, HF(256), HF(1.2), -5, 'BigBullet_1', 300, coords)
        self.air_cannon_distance = HF(173)
        self.bullet_distance = HF(57)

    def generate_bullets(self):
        cursor_pos = self.owner.get_mouse_pos()
        body_angle = self.owner.body.angle
        for k in (-1, 1):
            xo, yo = self.gun_pos(body_angle + k * 0.815 * pi)
            angle = calculate_angle(xo, yo, *cursor_pos)
            dx, dy = self.offset(self.bullet_distance, angle)
            bullet = self.make_bullet(xo + dx, yo + dy, angle, RegularBullet)
            self.owner.bullets.append(bullet)

        dx, dy = self.offset(self.air_cannon_distance, body_angle + pi)
        xo, yo = self.owner.x + dx, self.owner.y + dy
        angle = calculate_angle(xo, yo, *cursor_pos)
        dx, dy = self.offset(self.bullet_distance, angle)
        self.owner.bullets.append(AirBullet(xo + dx, yo + dy, angle))

#_________________________________________________________________________________________________

class Gun55(AutoGun):
    def __init__(self, player, game):
        coords = (
            (HF(268), 0.215 * pi), (HF(268), -0.215 * pi),
            (HF(264), 0.8 * pi), (HF(264), -0.8 * pi),
        )
        super().__init__(player, game, 230, HF(102), HF(1.1), -5, 'BigBullet_1', 300, coords)
        self.bullet_distance = HF(57)

    def generate_bullets(self):
        cursor_pos = self.owner.get_mouse_pos()
        body_angle = self.owner.body.angle
        for k in (0, 1):
            xo, yo = self.gun_pos(body_angle + k * pi)
            angle = calculate_angle(xo, yo, *cursor_pos)
            dx, dy = self.offset(self.bullet_distance, angle)
            if k == 0:
                bullet = AirBullet(xo + dx, yo + dy, angle)
            else:
                bullet = self.make_bullet(xo + dx, yo + dy, angle, RegularBullet)
            self.owner.bullets.append(bullet)

#_________________________________________________________________________________________________

guns = {
    'Gun00': Gun00,
    'Gun10': Gun10,
    'Gun11': Gun11,
    'Gun12': Gun12,
    'Gun20': Gun20,
    'Gun21': Gun21,
    'Gun22': Gun21,
    'Gun23': Gun23,
    'Gun30': Gun30,
    'Gun31': Gun31,
    'Gun32': Gun32,
    'Gun33': Gun32,
    'Gun34': Gun34,
    'Gun35': Gun35,
    'Gun40': Gun40,
    'Gun41': Gun41,
    'Gun42': Gun42,
    'Gun43': Gun43,
    'Gun44': Gun44,
    'Gun45': Gun45,
    'Gun50': Gun50,
    'Gun51': Gun51,
    'Gun52': Gun00,
    'Gun53': Gun53,
    'Gun54': Gun54,
    'Gun55': Gun55
}


def get_gun(name, player, game):
    return guns[name](player, game)


__all__ = ["get_gun"]

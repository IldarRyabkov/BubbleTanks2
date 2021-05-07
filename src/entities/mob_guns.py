from math import pi, sin, cos
from random import uniform

from objects.gun import *
from objects.bullets import *
from data.bullets import *
from data.mob_guns import *
from utils import calculate_angle, HF


class GunBossHead(Gun):
    def __init__(self):
        super().__init__(*GUN_BOSS_HEAD_PARAMS)
        self.activated = False
        self.bullet_cooldown = 50
        self.turret_shot_time = self.bullet_cooldown
        self.turret_cooldown_time = 2000
        self.turret_time = self.turret_cooldown_time - 1000
        self.target_angle_vel = -3.75 * pi / self.turret_cooldown_time
        self.target_angle = uniform(0, 2*pi)
        self.target = [0, 0]

    def generate_bullets(self, x, y, target, gamma):
        xo, yo = x, y + HF(299)
        angle = calculate_angle(xo, yo, *target)
        coords = (xo + self.radius * cos(angle), yo - self.radius * sin(angle))

        return [RegularBullet(*coords, self.bul_dmg, self.bul_vel, angle, self.bul_body)]

    def get_target(self, x, y):
        return [x + HF(92) * cos(self.target_angle), y + HF(114) - HF(92) * sin(self.target_angle)]

    def append_bullet(self, x, y, bullets):
        self.target = self.get_target(x, y)
        bullets.append(RegularBullet(*self.target, -10, HF(1.0), self.target_angle, BULLETS["BigBullet_2"]))

    def add_bullets(self, x, y, target, bullets, gamma=0):
        if self.activated and self.turret_shot_time == self.bullet_cooldown:
            self.turret_shot_time = 0
            self.append_bullet(x, y, bullets)

        if self.time == self.cooldown_time:
            self.time = 0
            bullets.extend(self.generate_bullets(x, y, target, gamma))

    def update_time(self, dt):
        super().update_time(dt)

        if self.activated:
            self.target_angle += dt * self.target_angle_vel
            while self.target_angle >= 2 * pi:
                self.target_angle -= 2 * pi
            self.turret_shot_time = min([self.turret_shot_time + dt, self.bullet_cooldown])

        self.turret_time = min([self.turret_time + dt, self.turret_cooldown_time])
        if self.turret_time == self.turret_cooldown_time:
            self.turret_time = 0
            self.activated = not self.activated
            self.turret_shot_time = self.bullet_cooldown


class GunBossHand(Gun):
    def __init__(self):
        super().__init__(*GUN_BOSS_HAND_PARAMS)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        r = HF(23)
        pos_0 = (xo, yo)
        pos_1 = (xo + r * sin(angle), yo + r * cos(angle))
        pos_2 = (xo - r * sin(angle), yo - r * cos(angle))

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle, self.bul_body),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle, self.bul_body),
                RegularBullet(*pos_2, self.bul_dmg, self.bul_vel, angle, self.bul_body)]


class GunBossLeg(Gun):
    def __init__(self):
        super().__init__(*GUN_BOSS_LEG_PARAMS)
        self.missile_switch = 1

    def generate_bullets(self, x, y, target, gamma):
        angle = 0.61 * pi if self.missile_switch == 1 else 0.39 * pi
        xo = x + self.radius * cos(angle)
        yo = y - self.radius * sin(angle)

        return [HomingMissile(xo, yo, HF(28), self.bul_dmg, self.bul_vel, self.bul_body)]

    def add_bullets(self, x, y, target, bullets, gamma=0):
        if self.time == self.cooldown_time:
            self.time = 0
            self.missile_switch *= -1
            bullets.extend(self.generate_bullets(x, y, target, gamma))


class GunBenLaden(Gun):
    def __init__(self):
        super().__init__(*GUN_BENLADEN_PARAMS)

    @staticmethod
    def get_bullets_coords(x, y, gamma):
        r = HF(171)
        pos_0 = (x + r * cos(gamma + 0.25 * pi), y - r * sin(gamma + 0.25 * pi))
        pos_1 = (x + r * cos(gamma - 0.25 * pi), y - r * sin(gamma - 0.25 * pi))
        pos_2 = (x + r * cos(gamma + 0.75 * pi), y - r * sin(gamma + 0.75 * pi))
        pos_3 = (x + r * cos(gamma - 0.75 * pi), y - r * sin(gamma - 0.75 * pi))
        pos_4 = (x + r * cos(gamma + 0.5 * pi),  y - r * sin(gamma + 0.5 * pi))
        pos_5 = (x + r * cos(gamma - 0.5 * pi),  y - r * sin(gamma - 0.5 * pi))
        return [pos_0, pos_1, pos_2, pos_3, pos_4, pos_5]

    def generate_bullets(self, x, y, target, gamma):
        bullets = []
        coords = self.get_bullets_coords(x, y, gamma)
        for i in range(6):
            bullets.append(BombBullet(*coords[i], self.bul_body))
        return bullets


class GunBomberShooter(Gun):
    def __init__(self):
        super().__init__(*GUN_BOMBERSHOOTER_PARAMS)

        self.time_bomb = -2000
        self.cooldown_time_bomb = 3000

    def update_time(self, dt):
        super().update_time(dt)
        self.time_bomb = min([self.time_bomb + dt, self.cooldown_time_bomb])

    def append_small_bullet(self, x, y, bullets, target, gamma):
        r1, r2 = HF(43), HF(33)
        xo, yo = x + r1*cos(gamma), y - r1*sin(gamma)
        angle = calculate_angle(xo, yo, *target)
        xo, yo = xo + r2*cos(angle), yo - r2*sin(angle)
        bullets.append(RegularBullet(xo, yo, self.bul_dmg, self.bul_vel, angle, self.bul_body))

    @staticmethod
    def append_bomb_bullet(x, y, bullets, gamma):
        r = HF(64)
        xo, yo = x - r*cos(gamma), y + r*sin(gamma)
        bullets.append(BombBullet(xo, yo, BULLETS["BombBullet_2"]))

    def add_bullets(self, x, y, target, bullets, gamma=0):
        if self.time == self.cooldown_time:
            self.append_small_bullet(x, y, bullets, target, gamma)
            self.time = 0
        if self.time_bomb == self.cooldown_time_bomb:
            self.append_bomb_bullet(x, y, bullets, gamma)
            self.time_bomb = 0


class GunBeetle(Gun):
    def __init__(self):
        super().__init__(*GUN_BEETLE_PARAMS)
        self.gun_switch = -1

    def append_bullet_1(self, x, y, bullets, target, gamma):
        r1, r2 = HF(83), HF(36)
        pos = [x + r1 * cos(gamma), y - r1 * sin(gamma)]
        angle = calculate_angle(*pos, *target)
        pos[0] += r2 * cos(angle)
        pos[1] -= r2 * sin(angle)
        bullets.append(RegularBullet(*pos, self.bul_dmg, self.bul_vel, angle, self.bul_body))

    def append_bullet_2(self, x, y, bullets, target, gamma):
        r = HF(50)
        pos = [x - r * cos(gamma), y + r * sin(gamma)]
        angle = calculate_angle(*pos, *target)
        pos[0] += r * cos(angle)
        pos[1] -= r * sin(angle)
        bullets.append(RegularBullet(*pos, self.bul_dmg, self.bul_vel, angle, self.bul_body))

    def add_bullets(self, x, y, target, bullets, gamma=0):
        if self.time == self.cooldown_time:
            self.time = 0
            self.gun_switch *= -1
            if self.gun_switch == 1:
                self.append_bullet_1(x, y, bullets, target, gamma)
            else:
                self.append_bullet_2(x, y, bullets, target, gamma)


class GunSpreader(Gun):
    def __init__(self):
        super().__init__(*GUN_SPREADER_PARAMS)

    def add_bullets(self, x, y, target, bullets, gamma=0):
        if self.time == self.cooldown_time:
            self.time = 0
            r = HF(54)
            for i in range(10):
                angle = gamma + i * 0.2*pi
                xo, yo = x + r * cos(angle), y - r * sin(angle)
                bullets.append(RegularBullet(xo, yo, self.bul_dmg, self.bul_vel, angle, self.bul_body))


class GunSpider(Gun):
    def __init__(self):
        super().__init__(*GUN_SPIDER_PARAMS)

        self.small_gun_is_alive = True
        self.cooldown_time_2 = 2000
        self.time_2 = self.cooldown_time_2 - 2000

    @staticmethod
    def append_small_bullet(x, y, bullets, gamma, target):
        r1, r2 = HF(17), HF(38)
        x = x + r1 * cos(gamma)
        y = y - r1 * sin(gamma)
        angle = calculate_angle(x, y, *target)
        x += r2 * cos(angle)
        y -= r2 * sin(angle)
        bullets.append(RegularBullet(x, y, -2, HF(0.88), angle, BULLETS["SmallBullet_2"]))

    @staticmethod
    def append_big_bullet(x, y, bullets, gamma, target):
        r1, r2 = HF(100), HF(70)
        x = x - r1 * cos(gamma)
        y = y + r1 * sin(gamma)
        angle = calculate_angle(x, y, *target)
        x += r2 * cos(angle)
        y -= r2 * sin(angle)
        bullets.append(RegularBullet(x, y, -15, HF(0.88), angle, BULLETS["BigBullet_2"]))

    def add_bullets(self, x, y, target, bullets, gamma=0):
        if self.time == self.cooldown_time and self.small_gun_is_alive:
            self.time = 0
            self.append_small_bullet(x, y, bullets, gamma, target)
        if self.time_2 == self.cooldown_time_2:
            self.time_2 = 0
            self.append_big_bullet(x, y, bullets, gamma, target)

    def update_time(self, dt):
        super().update_time(dt)
        self.time_2 = min([self.time_2 + dt, self.cooldown_time_2])


class GunMachineGunner(Gun):
    def __init__(self):
        super().__init__(*GUN_MACHINEGUNNER_PARAMS)

        self.activated = False
        self.bullet_cooldown = 100
        self.shot_time = self.bullet_cooldown

    def append_bullet(self, x, y, bullets, target):
        angle = calculate_angle(x, y, *target)
        r = HF(33)
        xo = x + r * cos(angle)
        yo = y - r * sin(angle)
        bullets.append(RegularBullet(xo, yo, self.bul_dmg, self.bul_vel, angle, self.bul_body))

    def add_bullets(self, x, y, target, bullets, gamma=0):
        if self.activated and self.shot_time == self.bullet_cooldown:
            self.shot_time = 0
            self.append_bullet(x, y, bullets, target)

    def update_time(self, dt):
        super().update_time(dt)
        if self.activated:
            self.shot_time = min([self.shot_time + dt, self.bullet_cooldown])

        if self.time == self.cooldown_time:
            self.time = 0
            self.activated = not self.activated
            self.shot_time = self.bullet_cooldown


class GunTurret(Gun):
    def __init__(self):
        super().__init__(*GUN_TURRET_PARAMS)

        self.activated = False
        self.target_angle_vel = -0.8 * pi / self.cooldown_time
        self.target_angle = uniform(0, 2*pi)
        self.target = [0, 0]
        self.bullet_cooldown = 50
        self.shot_time = self.bullet_cooldown

    def get_target(self, x, y):
        r = HF(64)
        return [x + r * cos(self.target_angle), y - r * sin(self.target_angle)]

    def append_bullet(self, x, y, bullets):
        self.target = self.get_target(x, y)
        bullets.append(RegularBullet(*self.target, -4, HF(1.3), self.target_angle, self.bul_body))

    def add_bullets(self, x, y, target, bullets, gamma=0):
        if self.activated and self.shot_time == self.bullet_cooldown:
            self.shot_time = 0
            self.append_bullet(x, y, bullets)

    def update_time(self, dt):
        super().update_time(dt)
        if self.activated:
            self.target_angle += dt * self.target_angle_vel
            while self.target_angle >= 2 * pi:
                self.target_angle -= 2 * pi
            self.shot_time = min([self.shot_time + dt, self.bullet_cooldown])

        if self.time == self.cooldown_time:
            self.time = 0
            self.activated = not self.activated
            self.shot_time = self.bullet_cooldown


def get_gun(name):
    if name == 'GunPeaceful':      return GunPeaceful()
    if name == 'GunBossHead':      return GunBossHead()
    if name == 'GunBossHand':      return GunBossHand()
    if name == 'GunBossLeg':       return GunBossLeg()
    if name == 'GunBenLaden':      return GunBenLaden()
    if name == 'GunBomberShooter': return GunBomberShooter()
    if name == 'GunBeetle':        return GunBeetle()
    if name == 'GunSpreader':      return GunSpreader()
    if name == 'GunSpider':        return GunSpider()
    if name == 'GunMachineGunner': return GunMachineGunner()
    if name == 'GunTurret':        return GunTurret()
    if name == 'GunBeetleReserve': return GunSingle(*GUN_BEETLE_REVERSE_PARAMS)
    if name == 'GunBug':           return GunSingle(*GUN_BUG_PARAMS)
    if name == 'GunAnt':           return GunSingle(*GUN_ANT_PARAMS)
    if name == 'GunScarab':        return GunSingle(*GUN_SCARAB_PARAMS)
    if name == 'GunGull':          return GunSingle(*GUN_GULL_PARAMS)
    if name == 'GunCockroach':     return GunSingle(*GUN_COCKROACH_PARAMS)
    if name == 'GunTurtle':        return GunSingle(*GUN_TURTLE_PARAMS)
    if name == 'GunTurtleDMG':     return GunSingle(*GUN_TURTLE_DMG_PARAMS)
    if name == 'GunTerrorist':     return GunSingle(*GUN_TERRORIST_PARAMS)
    if name == 'GunBigEgg':        return GunSingle(*GUN_BIGEGG_PARAMS)


__all__ = ["get_gun"]

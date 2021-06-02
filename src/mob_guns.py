from math import pi
from random import uniform

from bullets import *
from utils import *
from constants import TRANSPORTATION_TIME
from base_gun import BaseGun


#_________________________________________________________________________________________________

class Gun(BaseGun):
    def __init__(self, *args):
        super().__init__(*args)
        self.time -= 1000 + TRANSPORTATION_TIME

    def update(self, dt):
        self.time += dt
        if self.time >= self.cooldown_time:
            self.time = 0
            self.generate_bullets()

    def generate_bullets(self):
        angle = calculate_angle(self.owner.x, self.owner.y, self.game.player.x, self.game.player.y)
        bullet = self.make_bullet(*self.gun_pos(angle), angle, self.bullet_type)
        self.game.room.bullets.append(bullet)

#_________________________________________________________________________________________________

class DisplacedGun(Gun):
    def __init__(self, mob, game, cooldown_time, distance, displacement, bullet_vel, bullet_dmg, bullet_name):
        super().__init__(mob, game, cooldown_time, distance,  bullet_vel, bullet_dmg, bullet_name)
        self.displacement = displacement

    def generate_bullets(self):
        xo, yo = self.gun_pos(self.owner.body.angle)
        angle = calculate_angle(xo, yo, self.game.player.x, self.game.player.y)
        dx, dy = self.offset(self.displacement, angle)
        bullet = self.make_bullet(xo + dx, yo + dy, angle, self.bullet_type)
        self.game.room.bullets.append(bullet)

#_________________________________________________________________________________________________

class Mortar(Gun):
    def __init__(self, mob, game, cooldown_time, distance):
        super().__init__(mob, game, cooldown_time, distance, 0, -10, 'BombBullet_2')

    def generate_bullets(self):
        mine = Mine(*self.gun_pos(self.owner.body.angle), self.bullet_body)
        self.game.room.mines.append(mine)

#_________________________________________________________________________________________________

class GunPeaceful(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 0, 0, 0, 0, "SmallBullet_2")

    def update(self, dt):
        pass

#_________________________________________________________________________________________________

class GunBigEgg(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 900, HF(92), HF(0.88), -4, 'SmallBullet_2')

#_________________________________________________________________________________________________

class GunTerrorist(Mortar):
    def __init__(self, mob, game):
        super().__init__(mob, game, 3000, 0)

# _________________________________________________________________________________________________

class GunTurtle(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 1700, HF(57), HF(0.88), 0, 'StickyBullet')

#_________________________________________________________________________________________________

class GunTurtleDMG(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 1700, HF(57), HF(0.88), -10, 'BigBullet_2')

#_________________________________________________________________________________________________

class GunGull(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 900, HF(14), HF(0.8), -2, 'SmallBullet_2')

#_________________________________________________________________________________________________

class GunBug(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 900, HF(17), HF(0.8), -2, 'SmallBullet_2')

#_________________________________________________________________________________________________

class GunBeetle(DisplacedGun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 450, -HF(50), HF(50), HF(0.88), -2, 'SmallScalingBullet_2')
        self.small_cannon = DisplacedGun(mob, game, 450, HF(83), HF(36), HF(0.88), -2, 'SmallScalingBullet_2')
        self.cannon_switch = 1

    def generate_bullets(self):
        if self.owner.health <= 6:
            self.small_cannon = None

        if self.cannon_switch == -1 and self.small_cannon is not None:
            self.small_cannon.generate_bullets()
        elif self.cannon_switch == 1:
            super().generate_bullets()

        self.cannon_switch *= -1

#_________________________________________________________________________________________________

class GunTurret(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 2000, HF(64), HF(1.3), -4, 'SmallBullet_2')
        self.activated = False
        self.angular_vel = -0.8 * pi / self.cooldown_time
        self.angle = uniform(0, 2*pi)
        self.shot_cooldown_time = 50
        self.shot_time = self.shot_cooldown_time

        dx, dy = self.offset(10, self.angle)
        self.turret_target = self.owner.x + dx, self.owner.y + dy

    def generate_bullets(self):
        xo, yo = self.gun_pos(self.angle)
        self.turret_target = xo, yo
        bullet = self.make_bullet(xo, yo, self.angle, self.bullet_type)
        self.game.room.bullets.append(bullet)

    def update(self, dt):
        self.time += dt
        if self.time >= self.cooldown_time:
            self.time = 0
            self.activated = not self.activated
            self.shot_time = self.shot_cooldown_time

        if self.activated:
            self.shot_time += dt
            self.angle += self.angular_vel * dt
            self.angle %= 2*pi

            if self.shot_time >= self.shot_cooldown_time:
                self.shot_time = 0
                self.generate_bullets()

#_________________________________________________________________________________________________


class GunMachineGunner(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 3000, HF(33), HF(1.3), -1, 'SmallBullet_2')
        self.activated = False
        self.shot_cooldown_time = 100
        self.shot_time = self.shot_cooldown_time

    def update(self, dt):
        self.time += dt
        if self.time >= self.cooldown_time:
            self.time = 0
            self.activated = not self.activated
            self.shot_time = self.shot_cooldown_time

        if self.activated:
            self.shot_time += dt
            if self.shot_time >= self.shot_cooldown_time:
                self.shot_time = 0
                self.generate_bullets()

#_________________________________________________________________________________________________

class GunSpider(DisplacedGun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 1700, -HF(100), HF(70), HF(0.88), -15, 'BigBullet_2')
        self.small_cannon = DisplacedGun(mob, game, 900, HF(17), HF(38), HF(0.88), -2, 'SmallScalingBullet_2')

    def update(self, dt):
        super().update(dt)
        if self.owner.health <= 70:
            self.small_cannon = None
        if self.small_cannon is not None:
            self.small_cannon.update(dt)

#_________________________________________________________________________________________________


class GunSpreader(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 1500, HF(54), HF(0.44), -2, 'SmallBullet_2')

    def generate_bullets(self):
        angle = self.owner.body.angle
        for _ in range(10):
            angle += 0.2 * pi
            bullet = self.make_bullet(*self.gun_pos(angle), angle, self.bullet_type)
            self.game.room.bullets.append(bullet)

#_________________________________________________________________________________________________

class GunBomberShooter(DisplacedGun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 900, HF(43), HF(33), HF(0.8), -2, 'SmallBullet_2')
        self.mortar = Mortar(mob, game, 3000, -HF(64))

    def update(self, dt):
        super().update(dt)
        self.mortar.update(dt)

#_________________________________________________________________________________________________

class GunBenLaden(Mortar):
    def __init__(self, mob, game):
        super().__init__(mob, game, 3000, HF(171))

    def generate_bullets(self):
        angle = self.owner.body.angle
        for k in (-3, -2, -1, 1, 2, 3):
            mine = Mine(*self.gun_pos(angle + k * 0.25 * pi), self.bullet_body)
            self.game.room.mines.append(mine)

# _________________________________________________________________________________________________

class GunBossLeg(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 1500, HF(228), HF(0.56), -10, 'HomingMissile_2')
        self.angle = 0.39 * pi

    def generate_bullets(self):
        xo, yo = self.gun_pos(self.angle)
        seeker = Seeker(xo, yo, self.angle, 0.05, HF(10), self.bullet_dmg, self.bullet_vel, self.bullet_body)
        seeker.target = self.game.player
        self.game.room.seekers.append(seeker)
        self.angle = pi - self.angle

#_________________________________________________________________________________________________

class GunBossHand(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 900, HF(64), HF(1.1), -3, 'SmallScalingBullet_2')

    def generate_bullets(self):
        angle = calculate_angle(self.owner.x, self.owner.y, self.game.player.x, self.game.player.y)
        xo, yo = self.gun_pos(angle)
        dy, dx = self.offset(HF(23), angle)
        for k in (-1, 0, 1):
            bullet = self.make_bullet(xo - k*dx, yo + k*dy, angle, self.bullet_type)
            self.game.room.bullets.append(bullet)

#_________________________________________________________________________________________________

class GunBossHead(Gun):
    def __init__(self, mob, game):
        super().__init__(mob, game, 2000, HF(113), HF(1.0), -10, "BigBullet_2")
        self.sticky_cannon = DisplacedGun(mob, game, 900, HF(298), HF(56), HF(0.88), 0, 'StickyBullet')
        self.activated = False
        self.angular_vel = -3.75 * pi / self.cooldown_time
        self.angle = uniform(0, 2*pi)
        self.shot_cooldown_time = 50
        self.shot_time = self.shot_cooldown_time

    @property
    def turret_target(self):
        xo, yo = self.gun_pos(self.owner.body.angle)
        dx, dy = self.offset(HF(88), self.angle)
        return xo + dx, yo + dy

    def generate_bullets(self):
        bullet = self.make_bullet(*self.turret_target, self.angle, self.bullet_type)
        self.game.room.bullets.append(bullet)

    def update(self, dt):
        self.sticky_cannon.update(dt)
        self.time += dt
        if self.time >= self.cooldown_time:
            self.time = 0
            self.activated = not self.activated
            self.shot_time = self.shot_cooldown_time

        if self.activated:
            self.shot_time += dt
            self.angle += self.angular_vel * dt
            self.angle %= 2*pi

            if self.shot_time >= self.shot_cooldown_time:
                self.shot_time = 0
                self.generate_bullets()

#_________________________________________________________________________________________________


guns = {
    "GunPeaceful": GunPeaceful,
    "GunBigEgg": GunBigEgg,
    "GunTerrorist": GunTerrorist,
    "GunTurtle": GunTurtle,
    "GunTurtleDMG": GunTurtleDMG,
    "GunCockroach": GunGull,
    "GunGull": GunGull,
    "GunScarab": GunGull,
    "GunAnt": GunGull,
    "GunBug": GunBug,
    "GunBeetle": GunBeetle,
    "GunTurret": GunTurret,
    "GunMachineGunner": GunMachineGunner,
    "GunSpider": GunSpider,
    "GunSpreader": GunSpreader,
    "GunBomberShooter": GunBomberShooter,
    "GunBenLaden": GunBenLaden,
    "GunBossLeg": GunBossLeg,
    "GunBossHand": GunBossHand,
    "GunBossHead": GunBossHead
}


def get_gun(name, mob, game):
    return guns[name](mob, game)


__all__ = ["get_gun"]

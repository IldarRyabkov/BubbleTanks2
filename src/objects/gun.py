from math import sin, cos, hypot

from data.bullets import BULLETS, SMALL_BUL_BODY_1
from data.config import SCR_H
from utils import calculate_angle
from objects.bullets import RegularBullet


class Gun:
    """ A parent class for all gun classes. """
    def __init__(self,
                 radius: int,
                 bul_vel: float,
                 bul_dmg: int,
                 bullet_name: str,
                 cooldown_time: int,
                 time_delay: int):
        self.radius = radius
        self.bul_vel = bul_vel
        self.bul_dmg = bul_dmg
        self.bul_body = BULLETS[bullet_name]
        self.cooldown_time = cooldown_time
        self.time = cooldown_time + time_delay
        self.automatic = False
        self.is_aiming = True
        self.shooting_homing_bullets = False

    def get_reference_point(self, x, y, angle) -> tuple:
        xo = x + self.radius * cos(angle)
        yo = y - self.radius * sin(angle)
        return xo, yo

    def generate_bullets(self, x, y, target, gamma) -> list:
        """ Returns list of generated bullets. """
        return list()

    def append_bullets(self, x, y, target, bullets, gamma=0):
        """ Appends new bullets to the given list of bullets. """
        if self.time == self.cooldown_time:
            self.time = 0
            bullets.extend(self.generate_bullets(x, y, target, gamma))

    def update_time(self, dt):
        """
        Update the time counter. time = cooldown_time means
        that gun is recharged and ready to shoot.

        """
        self.time = min([self.time + dt, self.cooldown_time])


class GunSingle(Gun):
    """ A gun that fires one regular bullet at a time. """
    def __init__(self, radius, bul_vel, bul_dmg, bul_type, cooldown_time, time):
        super().__init__(radius, bul_vel, bul_dmg, bul_type, cooldown_time, time)

    def generate_bullets(self, x, y, target, gamma) -> list:
        angle = calculate_angle(x, y, *target)
        coords = self.get_reference_point(x, y, angle)

        return [RegularBullet(*coords, self.bul_dmg, self.bul_vel, angle, self.bul_body)]


class GunAutomatic(GunSingle):
    """ A gun that can shoot bullets automatically. """
    def __init__(self, radius, bul_vel, bul_dmg, bul_type,
                 cooldown_time, time, cooldown_time_auto, coords):

        super().__init__(radius, bul_vel, bul_dmg, bul_type, cooldown_time, time)

        self.automatic = True
        self.time_auto = cooldown_time_auto
        self.cooldown_time_auto = cooldown_time_auto
        self.auto_bullets_coords = coords

    def generate_bullets_auto(self, x, y, mob, gamma) -> list:
        bullets = list()
        for radius, angle in self.auto_bullets_coords:
            pos = (x + radius * cos(gamma + angle), y - radius * sin(gamma + angle))
            if mob.is_paralysed or mob.is_frozen:
                target = mob.x, mob.y
            else:
                dt = hypot(pos[0] - mob.x, pos[1] - mob.y) / 2.4
                target = mob.trajectory(mob.time + dt / 1000 * mob.w)
            bullet_angle = calculate_angle(*pos, *target)
            bullets.append(RegularBullet(*pos, -1, 2.4, bullet_angle, SMALL_BUL_BODY_1))
        return bullets

    def append_bullets_auto(self, x, y, mobs, bullets, gamma=0):
        if self.time_auto == self.cooldown_time_auto:
            self.time_auto = 0
            mob = -1
            distance = 9001
            for i in range(len(mobs)):
                d = hypot(x - mobs[i].x, y - mobs[i].y)
                if d < distance:
                    distance = d
                    mob = i
            bullets.extend(self.generate_bullets_auto(x, y, mobs[mob], gamma))

    def update_time(self, dt):
        super().update_time(dt)
        self.time_auto = min([self.time_auto + dt, self.cooldown_time_auto])


class GunPeaceful:
    """ A gun that shoots no bullets. """
    def __init__(self):
        self.shooting_homing_bullets = False

    def append_bullets(self, x, y, target, bullets, gamma=0):
        pass

    def update_time(self, dt):
        pass

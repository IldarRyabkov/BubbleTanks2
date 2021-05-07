from math import sin, cos, hypot
from numpy import array

from data.bullets import *
from utils import calculate_angle, HF
from objects.bullets import RegularBullet


class Gun:
    """ A parent class for all gun classes. """
    def __init__(self,
                 radius: float,
                 bul_vel: float,
                 bul_dmg: int,
                 bullet_name: str,
                 cooldown_time: int,
                 delay_time: int):
        self.radius = radius
        self.bul_vel = bul_vel
        self.bul_dmg = bul_dmg
        self.bul_body = BULLETS[bullet_name]
        self.cooldown_time = cooldown_time
        self.time = cooldown_time + delay_time

    def get_reference_point(self, x, y, angle) -> tuple:
        """ Returns the coordinates of the point relative
        to which the starting positions of the bullets will
        be calculated, depending on the type of gun.
        """
        xo = x + self.radius * cos(angle)
        yo = y - self.radius * sin(angle)
        return xo, yo

    def generate_bullets(self, x, y, target, gamma) -> list:
        """ Returns the list of generated bullets. """
        return []

    def add_bullets(self, x, y, target, bullets, gamma=0):
        """ Adds new bullets to the given list of bullets. """
        if self.time == self.cooldown_time:
            self.time = 0
            bullets.extend(self.generate_bullets(x, y, target, gamma))

    def update_time(self, dt):
        """
        Updates the time counter. self.time == self.cooldown_time means
        that gun is recharged and ready to shoot.
        """
        self.time = min([self.time + dt, self.cooldown_time])


class GunSingle(Gun):
    """ A gun that fires one regular bullet at a time. """
    def __init__(self,
                 radius,
                 bul_vel,
                 bul_dmg,
                 bul_type,
                 cooldown_time,
                 delay_time):

        super().__init__(radius,
                         bul_vel,
                         bul_dmg,
                         bul_type,
                         cooldown_time,
                         delay_time)

    def generate_bullets(self, x, y, target, gamma) -> list:
        angle = calculate_angle(x, y, *target)
        coords = self.get_reference_point(x, y, angle)
        return [RegularBullet(*coords, self.bul_dmg, self.bul_vel, angle, self.bul_body)]


class GunAutomatic(GunSingle):
    """ A gun that shoots bullets at moving targets automatically. """
    def __init__(self,
                 radius,
                 bul_vel,
                 bul_dmg,
                 bul_type,
                 cooldown_time,
                 delay_time,
                 cooldown_time_auto,
                 coords):

        super().__init__(radius,
                         bul_vel,
                         bul_dmg,
                         bul_type,
                         cooldown_time,
                         delay_time)
        self.time_auto = cooldown_time_auto
        self.cooldown_time_auto = cooldown_time_auto
        self.auto_bullets_coords = coords
        self.AUTO_BULLET_VEL = HF(2.4)

    def generate_bullets_auto(self, x, y, mob, gamma) -> list:
        """ Returns the list of bullets which will linearly move to the given mob. """
        bullets = []

        for radius, angle in self.auto_bullets_coords:

            # the starting point of the bullet's movement
            start_pos = array([x + radius * cos(gamma + angle),
                               y - radius * sin(gamma + angle)])

            # find the exact position of the target in order to
            # calculate the angle of movement of the bullet
            if mob.is_paralysed or mob.is_frozen:
                target = mob.pos
            else:
                # if the target is moving we must take into account
                # the displacement of the target, which will occur
                # while the bullet is moving towards it.
                dt = hypot(*(start_pos - mob.pos)) / self.AUTO_BULLET_VEL
                target = mob.trajectory(mob.pos_0, mob.polar_angle + dt * mob.angular_vel)

            # angle of movement of the bullet
            bullet_angle = calculate_angle(*start_pos, *target)

            bullets.append(RegularBullet(*start_pos, -1, self.AUTO_BULLET_VEL,
                                         bullet_angle, BULLETS["SmallBullet_1"]))
        return bullets

    def add_bullets_auto(self, pos, mobs, bullets, gamma=0):
        """ Adds bullets that automatically hit the nearest target
        to the given list of bullets.
        """
        if self.time_auto == self.cooldown_time_auto:
            self.time_auto = 0
            mob = min(mobs, key=lambda m: hypot(*(pos - m.pos)))
            bullets.extend(self.generate_bullets_auto(*pos, mob, gamma))

    def update_time(self, dt):
        super().update_time(dt)
        self.time_auto = min([self.time_auto + dt, self.cooldown_time_auto])


class GunPeaceful(Gun):
    """ A gun that shoots no bullets. """
    def __init__(self):
        super().__init__(0, 0.0, 0, 'SmallBullet_2', 0, 0)

    def add_bullets(self, x, y, target, bullets, gamma=0):
        pass

    def update_time(self, dt):
        pass


__all__ = [

    "Gun",
    "GunSingle",
    "GunAutomatic",
    "GunPeaceful"

]

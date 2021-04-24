from math import pi, sin, cos

from objects.gun import Gun, GunSingle, GunAutomatic
from utils import calculate_angle
from objects.bullets import RegularBullet
from objects.bullets import EllipticBullet
from objects.body import Body
from data.bullets import SMALL_BUL_BODY_1, BIG_BUL_BODY_1, STICKY_BUL_BODY


class Gun00(GunSingle):
    def __init__(self):
        super().__init__(26, 1.6, -1, 'SmallBullet_1', 300, 0)


class Gun10(GunSingle):
    def __init__(self):
        super().__init__(26, 1.6, -1, 'SmallBullet_1', 75, 0)


class Gun11(Gun):
    def __init__(self):
        super().__init__(26, 1.6, -1, 'SmallBullet_1', 150, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        pos_0 = xo + 10 * sin(angle), yo + 10 * cos(angle)
        pos_1 = xo - 10 * sin(angle), yo - 10 * cos(angle)

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle, Body(self.bul_body)),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle, Body(self.bul_body))]


class Gun12(GunSingle):
    def __init__(self):
        super().__init__(26, 1.2, -5, 'BigBullet_1', 300, 0)


class Gun20(Gun):
    def __init__(self):
        super().__init__(26, 1.6, -1, 'SmallBullet_1', 125, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        pos_0 = (xo, yo)
        pos_1 = (xo + 23 * sin(angle - 0.17*pi), yo + 23 * cos(angle - 0.17*pi))
        pos_2 = (xo - 23 * sin(angle + 0.17*pi), yo - 23 * cos(angle + 0.17*pi))

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle,             Body(self.bul_body)),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle - 0.17 * pi, Body(self.bul_body)),
                RegularBullet(*pos_2, self.bul_dmg, self.bul_vel, angle + 0.17 * pi, Body(self.bul_body))]


class Gun21(Gun):
    def __init__(self):
        super().__init__(72, 1.6, -1, 'SmallBullet_1', 150, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        pos_0 = (xo, yo)
        pos_1 = (xo + 22 * sin(angle), yo + 22 * cos(angle))
        pos_2 = (xo - 22 * sin(angle), yo - 22 * cos(angle))

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle, Body(self.bul_body)),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle, Body(self.bul_body)),
                RegularBullet(*pos_2, self.bul_dmg, self.bul_vel, angle, Body(self.bul_body))]


class Gun22(Gun21):
    def __init__(self):
        super().__init__()


class Gun23(Gun):
    def __init__(self):
        super().__init__(72, 1.6, -1, 'SmallBullet_1', 150, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        sina, cosa = sin(angle), cos(angle)
        coords = [(xo, yo),
                  (xo + 22*sina,          yo + 22*cosa),
                  (xo - 22*sina,          yo - 22*cosa),
                  (xo + 45*sina - 6*cosa, yo + 45*cosa + 6*sina),
                  (xo - 45*sina - 6*cosa, yo - 45*cosa + 6*sina)]

        bullets = []
        for pos in coords:
            bullets.append(RegularBullet(*pos, self.bul_dmg, self.bul_vel, angle, Body(self.bul_body)))
        return bullets


class Gun30(GunSingle):
    def __init__(self):
        super().__init__(16, 2.1, -10, 'SniperBullet', 350, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        return [EllipticBullet(xo, yo, self.bul_dmg, self.bul_vel, angle, self.bul_body)]


class Gun31(GunSingle):
    def __init__(self):
        super().__init__(32, 1.6, -2, 'SmallBullet_1', 75, 0)


class Gun32(Gun):
    def __init__(self):
        super().__init__(56, 1.6, -1, 'SmallBullet_1', 150, 0)

    @staticmethod
    def get_bullets_angles(angle):
        return angle, angle - 0.075*pi, angle + 0.075*pi, angle - 0.15*pi, angle + 0.15*pi

    @staticmethod
    def get_bullets_coords(xo, yo, angles):
        return [(xo, yo),
                (xo + 12 * sin(angles[1]), yo + 12 * cos(angles[1])),
                (xo - 12 * sin(angles[2]), yo - 12 * cos(angles[2])),
                (xo + 23 * sin(angles[3]),  yo + 23 * cos(angles[3])),
                (xo - 23 * sin(angles[4]),  yo - 23 * cos(angles[4]))]

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        angles = self.get_bullets_angles(angle)
        coords = self.get_bullets_coords(xo, yo, angles)

        bullets = []
        for i in range(5):
            bullets.append(RegularBullet(*coords[i], self.bul_dmg, self.bul_vel, angles[i], Body(self.bul_body)))
        return bullets


class Gun33(Gun32):
    def __init__(self):
        super().__init__()


class Gun34(Gun):
    def __init__(self):
        super().__init__(0, 1.1, -5, 'BigBullet_1', 300, 0)

    def generate_bullets(self, x, y, target, gamma):
        xo, yo = x + 128 * cos(gamma + 0.76*pi), y - 128 * sin(gamma + 0.76*pi)
        angle_0 = calculate_angle(xo, yo, *target)
        pos_0 = (xo + 64 * cos(angle_0), yo - 64 * sin(angle_0))

        xo, yo = x + 128 * cos(gamma - 0.76*pi), y - 128 * sin(gamma - 0.76*pi)
        angle_1 = calculate_angle(xo, yo, *target)
        pos_1 = (xo + 64 * cos(angle_1), yo - 64 * sin(angle_1))

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle_0, Body(self.bul_body)),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle_1, Body(self.bul_body))]


class Gun35(GunAutomatic):
    def __init__(self):
        coords = ((140, 0.25 * pi), (140, -0.25 * pi))
        super().__init__(48, 1.2, -5, 'BigBullet_1', 200, 0, 200, coords)


class Gun40(Gun):
    def __init__(self):
        super().__init__(32, 2.1, -15, 'SniperBullet', 425, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        return [EllipticBullet(xo, yo, self.bul_dmg, self.bul_vel, angle, self.bul_body)]


class Gun41(Gun11):
    def __init__(self):
        super().__init__()
        self.cooldown_time = 80


class Gun42(Gun):
    def __init__(self):
        super().__init__(16, 1.6, -1, 'SmallBullet_1', 200, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        pos_0 = (xo, yo)
        pos_1 = (xo + 85 * cos(angle + 0.48*pi), yo - 85 * sin(angle + 0.48*pi))
        pos_2 = (xo + 85 * cos(angle - 0.48*pi), yo - 85 * sin(angle - 0.48*pi))

        return [(RegularBullet(*pos_0, -5, 1.2, angle, Body(BIG_BUL_BODY_1))),
                (RegularBullet(*pos_1, -1, 1.6,  angle, Body(SMALL_BUL_BODY_1))),
                (RegularBullet(*pos_2, -1, 1.6,  angle, Body(SMALL_BUL_BODY_1)))]


class Gun43(Gun):
    def __init__(self):
        super().__init__(32, 1.3, -2, 'MediumBullet_1', 150, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        pos_0 = (x + 32 * cos(angle + 0.74*pi), y - 32 * sin(angle + 0.74*pi))
        pos_1 = (x + 32 * cos(angle - 0.74*pi), y - 32 * sin(angle - 0.74*pi))

        return [(RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle, Body(self.bul_body))),
                (RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle, Body(self.bul_body)))]


class Gun44(GunAutomatic):
    def __init__(self):
        coords = ((154, 0.25 * pi), (154, -0.25 * pi))
        super().__init__(48, 1.1, -5, 'BigBullet_1', 300, 0, 300, coords)

    def generate_bullets(self, x, y, target, gamma):
        xo, yo = x + 144 * cos(gamma + 0.75*pi), y - 144 * sin(gamma + 0.75*pi)
        angle_0 = calculate_angle(xo, yo, *target)
        pos_0 = (xo + 64 * cos(angle_0), yo - 64 * sin(angle_0))

        xo, yo = x + 144 * cos(gamma - 0.75*pi), y - 144 * sin(gamma - 0.75*pi)
        angle_1 = calculate_angle(xo, yo, *target)
        pos_1 = (xo + 64 * cos(angle_1), yo - 64 * sin(angle_1))

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle_0, Body(self.bul_body)),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle_1, Body(self.bul_body))]


class Gun45(GunAutomatic):
    def __init__(self):
        coords = ((198, 0.3 * pi), (198, -0.3 * pi), (198, 0))
        super().__init__(0, 1.1, -5, 'BigBullet_1', 300, 0, 300, coords)

    def generate_bullets(self, x, y, target, gamma):
        bullets = list()
        for angle in [gamma + 0.78*pi, gamma - 0.78*pi]:
            xo, yo = x + 160 * cos(angle), y - 160 * sin(angle)
            bullet_angle = calculate_angle(xo, yo, *target)
            bullet_pos = (xo + 64 * cos(bullet_angle), yo - 64 * sin(bullet_angle))
            bullets.append(RegularBullet(*bullet_pos, self.bul_dmg, self.bul_vel,
                                         bullet_angle, Body(self.bul_body)))
        return bullets


class Gun50(Gun40):
    def __init__(self):
        super().__init__()
        self.cooldown_time = 500
        self.radius = 64
        self.bul_dmg = -25


class Gun51(Gun21):
    def __init__(self):
        super().__init__()
        self.cooldown_time = 100
        self.radius = 23


class Gun52(Gun00):
    def __init__(self):
        super().__init__()


class Gun53(Gun00):
    def __init__(self):
        super().__init__()


class Gun54(GunAutomatic):
    def __init__(self):
        coords = ((243, 0.09 * pi), (243, -0.09 * pi),
                  (218, 0.29 * pi), (218, -0.29 * pi),
                  (218, 0.79 * pi), (218, -0.79 * pi))
        super().__init__(0, 1.1, -5, 'BigBullet_1', 300, 0, 300, coords)
        self.bullets_coords = ((192, 0.55 * pi), (192, -0.55 * pi), (200, pi))

    def generate_bullets(self, x, y, target, gamma):
        bullets = list()
        for radius, angle in self.bullets_coords:
            xo = x + radius * cos(gamma + angle)
            yo = y - radius * sin(gamma + angle)
            bullet_angle = calculate_angle(xo, yo, *target)
            bullet_pos = (xo + 64 * cos(bullet_angle), yo - 64 * sin(bullet_angle))
            bul_body = self.bul_body if radius != 200 else STICKY_BUL_BODY
            bul_dmg = self.bul_dmg if radius != 200 else 0
            bullets.append(RegularBullet(*bullet_pos, bul_dmg, self.bul_vel,
                                         bullet_angle, Body(bul_body)))
        return bullets


class Gun55(Gun00):
    def __init__(self):
        super().__init__()


def get_gun(name):
    if name == 'Gun00': return Gun00()
    if name == 'Gun10': return Gun10()
    if name == 'Gun11': return Gun11()
    if name == 'Gun12': return Gun12()
    if name == 'Gun20': return Gun20()
    if name == 'Gun21': return Gun21()
    if name == 'Gun22': return Gun22()
    if name == 'Gun23': return Gun23()
    if name == 'Gun30': return Gun30()
    if name == 'Gun31': return Gun31()
    if name == 'Gun32': return Gun32()
    if name == 'Gun33': return Gun33()
    if name == 'Gun34': return Gun34()
    if name == 'Gun35': return Gun35()
    if name == 'Gun40': return Gun40()
    if name == 'Gun41': return Gun41()
    if name == 'Gun42': return Gun42()
    if name == 'Gun43': return Gun43()
    if name == 'Gun44': return Gun44()
    if name == 'Gun45': return Gun45()
    if name == 'Gun50': return Gun50()
    if name == 'Gun51': return Gun51()
    if name == 'Gun52': return Gun52()
    if name == 'Gun53': return Gun53()
    if name == 'Gun54': return Gun54()
    if name == 'Gun55': return Gun55()


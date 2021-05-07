from math import pi, sin, cos

from objects.bullets import *
from objects.gun import *
from data.bullets import BULLETS
from utils import calculate_angle, HF


class Gun00(GunSingle):
    def __init__(self):
        super().__init__(HF(23), HF(1.6), -1, 'SmallBullet_1', 300, 0)


class Gun10(GunSingle):
    def __init__(self):
        super().__init__(HF(23), HF(1.6), -1, 'SmallBullet_1', 100, 0)


class Gun11(Gun):
    def __init__(self):
        super().__init__(HF(23), HF(1.6), -1, 'SmallBullet_1', 175, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        r = HF(9)
        pos_0 = xo + r * sin(angle), yo + r * cos(angle)
        pos_1 = xo - r * sin(angle), yo - r * cos(angle)

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle, self.bul_body),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle, self.bul_body)]


class Gun12(GunSingle):
    def __init__(self):
        super().__init__(HF(23), HF(1.2), -5, 'BigBullet_1', 300, 0)


class Gun20(Gun):
    def __init__(self):
        super().__init__(HF(23), HF(1.6), -1, 'SmallBullet_1', 125, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        pos_0 = (xo, yo)
        r = HF(21)
        pos_1 = (xo + r * sin(angle - 0.17*pi), yo + r * cos(angle - 0.17*pi))
        pos_2 = (xo - r * sin(angle + 0.17*pi), yo - r * cos(angle + 0.17*pi))

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle,             self.bul_body),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle - 0.17 * pi, self.bul_body),
                RegularBullet(*pos_2, self.bul_dmg, self.bul_vel, angle + 0.17 * pi, self.bul_body)]


class Gun21(Gun):
    def __init__(self):
        super().__init__(HF(64), HF(1.6), -1, 'SmallBullet_1', 150, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        pos_0 = (xo, yo)
        r = HF(20)
        pos_1 = (xo + r * sin(angle), yo + r * cos(angle))
        pos_2 = (xo - r * sin(angle), yo - r * cos(angle))

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle, self.bul_body),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle, self.bul_body),
                RegularBullet(*pos_2, self.bul_dmg, self.bul_vel, angle, self.bul_body)]


class Gun22(Gun21):
    def __init__(self):
        super().__init__()


class Gun23(Gun):
    def __init__(self):
        super().__init__(HF(64), HF(1.6), -1, 'SmallBullet_1', 150, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        sina, cosa = sin(angle), cos(angle)
        r1, r2, r3 = HF(20), HF(40), HF(5)
        coords = [(xo, yo),
                  (xo + r1*sina,           yo + r1*cosa),
                  (xo - r1*sina,           yo - r1*cosa),
                  (xo + r2*sina - r3*cosa, yo + r2*cosa + r3*sina),
                  (xo - r2*sina - r3*cosa, yo - r2*cosa + r3*sina)]

        bullets = []
        for pos in coords:
            bullets.append(RegularBullet(*pos, self.bul_dmg, self.bul_vel, angle, self.bul_body))
        return bullets


class Gun30(GunSingle):
    def __init__(self):
        super().__init__(HF(14), HF(2.1), -10, 'SniperBullet', 350, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        return [DrillingBullet(xo, yo, self.bul_dmg, self.bul_vel, angle, self.bul_body)]


class Gun31(GunSingle):
    def __init__(self):
        super().__init__(HF(28), HF(1.6), -2, 'SmallBullet_1', 75, 0)


class Gun32(Gun):
    def __init__(self):
        super().__init__(HF(50), HF(1.6), -1, 'SmallBullet_1', 150, 0)

    @staticmethod
    def get_bullets_angles(angle):
        return angle, angle - 0.075*pi, angle + 0.075*pi, angle - 0.15*pi, angle + 0.15*pi

    @staticmethod
    def get_bullets_coords(xo, yo, angles):
        r1, r2 = HF(11), HF(21)
        return [(xo, yo),
                (xo + r1 * sin(angles[1]), yo + r1 * cos(angles[1])),
                (xo - r1 * sin(angles[2]), yo - r1 * cos(angles[2])),
                (xo + r2 * sin(angles[3]), yo + r2 * cos(angles[3])),
                (xo - r2 * sin(angles[4]), yo - r2 * cos(angles[4]))]

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        angles = self.get_bullets_angles(angle)
        coords = self.get_bullets_coords(xo, yo, angles)

        bullets = []
        for i in range(5):
            bullets.append(RegularBullet(*coords[i], self.bul_dmg, self.bul_vel, angles[i], self.bul_body))
        return bullets


class Gun33(Gun32):
    def __init__(self):
        super().__init__()


class Gun34(Gun):
    def __init__(self):
        super().__init__(0, HF(1.1), -5, 'BigBullet_1', 300, 0)

    def generate_bullets(self, x, y, target, gamma):
        r1, r2 = HF(114), HF(57)
        xo, yo = x + r1 * cos(gamma + 0.76*pi), y - r1 * sin(gamma + 0.76*pi)
        angle_0 = calculate_angle(xo, yo, *target)
        pos_0 = (xo + r2 * cos(angle_0), yo - r2 * sin(angle_0))

        xo, yo = x + r1 * cos(gamma - 0.76*pi), y - r1 * sin(gamma - 0.76*pi)
        angle_1 = calculate_angle(xo, yo, *target)
        pos_1 = (xo + r2 * cos(angle_1), yo - r2 * sin(angle_1))

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle_0, self.bul_body),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle_1, self.bul_body)]


class Gun35(GunAutomatic):
    def __init__(self):
        coords = ((HF(124), 0.25 * pi), (HF(124), -0.25 * pi))
        super().__init__(HF(43), HF(1.2), -5, 'BigBullet_1', 200, 0, 200, coords)


class Gun40(Gun):
    def __init__(self):
        super().__init__(HF(28), HF(2.1), -15, 'SniperBullet', 425, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        return [DrillingBullet(xo, yo, self.bul_dmg, self.bul_vel, angle, self.bul_body)]


class Gun41(Gun11):
    def __init__(self):
        super().__init__()
        self.cooldown_time = 80


class Gun42(Gun):
    def __init__(self):
        super().__init__(HF(14), HF(1.6), -1, 'SmallBullet_1', 200, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        xo, yo = self.get_reference_point(x, y, angle)
        r = HF(76)
        pos_0 = (xo, yo)
        pos_1 = (xo + r * cos(angle + 0.48*pi), yo - r * sin(angle + 0.48*pi))
        pos_2 = (xo + r * cos(angle - 0.48*pi), yo - r * sin(angle - 0.48*pi))

        return [(RegularBullet(*pos_0, -5, HF(1.2), angle, BULLETS["BigBullet_1"])),
                (RegularBullet(*pos_1, -1, HF(1.6), angle, BULLETS["SmallBullet_1"])),
                (RegularBullet(*pos_2, -1, HF(1.6), angle, BULLETS["SmallBullet_1"]))]


class Gun43(Gun):
    def __init__(self):
        super().__init__(HF(28), HF(1.3), -2, 'MediumBullet_1', 150, 0)

    def generate_bullets(self, x, y, target, gamma):
        angle = calculate_angle(x, y, *target)
        pos_0 = (x + self.radius * cos(angle + 0.74*pi), y - self.radius * sin(angle + 0.74*pi))
        pos_1 = (x + self.radius * cos(angle - 0.74*pi), y - self.radius * sin(angle - 0.74*pi))

        return [(RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle, self.bul_body)),
                (RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle, self.bul_body))]


class Gun44(GunAutomatic):
    def __init__(self):
        coords = ((HF(137), 0.25 * pi), (HF(137), -0.25 * pi))
        super().__init__(HF(43), HF(1.1), -5, 'BigBullet_1', 300, 0, 200, coords)

    def generate_bullets(self, x, y, target, gamma):
        r1, r2 = HF(128), HF(57)
        xo, yo = x + r1 * cos(gamma + 0.75*pi), y - r1 * sin(gamma + 0.75*pi)
        angle_0 = calculate_angle(xo, yo, *target)
        pos_0 = (xo + r2 * cos(angle_0), yo - r2 * sin(angle_0))

        xo, yo = x + r1 * cos(gamma - 0.75*pi), y - r1 * sin(gamma - 0.75*pi)
        angle_1 = calculate_angle(xo, yo, *target)
        pos_1 = (xo + r2 * cos(angle_1), yo - r2 * sin(angle_1))

        return [RegularBullet(*pos_0, self.bul_dmg, self.bul_vel, angle_0, self.bul_body),
                RegularBullet(*pos_1, self.bul_dmg, self.bul_vel, angle_1, self.bul_body)]


class Gun45(GunAutomatic):
    def __init__(self):
        coords = ((HF(176), 0.3 * pi), (HF(176), -0.3 * pi), (HF(176), 0))
        super().__init__(0, HF(1.1), -5, 'BigBullet_1', 300, 0, 300, coords)

    def generate_bullets(self, x, y, target, gamma):
        bullets = list()
        r1, r2 = HF(142), HF(57)
        for angle in [gamma + 0.78*pi, gamma - 0.78*pi]:
            xo, yo = x + r1 * cos(angle), y - r1 * sin(angle)
            bullet_angle = calculate_angle(xo, yo, *target)
            bullet_pos = (xo + r2 * cos(bullet_angle), yo - r2 * sin(bullet_angle))
            bullets.append(RegularBullet(*bullet_pos, self.bul_dmg, self.bul_vel,
                                         bullet_angle, self.bul_body))
        return bullets


class Gun50(Gun40):
    def __init__(self):
        super().__init__()
        self.cooldown_time = 500
        self.radius = HF(57)
        self.bul_dmg = -15


class Gun51(Gun21):
    def __init__(self):
        super().__init__()
        self.cooldown_time = 100
        self.radius = HF(21)


class Gun52(Gun00):
    def __init__(self):
        super().__init__()


class Gun53(Gun00):
    def __init__(self):
        super().__init__()


class Gun54(GunAutomatic):
    def __init__(self):
        coords = ((HF(216), 0.09 * pi), (HF(216), -0.09 * pi),
                  (HF(194), 0.29 * pi), (HF(194), -0.29 * pi),
                  (HF(194), 0.79 * pi), (HF(194), -0.79 * pi))
        super().__init__(0, HF(1.1), -5, 'BigBullet_1', 200, 0, 200, coords)
        self.bullets_coords = ((HF(171), 0.55 * pi), (HF(171), -0.55 * pi), (HF(178), pi))

    def generate_bullets(self, x, y, target, gamma):
        bullets = list()
        r1, r2 = HF(57), HF(178)
        for radius, angle in self.bullets_coords:
            xo = x + radius * cos(gamma + angle)
            yo = y - radius * sin(gamma + angle)
            bullet_angle = calculate_angle(xo, yo, *target)
            bullet_pos = (xo + r1 * cos(bullet_angle), yo - r1 * sin(bullet_angle))
            bul_body = self.bul_body if radius != r2 else BULLETS["StickyBullet"]
            bul_dmg = self.bul_dmg if radius != r2 else 0
            bullets.append(RegularBullet(*bullet_pos, bul_dmg, self.bul_vel,
                                         bullet_angle, bul_body))
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


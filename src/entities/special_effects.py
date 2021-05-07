import pygame as pg
from random import uniform
from math import pi, sin, cos

from objects.circle import Circle
from data.config import *
from data.colors import *
from data.paths import PARALYZING_EXPLOSION, POWERFUL_EXPLOSION, TELEPORTATION
from utils import H, HF


class Line:
    def __init__(self, x, y, size, alpha, duration):
        if size == 'SmallHitLines':
            self.widths = [H(3), H(5), H(6)]
            length = uniform(HF(59), HF(251))
        else:
            self.widths = [H(8), H(11), H(14)]
            length = uniform(HF(216), HF(616))

        radius = HF(32)
        cosa, sina = cos(alpha), sin(alpha)
        self.X0 = x + radius * cosa
        self.Y0 = y - radius * sina
        self.X1, self.Y1 = self.X0, self.Y0
        self.vel_x = length * cosa / duration
        self.vel_y = -length * sina / duration

    def update(self, dt):
        self.X1 += self.vel_x * dt
        self.Y1 += self.vel_y * dt

    def draw(self, surface, dx, dy):
        pg.draw.line(surface, HIT_COLOR,
                     (self.X0 - dx, self.Y0 - dy),
                     (self.X1 - dx, self.Y1 - dy), self.widths[0])
        pg.draw.line(surface, HIT_COLOR,
                     (self.X0 + (self.X1 - self.X0)*0.125 - dx,
                      self.Y0 + (self.Y1 - self.Y0)*0.125 - dy),
                     (self.X1 - (self.X1 - self.X0)*0.125 - dx,
                      self.Y1 - (self.Y1 - self.Y0)*0.125 - dy), self.widths[1])
        pg.draw.line(surface, HIT_COLOR,
                     (self.X0 + (self.X1 - self.X0)*0.25 - dx,
                      self.Y0 + (self.Y1 - self.Y0)*0.25 - dy),
                     (self.X1 - (self.X1 - self.X0)*0.25 - dx,
                      self.Y1 - (self.Y1 - self.Y0)*0.25 - dy), self.widths[2])


class SpecialEffect:
    def __init__(self, x, y, duration):
        self.x = x
        self.y = y
        self.t = 0
        self.duration = duration
        self.running = True

    def update(self, dt):
        self.t = min(self.t + dt, self.duration)
        if self.t >= self.duration:
            self.running = False

    def draw(self, screen, dx, dy):
        pass


class BulletHitLines(SpecialEffect):
    def __init__(self, x, y, size: str):
        super().__init__(x, y, duration=90)
        self.lines = self.create_lines(size)

    def create_lines(self, size):
        lines = []
        beta = 0
        for i in range(4):
            angle = uniform(pi/16, 7*pi/16) + beta
            beta += pi/2
            lines.append(Line(self.x, self.y, size, angle, self.duration))
        return lines

    def update(self, dt):
        super().update(dt)

        for line in self.lines:
            line.update(dt)

    def draw(self, surface, dx, dy):
        for line in self.lines:
            line.draw(surface, dx, dy)


class BulletHitCircle(SpecialEffect):
    def __init__(self, x, y, color):
        super().__init__(x, y, duration=125)
        self.r = HF(96)
        self.circle = Circle(HF(64), HF(3), color, 0, 0, True, HF(0.51), HF(128), True)
        self.circle.scaling_phase = 0.75
        self.surface = pg.Surface((2 * self.r, 2 * self.r))
        self.alpha = 255
        self.surface.set_alpha(self.alpha)
        self.surface.set_colorkey(BLACK)

    def update(self, dt):
        super().update(dt)

        self.circle.update(self.r, self.r, dt)

        self.alpha = max(self.alpha - 255 * dt/self.duration, 0)
        self.surface.set_alpha(self.alpha)

    def draw(self, screen, dx, dy):
        self.surface.fill(BLACK)
        self.circle.draw(self.surface, 0, 0)
        screen.blit(self.surface, (self.x - self.r - dx, self.y - self.r - dy))


class Armor(SpecialEffect):
    def __init__(self, x, y, radius):
        super().__init__(x + HF(5), y, duration=500)
        self.surface = pg.Surface((2*radius, 2*radius))
        self.surface.fill(COLOR_KEY)
        pg.draw.circle(self.surface, WHITE, (radius, radius), radius)
        self.surface.set_colorkey(COLOR_KEY)
        self.surface.set_alpha(255)
        self.is_shifted = False

    def shift(self):
        self.x -= HF(5)
        self.is_shifted = True

    def update(self, dt):
        super().update(dt)
        alpha = 255 * (1 - self.t / self.duration)
        self.surface.set_alpha(alpha)
        if self.t >= 50 and not self.is_shifted:
            self.shift()

    def draw(self, screen, dx, dy):
        screen.blit(self.surface, (self.x, self.y))


class ParalyzingExplosion(SpecialEffect):
    def __init__(self, x, y, max_diam):
        super().__init__(x, y, duration=300)
        self.surface_0 = pg.image.load(PARALYZING_EXPLOSION).convert_alpha()
        self.surface = None
        self.max_diam = max_diam
        self.diam = None

    def update(self, dt):
        super().update(dt)
        if self.t <= self.duration:
            self.diam = round(self.max_diam * self.t / self.duration)
            self.surface = pg.transform.scale(self.surface_0, (self.diam, self.diam))

    def draw(self, screen, dx, dy):
        screen.blit(self.surface, (self.x - self.diam/2 - dx,
                                   self.y - self.diam/2 - dy))


class PowerfulExplosion(SpecialEffect):
    def __init__(self, x, y):
        super().__init__(x, y, duration=300)
        self.surface_0 = pg.image.load(POWERFUL_EXPLOSION).convert_alpha()
        self.surface = None
        self.max_diam = HF(1000)
        self.diam = None

    def update(self, dt):
        super().update(dt)
        if self.t <= self.duration:
            self.diam = round(self.max_diam * self.t / self.duration)
            self.surface = pg.transform.scale(self.surface_0, (self.diam, self.diam))

    def draw(self, screen, dx, dy):
        screen.blit(self.surface, (self.x - self.diam // 2 - dx,
                                   self.y - self.diam // 2 - dy))


class Flash(SpecialEffect):
    def __init__(self):
        super().__init__(0, 0, duration=200)
        self.surface = pg.Surface((SCR_W, SCR_H))
        self.surface.fill(WHITE)

    def update(self, dt):
        super().update(dt)
        alpha = 255 * (1 - self.t/self.duration)
        self.surface.set_alpha(alpha)

    def draw(self, screen, dx, dy):
        screen.blit(self.surface, (0, 0))


class StarsAroundMob(SpecialEffect):
    def __init__(self, mob_x, mob_y, mob_radius):
        super().__init__(mob_x, mob_y, duration=2000)

        self.angle = uniform(0, 2*pi)
        self.timer = 0
        self.radius = mob_radius + HF(60)
        self.big_stars_marker = True

    def get_stars_coords(self, dx, dy):
        pos_1 = (
            round(self.x + self.radius * cos(self.angle) - dx),
            round(self.y - self.radius * sin(self.angle) - dy)
        )
        pos_2 = (
            round(self.x + self.radius * cos(self.angle+2/3*pi) - dx),
            round(self.y - self.radius * sin(self.angle+2/3*pi) - dy)
        )
        pos_3 = (
            round(self.x + self.radius * cos(self.angle+4/3*pi) - dx),
            round(self.y - self.radius * sin(self.angle+4/3*pi) - dy)
        )
        return pos_1, pos_2, pos_3

    def update_stars_marker(self, dt):
        self.timer += dt
        if self.timer >= 80:
            self.timer -= 80
            self.angle += 0.4 * pi
            self.big_stars_marker = not self.big_stars_marker

    def update(self, dt):
        super().update(dt)
        self.update_stars_marker(dt)

    @staticmethod
    def draw_big_star(screen, x, y):
        pg.draw.circle(screen, WHITE, (x, y), H(8), H(3))
        pg.draw.line(screen, WHITE, (x, y - H(27)), (x, y + H(11)), H(3))
        pg.draw.line(screen, WHITE, (x - H(10), y), (x + H(13), y), H(3))

    @staticmethod
    def draw_small_star(screen, x, y):
        pg.draw.circle(screen, WHITE, (x, y), H(5))

    def draw(self, screen, dx, dy):
        if self.big_stars_marker:
            for pos in self.get_stars_coords(dx, dy):
                self.draw_big_star(screen, *pos)
        else:
            for pos in self.get_stars_coords(dx, dy):
                self.draw_small_star(screen, *pos)


class TeleportationFlash(SpecialEffect):
    def __init__(self, x, y):
        super().__init__(x, y, duration=250)
        self.surface_0 = pg.image.load(TELEPORTATION).convert_alpha()
        self.surface = None
        self.diam = 0
        self.max_diam = HF(320)

    def update(self, dt):
        super().update(dt)
        if self.t <= self.duration:
            self.diam = int(self.max_diam * (1 - self.t/self.duration))
            self.surface = pg.transform.scale(self.surface_0, (self.diam, self.diam))

    def draw(self, screen, dx, dy):
        screen.blit(self.surface, (self.x - self.diam/2 - dx,
                                   self.y - self.diam/2 - dy))


def add_effect(name, effects, x=0, y=0, radius=0):
    if name in ('SmallHitLines', 'BigHitLines'): effect = BulletHitLines(x, y, name)
    elif name == 'RedHitCircle': effect = BulletHitCircle(x, y, RED)
    elif name == 'VioletHitCircle': effect = BulletHitCircle(x, y, VIOLET)
    elif name == 'Armor': effect = Armor(x, y, radius)
    elif name == 'ParalyzingExplosion': effect = ParalyzingExplosion(x, y, HF(960))
    elif name == 'BigParalyzingExplosion': effect = ParalyzingExplosion(x, y, HF(1440))
    elif name == 'PowerfulExplosion': effect = PowerfulExplosion(x, y)
    elif name == 'Flash': effect = Flash()
    elif name == 'StarsAroundMob': effect = StarsAroundMob(x, y, radius)
    else: effect = TeleportationFlash(x, y)
    effects.append(effect)

import pygame as pg
from random import uniform
from math import pi, sin, cos

from components.circle import make_circle
from components.utils import *
from data.constants import *
from data.bullets import BULLETS
from assets.paths import *


# load all images only one time, to increase game performance
images = {
    "conversion": pg.image.load(DRONE_CONVERSION).convert_alpha(),
    "teleport": pg.image.load(TELEPORTATION).convert_alpha(),
    "damage_burst": pg.image.load(DAMAGE_BURST_IMAGE).convert_alpha(),
    "damage_burst_bg": pg.image.load(DAMAGE_BURST_BG_IMAGE).convert_alpha(),
    "stun_burst": pg.image.load(STUN_BURST_IMAGE).convert_alpha()
}


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

    @staticmethod
    def set_image(name, size):
        return pg.transform.scale(images[name], (size, size))

    def update(self, dt):
        self.t = min(self.t + dt, self.duration)
        if self.t == self.duration:
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


class LeechEffect(SpecialEffect):
    circles_data = [
        # radius  |  width
        (H(4.224),  H(1)),
        (H(13.704), H(1)),
        (H(23.232), H(1)),
        (H(32.664), H(1)),
        (H(42.144), H(1.224)),
        (H(51.48),  H(1.512)),
        (H(60.936), H(1.776)),
        (H(70.488), H(2.04)),
        (H(79.944), H(2.28)),
        (H(89.424), H(2.544))
    ]
    frames = {
        0: [0],
        1: [1],
        2: [2, 0],
        3: [3, 1],
        4: [4, 2, 0],
        5: [5, 3, 1],
        6: [6, 4, 2],
        7: [7, 5, 3],
        8: [8, 6, 4],
        9: [9, 7, 5],
        10: [9, 8, 6],
        11: [9, 7],
        12: [9, 8],
        13: [9],
    }

    def __init__(self, x, y):
        super().__init__(x, y, duration=249)

    def draw(self, screen, dx, dy):
        frame = max(13, int(14 * self.t / self.duration))
        for index in self.frames[frame]:
            r, w = self.circles_data[index]
            pg.draw.circle(screen, LEECH_EFFECT_COLOR, (self.x-dx, self.y-dy), r, w)


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


class SpriteEffect(SpecialEffect):
    def __init__(self, x, y, surfaces, duration, fixed=False):
        super().__init__(x, y, duration)
        self.surfaces = surfaces
        self.index = 0
        self.fixed = fixed

    def update(self, dt):
        super().update(dt)
        self.index = min(len(self.surfaces) - 1, int(self.t/self.duration * len(self.surfaces)))

    def draw(self, screen, dx, dy):
        surface = self.surfaces[self.index]
        if self.fixed:
            dx = dy = 0
        screen.blit(surface, (self.x - surface.get_width()/2 - dx,
                              self.y - surface.get_height()/2 - dy))


def _init_conversion_surfaces() -> list:
    surfaces = []
    start_diam = HF(75.84)
    delta_diam = HF(97.4)
    for i in range(19):
        diam = round(start_diam + i * delta_diam)
        image = pg.transform.scale(images["conversion"], (diam, diam))
        if i >= 15:
            alpha = round((19 - i)/5 * 255)
            image.set_alpha(alpha)
        surface = pg.Surface(image.get_size(), pg.SRCALPHA)
        surface.blit(image, (0, 0))
        surfaces.append(surface)
    return surfaces


def _init_flash_surfaces() -> list:
    surfaces = []
    n = 4
    for i in range(n):
        alpha = round(255 * (n - i) / n)
        surface = pg.Surface(SCR_SIZE, pg.SRCALPHA)
        surface.fill((255, 255, 255, alpha))
        surfaces.append(surface)
    return surfaces


def _init_teleport_surfaces() -> list:
    surfaces = []
    alphas = [255, 254, 247, 235, 218, 197, 171, 140, 104, 64]
    diameters = [HF(264.24), HF(261.84), HF(254.64), HF(242.88), HF(226.32),
                 HF(204.96), HF(178.8), HF(148.08), HF(112.32), HF(72.0)]
    for alpha, diam in zip(alphas, diameters):
        size = (round(diam), round(diam))
        image = pg.transform.scale(images["teleport"], size)
        image.set_alpha(alpha)
        surface = pg.Surface(image.get_size(), pg.SRCALPHA)
        surface.blit(image, (0, 0))
        surfaces.append(surface)
    return surfaces


def _init_stun_burst_surfaces(size) -> list:
    scale = size / 600
    surfaces = []
    alphas = [207, 164, 125, 92, 64, 41, 23]
    diameters = [HF(57.6), HF(132.24), HF(201.6), HF(265.2), HF(323.28),
                 HF(375.84), HF(422.88), HF(464.4), HF(500.4), HF(530.88),
                 HF(555.84), HF(575.04), HF(588.96), HF(597.36), HF(600)]

    for diam in diameters:
        diam *= scale
        size = (round(diam), round(diam))
        surface = pg.transform.scale(images["stun_burst"], size)
        surfaces.append(surface)

    size = surfaces[-1].get_size()
    base_surface = pg.transform.scale(images["stun_burst"], size)
    for alpha in alphas:
        base_surface.set_alpha(alpha)
        surface = pg.Surface(size, pg.SRCALPHA)
        surface.blit(base_surface, (0, 0))
        surfaces.append(surface)

    return surfaces


def _init_damage_burst_surfaces(size) -> list:
    scale = size / 720
    surfaces = []
    bg_alphas = [255, 236, 217, 197, 177, 158, 138, 118, 98, 79, 59, 39, 20, 0]
    alphas = [255, 255, 243, 230, 217, 204, 191, 178, 165, 152, 139, 126, 113, 100]
    diameters = [HF(0), HF(72), HF(126), HF(180), HF(234), HF(288), HF(342),
                 HF(396), HF(450), HF(504), HF(558), HF(612), HF(666), HF(720)]

    max_diam = round(diameters[-1] * scale)
    max_size = (max_diam, max_diam)
    bg_image = pg.transform.scale(images["damage_burst_bg"], max_size)

    for diam, alpha, bg_alpha in zip(diameters, alphas, bg_alphas):
        diam = round(diam * scale)
        size = (diam, diam)
        image = pg.transform.scale(images["damage_burst"], size)
        image.set_alpha(alpha)
        image_pos = round((max_diam - diam) / 2), round((max_diam - diam) / 2)
        bg_image.set_alpha(bg_alpha)
        surface = pg.Surface(max_size, pg.SRCALPHA)
        surface.blit(image, image_pos)
        surface.blit(bg_image, (0, 0))
        surfaces.append(surface)
    return surfaces


def _init_sticky_circle_surfaces() -> list:
    surfaces = []
    circle = make_circle(BULLETS["sticky"]["circles"][0], 20)
    circle.update_pos(circle.radius, circle.radius, 0, 0)
    circle.update_glares(0)
    max_diam = round(circle.max_radius * 2)
    base_surface = pg.Surface((max_diam, max_diam), pg.SRCALPHA)
    circle.draw(base_surface)
    diameters = [H(52.8), H(76.8), H(100.32), H(123.84), H(147.36)]
    alphas = [255, 205, 154, 102, 51]
    for diam, alpha in zip(diameters, alphas):
        image = pg.transform.smoothscale(base_surface, (diam, diam))
        image.set_alpha(alpha)
        surface = pg.Surface(image.get_size(), pg.SRCALPHA)
        surface.blit(image, (0, 0))
        surfaces.append(surface)
    return surfaces


def _init_light_red_circle_surfaces():
    surfaces = []
    circle_data = {
        "type": "fixed",
        "color": "light red",
        "radius": 150,
        "edge factor": 0.087,
        "distance": 0,
        "angle": 0
    }
    circle = make_circle(circle_data)
    circle.update_pos(circle.max_radius, circle.max_radius, 0, 0)
    circle.update_glares(0)
    max_diam = round(circle.max_radius * 2)
    base_surface = pg.Surface((max_diam, max_diam), pg.SRCALPHA)
    circle.draw(base_surface)
    diameters = [H(20.64), H(64.32), H(103.2), H(135.36), H(161.76), H(182.4), H(196.32)]
    alphas = [255, 196, 144, 100, 64, 36, 16]
    for diam, alpha in zip(diameters, alphas):
        image = pg.transform.smoothscale(base_surface, (diam, diam))
        image.set_alpha(alpha)
        surface = pg.Surface(image.get_size(), pg.SRCALPHA)
        surface.blit(image, (0, 0))
        surfaces.append(surface)
    return surfaces


def _init_red_circle_surfaces():
    surfaces = []
    circle_data = {
        "type": "fixed",
        "color": "red",
        "radius": 150,
        "edge factor": 0.086,
        "distance": 0,
        "angle": 0
    }
    circle = make_circle(circle_data)
    circle.update_pos(circle.max_radius, circle.max_radius, 0, 0)
    circle.update_glares(0)
    max_diam = round(circle.max_radius * 2)
    base_surface = pg.Surface((max_diam, max_diam), pg.SRCALPHA)
    circle.draw(base_surface)
    diameters = [H(20.64), H(64.32), H(103.2), H(135.36), H(161.76), H(182.4), H(196.32)]
    alphas = [255, 196, 144, 100, 64, 36, 16]
    for diam, alpha in zip(diameters, alphas):
        image = pg.transform.smoothscale(base_surface, (diam, diam))
        image.set_alpha(alpha)
        surface = pg.Surface(image.get_size(), pg.SRCALPHA)
        surface.blit(image, (0, 0))
        surfaces.append(surface)
    return surfaces


def _init_spawner_burst_surfaces():
    surfaces = []
    circle_data = {
        "type": "fixed",
        "color": "orange",
        "radius": 98.16,
        "edge factor": 0.04,
        "distance": 0,
        "angle": 0
    }
    circle = make_circle(circle_data)
    circle.update_pos(circle.max_radius, circle.max_radius, 0, 0)
    circle.update_glares(0)
    max_diam = round(circle.max_radius * 2)
    base_surface = pg.Surface((max_diam, max_diam), pg.SRCALPHA)
    circle.draw(base_surface)
    diameters = [H(239.2), H(280.32), H(322.56), H(182.52)]
    alphas = [205, 154, 102, 51]
    for diam, alpha in zip(diameters, alphas):
        image = pg.transform.smoothscale(base_surface, (diam, diam))
        image.set_alpha(alpha)
        surface = pg.Surface(image.get_size(), pg.SRCALPHA)
        surface.blit(image, (0, 0))
        surfaces.append(surface)
    return surfaces


def _init_shield_surfaces() -> list:
    surfaces = []
    radius = H(160)
    surf_size = (2*radius, 2*radius)
    alphas = [254, 177, 162, 146, 131, 115, 100, 85, 69, 54, 38, 23, 8]
    for alpha in alphas:
        surface = pg.Surface(surf_size, pg.SRCALPHA)
        pg.draw.circle(surface, (255, 255, 255, alpha), (radius, radius), radius)
        surfaces.append(surface)
    return surfaces


def _init_sapper_attack_surfaces() -> list:
    size = (H(166), H(166))
    surfaces = [
        pg.transform.scale(pg.image.load(SAPPER_IMG_1).convert_alpha(), size),
        pg.transform.scale(pg.image.load(SAPPER_IMG_2).convert_alpha(), size),
        pg.transform.scale(pg.image.load(SAPPER_IMG_3).convert_alpha(), size),
        pg.transform.scale(pg.image.load(SAPPER_IMG_4).convert_alpha(), size),
        pg.transform.scale(pg.image.load(SAPPER_IMG_5).convert_alpha(), size),
        pg.transform.scale(pg.image.load(SAPPER_IMG_6).convert_alpha(), size),
        pg.transform.scale(pg.image.load(SAPPER_IMG_7).convert_alpha(), size),
        pg.transform.scale(pg.image.load(SAPPER_IMG_8).convert_alpha(), size),
    ]
    return surfaces


def _init_sapper_surfaces() -> list:
    surfaces = []
    diam = H(55)
    radius = H(27.5)
    surf_size = (diam, diam)
    circle_data = {
        "type": "fixed",
        "color": "red",
        "radius": 98.16,
        "edge factor": 0.122,
        "distance": 0,
        "angle": 0
    }
    circle = make_circle(circle_data)
    circle.update_pos(circle.max_radius, circle.max_radius, 0, 0)
    circle.update_glares(0)
    circle_diam = round(circle.max_radius * 2)
    surface_1 = pg.Surface((circle_diam, circle_diam), pg.SRCALPHA)
    circle.draw(surface_1)
    surface_2 = pg.Surface(surf_size, pg.SRCALPHA)
    pg.draw.circle(surface_2, WHITE, (radius, radius), radius)
    for i in range(10):
        alpha = round(51 + 128 * i/9)
        d = round((0.653 + 0.347 * i/9) * HF(55))
        scaled_surface = pg.transform.smoothscale(surface_1, (d, d))
        surface_2.set_alpha(alpha)
        surface = pg.Surface(surf_size, pg.SRCALPHA)
        surface.blit(scaled_surface, (round(diam - d)/2, round(diam - d)/2))
        surface.blit(surface_2, (0, 0))
        surfaces.append(surface)
    for i in range(8, -1, -1):
        surfaces.append(surfaces[i])
    return surfaces


def _init_infection_surfaces() -> list:
    surfaces = []
    w, h = HF(120.286), HF(114.887)
    circle_surfaces = []
    k = 0.181
    for surface in red_circle_surfaces:
        diam = round(k * surface.get_width())
        circle_surfaces.append(pg.transform.smoothscale(surface, (diam, diam)))
    positions = [
        (HF(44.284), 0.508 * pi),
        (HF(39.183), 0.267 * pi),
        (HF(40.364), 0.844 * pi),
        (HF(4.759), 0.41 * pi),
        (HF(12.402), -0.9 * pi),
        (HF(42.413), 0.871 * pi),
        (HF(42.86), -0.549 * pi),
        (HF(35.49), -0.24 * pi),
        (HF(48.775), 0.015 * pi)
    ]
    for circle_surf in circle_surfaces:
        surface = pg.Surface((w, h), pg.SRCALPHA)
        for distance, angle in positions:
            x = round(w/2 + distance * cos(angle) - circle_surf.get_width()/2)
            y = round(h/2 - distance * sin(angle) - circle_surf.get_height()/2)
            surface.blit(circle_surf, (x, y))
        surfaces.append(surface)
    return surfaces


conversion_surfaces = _init_conversion_surfaces()
flash_surfaces = _init_flash_surfaces()
teleport_surfaces = _init_teleport_surfaces()
stun_burst_surfaces = _init_stun_burst_surfaces(800)
stun_burst_large_surfaces = _init_stun_burst_surfaces(1100)
damage_burst_surfaces = _init_damage_burst_surfaces(360)
damage_burst_large_surfaces = _init_damage_burst_surfaces(720)
sticky_circle_surfaces = _init_sticky_circle_surfaces()
light_red_circle_surfaces = _init_light_red_circle_surfaces()
red_circle_surfaces = _init_red_circle_surfaces()
shield_surfaces = _init_shield_surfaces()
spawner_burst_surfaces = _init_spawner_burst_surfaces()
sapper_attack_surfaces = _init_sapper_attack_surfaces()
sapper_surfaces = _init_sapper_surfaces()
infection_surfaces = _init_infection_surfaces()


def add_effect(name, effects, x=0, y=0, radius=0):
    if name in ('SmallHitLines', 'BigHitLines'):
        effects.append(BulletHitLines(x, y, name))
    elif name == 'LightRedCircle':
        effects.append(SpriteEffect(x, y, light_red_circle_surfaces, 126))
    elif name == 'RedCircle':
        effects.append(SpriteEffect(x, y, red_circle_surfaces, 126))
    elif name == 'StickyCircle':
        effects.append(SpriteEffect(x, y, sticky_circle_surfaces, 108))
    elif name == 'Shield':
        effects.append(SpriteEffect(x, y, shield_surfaces, 452, fixed=True))
    elif name == "StunBurst":
        effects.append(SpriteEffect(x, y, stun_burst_surfaces, 397))
    elif name == 'StunBurstLarge':
        effects.append(SpriteEffect(x, y, stun_burst_large_surfaces, 397))
    elif name == 'DamageBurst':
        effects.append(SpriteEffect(x, y, damage_burst_surfaces, 253))
    elif name == 'DamageBurstLarge':
        effects.append(SpriteEffect(x, y, damage_burst_large_surfaces, 253))
    elif name == "Conversion":
        effects.append(SpriteEffect(x, y, conversion_surfaces, 344))
    elif name == "Flash":
        effects.append(SpriteEffect(SCR_W2, SCR_H2, flash_surfaces, 83, fixed=True))
    elif name == 'StarsAroundMob':
        effects.append(StarsAroundMob(x, y, radius))
    elif name == "Teleport":
        effects.append(SpriteEffect(x, y, teleport_surfaces, 193))
    elif name == "SpawnerBurst":
        effects.append(SpriteEffect(x, y, spawner_burst_surfaces, 108))
    elif name == "SapperAttack":
        effects.append(SpriteEffect(SCR_W2, SCR_H2, sapper_attack_surfaces, 144, fixed=True))
    elif name == "LeechEffect":
        effects.append(LeechEffect(x, y))


__all__ = ["add_effect", "sapper_surfaces", "infection_surfaces"]

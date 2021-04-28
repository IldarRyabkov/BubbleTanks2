import pygame as pg
from math import sqrt, hypot, sin, cos, pi, ceil

from data.paths import *
from data.config import *
from data.colors import *


def create_room_bg() -> list:
    img = pg.transform.scale(pg.image.load(ROOM_BG).convert_alpha(),
                             (2 * ROOM_RADIUS, 2 * ROOM_RADIUS))
    room_bg = list()
    r = ROOM_RADIUS
    w = ROOM_RADIUS // 4
    step = w // 7
    for y in range(0, w, step):
        d = sqrt(r * r - (r - y - step) * (r - y - step))
        room_bg.append(img.subsurface(pg.Rect(r - d, y, 2 * d, step)))

    for y in range(w, r, step):
        d1 = sqrt(r * r - (r - y - step) * (r - y - step))
        d2 = ceil(sqrt((r - w) * (r - w) - (r - y) * (r - y)))
        room_bg.append(img.subsurface(pg.Rect(r - d1, y, d1 - d2, step)))
        room_bg.append(img.subsurface(pg.Rect(r + d2, y, d1 - d2, step)))

    for y in range(r, 2 * r - w, step):
        d1 = sqrt(r * r - (r - y) * (r - y))
        d2 = ceil(sqrt((r - w) * (r - w) - (r - y - step) * (r - y - step)))
        room_bg.append(img.subsurface(pg.Rect(r - d1, y, d1 - d2, step)))
        room_bg.append(img.subsurface(pg.Rect(r + d2, y, d1 - d2, step)))

    for y in range(2 * r - w, 2 * r, step):
        d = sqrt(r * r - (r - y) * (r - y))
        room_bg.append(img.subsurface(pg.Rect(r - d, y, 2 * d, step)))
    return room_bg


def create_room_glares() -> list:
    room_glares = list()
    room_glares.append(RoomGlare(-7/60, -17/60, 1/3))
    room_glares.append(RoomGlare(7/24, -17/40, 11/60))
    room_glares.append(RoomGlare(13/12, 11/12, 1/3))
    room_glares.append(RoomGlare(103/120, 149/120, 11/60))
    return room_glares


class RoomGlare:
    def __init__(self, x_coeff: float, y_coeff: float, diam_coeff: float):
        self.x = x_coeff * SCR_H
        self.y = y_coeff * SCR_H
        self.image = pg.image.load(ROOM_GLARE).convert_alpha()
        diam = int(diam_coeff * SCR_H)
        self.surface = pg.transform.scale(self.image, (diam, diam))

    def draw(self, surface, dx, dy):
        surface.blit(self.surface, (int(self.x - dx), int(self.y - dy)))


class PlayerHalo:
    x = None
    y = None
    radius = None
    surface = None

    def __init__(self, radius=int(1/6*SCR_H)):
        self.set(radius)

    def set(self, radius):
        self.radius = radius
        self.x = SCR_W2 - radius
        self.y = SCR_H2 - radius
        self.surface = pg.Surface((2*radius, 2*radius))
        self.surface.set_colorkey(COLOR_KEY)

    def draw(self, surface, offset, offset_new):
        if hypot(*offset) > ROOM_RADIUS - self.radius - 1/40 * SCR_H:
            self.surface.fill(COLOR_KEY)
            pg.draw.circle(self.surface, WHITE,
                           (self.radius, self.radius),
                           self.radius)
            pg.draw.circle(self.surface, PLAYER_BG_COLOR,
                           (self.radius, self.radius),
                           self.radius - 1/120 * SCR_H)
            pg.draw.circle(self.surface, COLOR_KEY,
                           (self.radius - int(offset[0]),
                            self.radius - int(offset[1])),
                           ROOM_RADIUS - 1/40 * SCR_H)
            if offset_new is not None:
                pg.draw.circle(self.surface, COLOR_KEY,
                               (self.radius - int(offset_new[0]),
                                self.radius - int(offset_new[1])),
                               ROOM_RADIUS - 1/40 * SCR_H)
            surface.blit(self.surface, (self.x, self.y))


class DestinationCircle:
    def __init__(self):
        self.x = 0
        self.y = 0

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, dx, dy):
        pg.draw.circle(screen, ROOM_COLOR, (self.x-dx, self.y-dy), 18)
        pg.draw.circle(screen, WHITE,      (self.x-dx, self.y-dy), 12)


class PlayerTrace:
    coords = []

    def set_coords(self, x, y, dist, angle):
        self.coords = list()
        self.coords.append((x + dist * cos(angle),
                            y - dist * sin(angle)))
        self.coords.append((x + dist * cos(angle) + 96 * cos(angle + 0.15 * pi),
                            y - dist * sin(angle) - 96 * sin(angle + 0.15 * pi)))
        self.coords.append((x + dist * cos(angle) + 64 * cos(angle - 0.25 * pi),
                            y - dist * sin(angle) - 64 * sin(angle - 0.25 * pi)))

    def draw(self, screen, dx, dy):
        for i in range(3):
            radius = 1/40 * SCR_H if i == 0 else 1/60 * SCR_H
            pos = int(self.coords[i][0] - dx), int(self.coords[i][1] - dy)
            pg.draw.circle(screen, WHITE, pos, int(radius), int(1/200 * SCR_H))


class BackgroundEnvironment:
    def __init__(self):
        self.bg = pg.transform.scale(pg.image.load(BG).convert(), SCR_SIZE)
        self.room_bg = create_room_bg()
        self.room_glares = create_room_glares()
        self.player_halo = PlayerHalo()
        self.destination_circle = DestinationCircle()
        self.player_trace = PlayerTrace()

    def set_player_halo(self, radius):
        self.player_halo.set(radius)

    def set_player_trace(self, x, y, dist, alpha):
        self.player_trace.set_coords(x, y, 0.05 * dist, alpha)

    def set_destination_circle(self, pos):
        self.destination_circle.set_pos(*pos)

    def draw_bg(self, screen):
        screen.blit(self.bg, (0, 0))

    def draw_room_bg(self, screen, dx, dy):
        for surface in self.room_bg:
            pos = surface.get_offset()
            x = SCR_W2 - ROOM_RADIUS - int(dx) + pos[0]
            y = SCR_H2 - ROOM_RADIUS - int(dy) + pos[1]
            screen.blit(surface, (x, y))

    def draw_player_halo(self, screen, pos1, pos2=None):
        self.player_halo.draw(screen, pos1, pos2)

    def draw_room_glares(self, surface, dx, dy):
        for glare in self.room_glares:
            glare.draw(surface, dx, dy)

    def draw_player_trace(self, screen, dx, dy):
        self.player_trace.draw(screen, dx, dy)

    def draw_destination_circle(self, surface, dx, dy):
        self.destination_circle.draw(surface, int(dx), int(dy))

    def draw_transportation(self, screen, offset_new, offset_old, time):
        self.draw_bg(screen)
        self.draw_room_bg(screen, *offset_new)
        self.draw_room_bg(screen, *offset_old)
        self.draw_destination_circle(screen, *offset_new)
        if time >= 0.2 * TRANSPORTATION_TIME:
            self.draw_player_trace(screen, *offset_new)
        self.draw_player_halo(screen, offset_old, offset_new)


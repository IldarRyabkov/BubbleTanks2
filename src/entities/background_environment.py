import pygame as pg

from math import cos, sin, sqrt, ceil, pi, hypot
from data.config import *
from data.colors import *
from data.paths import ROOM_BG, ROOM_GLARE
from utils import H, HF


def room_bg() -> list:
    """The background of the room is a very large surface with transparency.
    It takes a very long time to draw, so this surface is divided into many
    subsurfaces to draw only those that are currently on the screen.
    This significantly increases the FPS.

    The screen height MUST be a multiple of 6 for the subsurface
    dimensions to be calculated without mathematical errors!
    """
    img = pg.transform.scale(pg.image.load(ROOM_BG).convert_alpha(),
                             (2 * ROOM_RADIUS, 2 * ROOM_RADIUS))
    bg = []
    r = ROOM_RADIUS
    w = ROOM_RADIUS / 4
    step = ROOM_RADIUS / 28
    y = 0
    for i in range(7):
        d = sqrt(r * r - (r - y - step) * (r - y - step))
        rect_h = ceil(step) if int(y) < y else step
        bg.append(img.subsurface(pg.Rect(r - d, int(y), 2 * d, rect_h)))
        y += step

    for i in range(21):
        d1 = sqrt(r * r - (r - y - step) * (r - y - step))
        d2 = ceil(sqrt((r - w) * (r - w) - (r - y) * (r - y)))
        rect_h = ceil(step) if int(y) < y else step
        bg.append(img.subsurface(pg.Rect(r - d1, int(y), d1 - d2, rect_h)))
        bg.append(img.subsurface(pg.Rect(r + d2, int(y), d1 - d2, rect_h)))
        y += step

    for i in range(21):
        d1 = sqrt(r * r - (r - y) * (r - y))
        d2 = ceil(sqrt((r - w) * (r - w) - (r - y - step) * (r - y - step)))
        rect_h = ceil(step) if int(y) < y else step
        bg.append(img.subsurface(pg.Rect(r - d1, int(y), d1 - d2, rect_h)))
        bg.append(img.subsurface(pg.Rect(r + d2, int(y), d1 - d2, rect_h)))
        y += step

    for i in range(7):
        d = sqrt(r * r - (r - y) * (r - y))
        rect_h = ceil(step) if int(y) < y else step
        bg.append(img.subsurface(pg.Rect(r - d, int(y), 2 * d, rect_h)))
        y += step

    return bg


class RoomGlare:
    def __init__(self,
                 x: float,
                 y: float,
                 diam: float):
        self.x = x - diam / 2
        self.y = y - diam / 2
        self.image = pg.image.load(ROOM_GLARE).convert_alpha()
        self.surface = pg.transform.scale(self.image, (round(diam), round(diam)))

    def draw(self, surface, dx, dy):
        surface.blit(self.surface, (round(self.x - dx), round(self.y - dy)))


class PlayerHalo:
    def __init__(self):
        self.x = None
        self.y = None
        self.radius = None
        self.surface = None
        self.set_size(HF(160))

    def reset(self):
        self.__init__()

    def set_size(self, radius: float):
        self.radius = radius
        self.x = SCR_W2 - radius
        self.y = SCR_H2 - radius
        self.surface = pg.Surface((round(2*radius), round(2*radius)))
        self.surface.set_colorkey(COLOR_KEY)

    def draw(self, surface, offset, offset_new):
        if hypot(*offset) > ROOM_RADIUS - self.radius - HF(24):
            self.surface.fill(COLOR_KEY)
            r = round(self.radius)
            pg.draw.circle(self.surface, WHITE, (r, r), r)
            pg.draw.circle(self.surface, PLAYER_BG_COLOR, (r, r),  round(self.radius - HF(8)))
            pg.draw.circle(self.surface, COLOR_KEY,
                           (round(self.radius - offset[0]), round(self.radius - offset[1])),
                           round(ROOM_RADIUS - HF(24)))

            if offset_new is not None:
                pg.draw.circle(self.surface, COLOR_KEY,
                               (round(self.radius - offset_new[0]), round(self.radius - offset_new[1])),
                               round(ROOM_RADIUS - HF(24)))

            surface.blit(self.surface, (round(self.x), round(self.y)))


class DestinationCircle:
    """Background effect which appears when player
    is being transported from one room to another.
    Draws a circle at player's destination point.
    """
    def __init__(self):
        self.x = 0
        self.y = 0

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, dx, dy):
        pos = (round(self.x - dx), round(self.y - dy))
        pg.draw.circle(screen, ROOM_COLOR, pos, H(18))
        pg.draw.circle(screen, WHITE, pos, H(12))


class PlayerTrace:
    """Background effect which appears when player
    is being transported from one room to another.
    Imitates trace of bubbles that player's tank leaves on its way.
    """
    coords = ()  # coordinates of circles that will be drawn

    def set_coords(self, x, y, dist, angle):
        self.coords = (
            (x + dist * cos(angle), y - dist * sin(angle)),

            (x + dist * cos(angle) + HF(96) * cos(angle + 0.15 * pi),
             y - dist * sin(angle) - HF(96) * sin(angle + 0.15 * pi)),

            (x + dist * cos(angle) + HF(64) * cos(angle - 0.25 * pi),
             y - dist * sin(angle) - HF(64) * sin(angle - 0.25 * pi))
        )

    def draw(self, screen, dx, dy):
        for i, (x, y) in enumerate(self.coords):
            radius = H(24) if i == 0 else H(16)
            pg.draw.circle(screen, WHITE, (round(x - dx), round(y - dy)), radius, H(4))


__all__ = [

    "room_bg",
    "RoomGlare",
    "PlayerHalo",
    "DestinationCircle",
    "PlayerTrace"

]

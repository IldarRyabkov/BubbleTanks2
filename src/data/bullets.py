import pygame as pg
from math import pi
from constants import *
from utils import *


def create_sniper_bullet():
    w, h = H(35), H(21)
    body = pg.Surface((w, h))
    body.fill(COLOR_KEY)
    pg.draw.ellipse(body, WHITE, pg.Rect(0, 0, w, h))
    edge = H(2)
    pg.draw.ellipse(body, RED, pg.Rect(edge, edge, w - 2 * edge, h - 2 * edge))
    pg.draw.circle(body, RED_GLARE_1, (w // 4, w // 4), H(3))
    body.set_colorkey(COLOR_KEY)
    return body

SNIPER_BULLET_BODY = create_sniper_bullet()

AIR_BULLET_BODY = [
    [28, 4, BUBBLE_COLOR, 0, 0, True, 17, True, False]

]

SMALL_BUL_BODY_1 = [
    [12, 2, DARK_RED, 0, 0, False, 0, True, False]
]

SMALL_BUL_BODY_2 = [
    [12, 2, RED, 0, 0, False, 0, True, False]
]

MEDIUM_BUL_BODY_1 = [
    [19, 3, DARK_RED, 0, 0, True, 19, True, False]
]

MEDIUM_BUL_BODY_2 = [
    [21, 3, RED, 0, 0, True, 17, True, False]
]

BIG_BUL_BODY_1 = [
    [26, 4, DARK_RED, 0, 0, True, 17, True, False]
]

BIG_BUL_BODY_2 = [
    [26, 4, RED, 0, 0, True, 17, True, False]
]

GIANT_BUL_BODY = [
    [88, 7, RED, 0, 0, True, 20, True, False]
]

BOMB_BUL_BODY_1 = [
    [8,  1, DARK_RED, 16, 0,          False, 0, True, False],
    [8,  1, DARK_RED, 16, 0.667 * pi, False, 0, True, False],
    [8,  1, DARK_RED, 16, 1.333 * pi, False, 0, True, False],
    [16, 3, DARK_RED, 0,  0,          False, 0, True, False]
]

BOMB_BUL_BODY_2 = [
    [8,  1, RED, 16, 0,          False, 0, True, False],
    [8,  1, RED, 16, 0.667 * pi, False, 0, True, False],
    [8,  1, RED, 16, 1.333 * pi, False, 0, True, False],
    [16, 3, RED, 0,  0,          False, 0, True, False]
]

STICKY_BUL_BODY = [
    [26, 2, VIOLET, 0, 0, False, 0, True, False]
]

SMALL_SCALING_BUL_BODY_1 = [
    [13, 2, DARK_RED, 0, 0, True, 13, True, False]
]

SMALL_SCALING_BUL_BODY_2 = [
    [13, 2, RED, 0, 0, True, 13, True, False]
]

HOMING_MISSILE_BODY_1 = [
    [14, 2, DARK_RED, 0, 0, False, 0, True, True],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 16, 0.72 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 16, -0.72 * pi],
    [5,  1, DARK_RED, 0, 0, False, 0, True, True, 14, pi],
    [8,  1, DARK_RED, 0, 0, False, 0, True, True, 16, 0],
    [5,  1, DARK_RED, 0, 0, False, 0, True, True, 25, 0]
]

HOMING_MISSILE_BODY_2 = [
    [14, 2, RED, 0, 0, False, 0, True, True],
    [7,  1, RED, 0, 0, False, 0, True, True, 16, 0.72 * pi],
    [7,  1, RED, 0, 0, False, 0, True, True, 16, -0.72 * pi],
    [5,  1, RED, 0, 0, False, 0, True, True, 14, pi],
    [8,  1, RED, 0, 0, False, 0, True, True, 16, 0],
    [5,  1, RED, 0, 0, False, 0, True, True, 25, 0]
]

SHURIKEN_BODY = [
    [11, 1, DARK_RED, 0, 0, False, 0, True, True],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 14, pi],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 14, -0.6 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 14, -0.2 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 14, 0.2 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 14, 0.6 * pi]
]


BIG_DRONE_BODY = [
    [20, 4, DARK_RED, 0, 0, False, 0, True,  True, 18, 0],
    [9,  1, DARK_RED, 0, 0, False, 0, True,  True, 21, 0.44 * pi],
    [9,  1, DARK_RED, 0, 0, False, 0, True,  True, 21, -0.44 * pi],
    [14, 3, DARK_RED, 0, 0, False, 0, True,  True, 25, 0.67 * pi],
    [14, 3, DARK_RED, 0, 0, False, 0, True,  True, 25, -0.67 * pi]
]

MEDIUM_DRONE_BODY = [
    [15, 3, DARK_RED, 0, 0, False, 0, True, True, 14, 0],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 16, 0.44 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 16, -0.44 * pi],
    [11, 2, DARK_RED, 0, 0, False, 0, True, True, 19, 0.67 * pi],
    [11, 2, DARK_RED, 0, 0, False, 0, True, True, 19, -0.67 * pi]
]

SMALL_DRONE_BODY = [
    [12, 2, DARK_RED, 0, 0, False, 0, True, True, 11, 0],
    [5,  1, DARK_RED, 0, 0, False, 0, True, True, 12, 0.44 * pi],
    [5,  1, DARK_RED, 0, 0, False, 0, True, True, 12, -0.44 * pi],
    [8,  2, DARK_RED, 0, 0, False, 0, True, True, 15, 0.67 * pi],
    [8,  2, DARK_RED, 0, 0, False, 0, True, True, 15, -0.67 * pi]
]

TINY_DRONE_BODY = [
    [10, 2, DARK_RED, 0, 0, False, 0, True, True, 9,  0],
    [4,  1, DARK_RED, 0, 0, False, 0, True, True, 10, 0.44 * pi],
    [4,  1, DARK_RED, 0, 0, False, 0, True, True, 10, -0.44 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 12, 0.67 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0, True, True, 12, -0.67 * pi]
]

BULLET_BODIES = {
    'SmallBullet_1': scaled_body(SMALL_BUL_BODY_1),
    'SmallBullet_2': scaled_body(SMALL_BUL_BODY_2),
    'MediumBullet_1': scaled_body(MEDIUM_BUL_BODY_1),
    'MediumBullet_2': scaled_body(MEDIUM_BUL_BODY_2),
    'BigBullet_1': scaled_body(BIG_BUL_BODY_1),
    'BigBullet_2': scaled_body(BIG_BUL_BODY_2),
    'StickyBullet': scaled_body(STICKY_BUL_BODY),
    'BombBullet_1': scaled_body(BOMB_BUL_BODY_1),
    'BombBullet_2': scaled_body(BOMB_BUL_BODY_2),
    'SmallScalingBullet_1': scaled_body(SMALL_SCALING_BUL_BODY_1),
    'SmallScalingBullet_2': scaled_body(SMALL_SCALING_BUL_BODY_2),
    'SniperBullet': SNIPER_BULLET_BODY,
    'HomingMissile_1': scaled_body(HOMING_MISSILE_BODY_1),
    'HomingMissile_2': scaled_body(HOMING_MISSILE_BODY_2),
    'Shuriken': scaled_body(SHURIKEN_BODY),
    'GiantBullet': scaled_body(GIANT_BUL_BODY),
    'AirBullet': scaled_body(AIR_BULLET_BODY),
    'BigDrone': scaled_body(BIG_DRONE_BODY),
    'MediumDrone': scaled_body(MEDIUM_DRONE_BODY),
    'SmallDrone': scaled_body(SMALL_DRONE_BODY),
    'TinyDrone': scaled_body(TINY_DRONE_BODY)
}


__all__ = ["BULLET_BODIES"]

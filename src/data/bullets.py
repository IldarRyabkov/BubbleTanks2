import pygame as pg
from math import pi
from data.colors import *
from utils import scaled_body, H


def create_sniper_bullet():
    w, h = H(45), H(29)
    body = pg.Surface((w, h))
    body.fill(COLOR_KEY)
    pg.draw.ellipse(body, WHITE, pg.Rect(0, 0, w, h))
    pg.draw.ellipse(body, RED, pg.Rect(H(2), H(2), H(45 - 4), H(29 - 4)))
    pg.draw.circle(body, RED_GLARE_1, (w // 4, w // 4), H(3))
    body.set_colorkey(COLOR_KEY)
    return body

SNIPER_BULLET_BODY = create_sniper_bullet()

SMALL_BUL_BODY_1 = [
    [12, 1, DARK_RED, 0, 0, False, 0.0, 0, True, False]
]

SMALL_BUL_BODY_2 = [
    [12, 1, RED, 0, 0, False, 0.0, 0, True, False]
]

MEDIUM_BUL_BODY_1 = [
    [22, 3, DARK_RED, 0, 0, True, 0.031, 17, True, False]
]

MEDIUM_BUL_BODY_2 = [
    [22, 3, RED, 0, 0, True, 0.031, 17, True, False]
]

BIG_BUL_BODY_1 = [
    [28, 3, DARK_RED, 0, 0, True, 0.033, 17, True, False]
]

BIG_BUL_BODY_2 = [
    [28, 3, RED, 0, 0, True, 0.033, 17, True, False]
]

GIANT_BUL_BODY = [
    [88, 7, RED, 0, 0, True, 0.041, 20, True, False]
]

BOMB_BUL_BODY_1 = [
    [8,  1, DARK_RED, 16, 0,          False, 0.0, 0, True, False],
    [8,  1, DARK_RED, 16, 0.667 * pi, False, 0.0, 0, True, False],
    [8,  1, DARK_RED, 16, 1.333 * pi, False, 0.0, 0, True, False],
    [16, 3, DARK_RED, 0,  0,          False, 0.0, 0, True, False]
]

BOMB_BUL_BODY_2 = [
    [8,  1, RED, 16, 0,          False, 0.0, 0, True, False],
    [8,  1, RED, 16, 0.667 * pi, False, 0.0, 0, True, False],
    [8,  1, RED, 16, 1.333 * pi, False, 0.0, 0, True, False],
    [16, 3, RED, 0,  0,          False, 0.0, 0, True, False]
]

STICKY_BUL_BODY = [
    [25, 1, VIOLET, 0, 0, False, 0.0, 0, True, False]
]

SMALL_SCALING_BUL_BODY_1 = [
    [13, 1, DARK_RED, 0, 0, True, 0.026, 13, True, False]
]

SMALL_SCALING_BUL_BODY_2 = [
    [13, 1, RED, 0, 0, True, 0.026, 13, True, False]
]

HOMING_MISSILE_BODY_1 = [
    [14, 1, DARK_RED, 0, 0, False, 0.0, 0, True, True],
    [7,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 16, 0.72 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 16, -0.72 * pi],
    [5,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 14, pi],
    [8,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 16, 0],
    [5,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 25, 0]
]

HOMING_MISSILE_BODY_2 = [
    [14, 1, RED, 0, 0, False, 0.0, 0, True, True],
    [7,  1, RED, 0, 0, False, 0.0, 0, True, True, 16, 0.72 * pi],
    [7,  1, RED, 0, 0, False, 0.0, 0, True, True, 16, -0.72 * pi],
    [5,  1, RED, 0, 0, False, 0.0, 0, True, True, 14, pi],
    [8,  1, RED, 0, 0, False, 0.0, 0, True, True, 16, 0],
    [5,  1, RED, 0, 0, False, 0.0, 0, True, True, 25, 0]
]

SHURIKEN_BODY = [
    [11, 1, DARK_RED, 0, 0, False, 0.0, 0, True, True],
    [7,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 14, pi],
    [7,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 14, -0.6 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 14, -0.2 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 14, 0.2 * pi],
    [7,  1, DARK_RED, 0, 0, False, 0.0, 0, True, True, 14, 0.6 * pi]
]


BULLETS = {
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
    'GiantBullet': scaled_body(GIANT_BUL_BODY)
}


__all__ = ["BULLETS"]

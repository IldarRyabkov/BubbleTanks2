import pygame as pg
from math import pi
from data.colors import *
from data.config import SCR_H


def create_sniper_bullet():
    w, h = int(14/300 * SCR_H), int(3/100 * SCR_H)
    body = pg.Surface((w, h))
    body.fill(COLOR_KEY)
    pg.draw.ellipse(body, WHITE, pg.Rect(0, 0, w, h))
    pg.draw.ellipse(body, RED, pg.Rect(2, 2, w-4, h-4))
    pg.draw.circle(body, RED_GLARE_1, (w//4, w//4), int(1/300 * SCR_H))
    body.set_colorkey(COLOR_KEY)
    return body

SNIPER_BULLET_BODY = create_sniper_bullet()

SMALL_BUL_BODY_1 = [[13, 1, DARK_RED, 0, 0, False, 0, 0, 0, True, False]]
SMALL_BUL_BODY_2 = [[13, 1, RED,      0, 0, False, 0, 0, 0, True, False]]

MEDIUM_BUL_BODY_1 = [[22, 3, DARK_RED, 0, 0, True, 0.035, 20, 0, True, False]]
MEDIUM_BUL_BODY_2 = [[22, 3, RED,      0, 0, True, 0.035, 20, 0, True, False]]

BIG_BUL_BODY_1 = [[29, 3, DARK_RED, 0, 0, True, 0.037, 20, 0,    True, False]]
BIG_BUL_BODY_2 = [[29, 3, RED,      0, 0, True, 0.037, 20, 0.25, True, False]]

GIANT_BUL_BODY = [[93, 6, RED,      0, 0, True, 0.037, 20, 0.25, True, False]]

BOMB_BUL_BODY_1 = [[10,  1, DARK_RED, 19, 0,      False, 0, 0, 0, True, False],
                   [10,  1, DARK_RED, 19, 2*pi/3, False, 0, 0, 0, True, False],
                   [10,  1, DARK_RED, 19, 4*pi/3, False, 0, 0, 0, True, False],
                   [19,  3, DARK_RED, 0,  0,      False, 0, 0, 0, True, False]]

BOMB_BUL_BODY_2 = [[10,  1, RED,      19, 0,      False, 0, 0, 0, True, False],
                   [10,  1, RED,      19, 2*pi/3, False, 0, 0, 0, True, False],
                   [10,  1, RED,      19, 4*pi/3, False, 0, 0, 0, True, False],
                   [19,  3, RED,      0,  0,      False, 0, 0, 0, True, False]]

STICKY_BUL_BODY = [[29, 1, VIOLET, 0, 0, False, 0, 0, 0, True, False]]

SMALL_SCALING_BUL_BODY_1 = [[14, 1, DARK_RED, 0, 0, True, 0.026, 14, 0, True, False]]
SMALL_SCALING_BUL_BODY_2 = [[14, 1, RED,      0, 0, True, 0.026, 14, 0, True, False]]

HOMING_MISSILE_BODY_1 = [[16, 1, DARK_RED, 0, 0, False, 0, 0, 0, True, True],
                         [8,  1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 19, 0.72 * pi],
                         [8,  1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 19, -0.72 * pi],
                         [6,  1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 16, pi],
                         [10, 1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 19, 0],
                         [6,  1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 29, 0]]

HOMING_MISSILE_BODY_2 = [[16, 1, RED, 0, 0, False, 0, 0, 0, True, True],
                         [8,  1, RED, 0, 0, False, 0, 0, 0, True, True, 19, 0.72 * pi],
                         [8,  1, RED, 0, 0, False, 0, 0, 0, True, True, 19, -0.72 * pi],
                         [6,  1, RED, 0, 0, False, 0, 0, 0, True, True, 16, pi],
                         [10, 1, RED, 0, 0, False, 0, 0, 0, True, True, 19, 0],
                         [6,  1, RED, 0, 0, False, 0, 0, 0, True, True, 29, 0]]

SHURIKEN_BODY = [[13, 1, DARK_RED, 0, 0, False, 0, 0, 0, True, True],
                 [8,  1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 16, pi],
                 [8,  1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 16, -0.6 * pi],
                 [8,  1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 16, -0.2 * pi],
                 [8,  1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 16, 0.2 * pi],
                 [8,  1, DARK_RED, 0, 0, False, 0, 0, 0, True, True, 16, 0.6 * pi]]


BULLETS = {'SmallBullet_1': SMALL_BUL_BODY_1,
           'SmallBullet_2': SMALL_BUL_BODY_2,
           'MediumBullet_1': MEDIUM_BUL_BODY_1,
           'MediumBullet_2': MEDIUM_BUL_BODY_2,
           'BigBullet_1': BIG_BUL_BODY_1,
           'BigBullet_2': BIG_BUL_BODY_2,
           'StickyBullet': STICKY_BUL_BODY,
           'BombBullet_1': BOMB_BUL_BODY_1,
           'BombBullet_2': BOMB_BUL_BODY_2,
           'SmallScalingBullet_1': SMALL_SCALING_BUL_BODY_1,
           'SmallScalingBullet_2': SMALL_SCALING_BUL_BODY_2,
           'SniperBullet': SNIPER_BULLET_BODY,
           'HomingMissile_1': HOMING_MISSILE_BODY_1,
           'HomingMissile_2': HOMING_MISSILE_BODY_2
           }

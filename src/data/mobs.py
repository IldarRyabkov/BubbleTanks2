from math import pi
from data.colors import *
from data.config import *
from utils import *


BOSS_HEAD_BODY = [

    [68,  2, BLUE,   0,   0,           True,  0.043, 25, True,  False],
    [49,  5, BLUE,   327, 0.055 * pi,  True,  0.077, 45, True,  False],
    [49,  5, BLUE,   327, -0.055 * pi, True,  0.077, 45, True,  False],
    [31,  3, BLUE,   391, 0.045 * pi,  True,  0.05,  29, True,  False],
    [31,  3, BLUE,   391, -0.045 * pi, True,  0.05,  29, True,  False],
    [55,  2, BLUE,   270, 0,           True,  0.041, 24, True,  False],
    [116, 5, BLUE,   128, 0,           True,  0.071, 42, True,  False],
    [31,  3, BLUE,   14,  0,           True,  0.051, 31, True,  False],
    [31,  3, BLUE,   135, 0.31 * pi,   True,  0.051, 31, True,  False],
    [31,  3, BLUE,   135, -0.31 * pi,  True,  0.051, 31, True,  False],
    [51,  2, BLUE,   213, 0.22 * pi,   True,  0.036, 21, True,  False],
    [51,  2, BLUE,   213, -0.22 * pi,  True,  0.036, 21, True,  False],
    [36,  4, BLUE,   274, 0.225 * pi,  True,  0.057, 34, True,  False],
    [36,  4, BLUE,   274, -0.225 * pi, True,  0.057, 34, True,  False],
    [21,  2, BLUE,   312, 0.21 * pi,   True,  0.031, 18, True,  False],
    [21,  2, BLUE,   312, -0.21 * pi,  True,  0.031, 18, True,  False],
    [14,  1, ORANGE, 113, 0,           False, 0.0,   0,  True,  True,  39, 0.26 * pi],
    [14,  1, ORANGE, 113, 0,           False, 0.0,   0,  True,  True,  39, -0.26 * pi],
    [14,  1, ORANGE, 113, 0,           False, 0.0,   0,  True,  True,  48, 0.16 * pi],
    [14,  1, ORANGE, 113, 0,           False, 0.0,   0,  True,  True,  48, -0.16 * pi],
    [14,  1, ORANGE, 113, 0,           False, 0.0,   0,  True,  True,  59, 0.065 * pi],
    [14,  1, ORANGE, 113, 0,           False, 0.0,   0,  True,  True,  59, -0.065 * pi],
    [21,  2, ORANGE, 113, 0,           False, 0.0,   0,  True,  True,  81, 0],
    [42,  4, ORANGE, 113, 0,           False, 0.0,   0,  True,  True,  0,  0],
    [14,  1, ORANGE, 298, 0,           True,  0.021, 12, True,  True,  41, 0.25 * pi],
    [14,  1, ORANGE, 298, 0,           True,  0.021, 12, True,  True,  41, -0.25 * pi],
    [14,  1, ORANGE, 298, 0,           True,  0.021, 12, True,  True,  59, 0.167 * pi],
    [14,  1, ORANGE, 298, 0,           True,  0.021, 12, True,  True,  59, -0.167 * pi],
    [12,  1, ORANGE, 298, 0,           True,  0.021, 12, True,  True,  78, 0.125 * pi],
    [12,  1, ORANGE, 298, 0,           True,  0.021, 12, True,  True,  78, -0.125 * pi],
    [8,   1, ORANGE, 298, 0,           True,  0.014, 8,  True,  True,  79, -0.19 * pi],
    [8,   1, ORANGE, 298, 0,           True,  0.014, 8,  True,  True,  79, 0.19 * pi],
    [39,  4, ORANGE, 298, 0,           True,  0.063, 36, True,  True,  0,  0],
    [17,  1, ORANGE, 298, 0,           True,  0.024, 14, True,  True,  42, -1.0 * pi],
    [17,  1, ORANGE, 298, 0,           True,  0.024, 14, True,  True,  42, -0.667 * pi],
    [17,  1, ORANGE, 298, 0,           True,  0.024, 14, True,  True,  42, 0.667 * pi],
    [19,  1, VIOLET, 19,  -0.15 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 31,  -0.35 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 45,  0.22 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 45,  -0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 42,  -0.75 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [18,  1, VIOLET, 56,  -0.8 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [24,  1, VIOLET, 41,  0.82 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 11,  0.5 * pi,    False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 54,  0.6 * pi,    False, 0.0,   0,  False, False, 0,  0],
    [17,  1, VIOLET, 31,  0.65 * pi,   False, 0.0,   0,  False, False, 0,  0]

]

BOSS_HEAD_PARAMS = {
    "name": "BossHead",
    "x": SCR_W2,
    "y": SCR_H2 - HF(1000),
    "health": 250,
    "health_states": ((0, ),),
    "bubbles": {"small": 0, "medium": 5, "big": 3},
    "radius": HF(116),
    "body": scaled_body(BOSS_HEAD_BODY),
    "gun_type": 'GunBossHead',
    "angular_vel": 0,
    "body_size": HF(400),
    "trajectory": no_trajectory
}

BOSS_LEG_BODY = [

    [58, 2, BLUE,   85,  -0.75 * pi,  True,  0.041, 24, True,  False],
    [58, 2, BLUE,   85,  -1.25 * pi,  True,  0.041, 24, True,  False],
    [34, 3, BLUE,   142, -0.84 * pi,  True,  0.051, 31, True,  False],
    [34, 3, BLUE,   142, -1.16 * pi,  True,  0.051, 31, True,  False],
    [85, 3, BLUE,   28,  0,           True,  0.057, 34, True,  False],
    [34, 3, BLUE,   113, -0.34 * pi,  True,  0.051, 31, True,  False],
    [34, 3, BLUE,   113, -1.66 * pi,  True,  0.051, 31, True,  False],
    [25, 3, BLUE,   156, -0.34 * pi,  True,  0.038, 22, True,  False],
    [25, 3, BLUE,   156, -1.66 * pi,  True,  0.038, 22, True,  False],
    [19, 2, BLUE,   190, -0.34 * pi,  True,  0.028, 17, True,  False],
    [19, 2, BLUE,   190, -1.66 * pi,  True,  0.028, 17, True,  False],
    [8,  1, ORANGE, 174, -0.87 * pi,  True,  0.013, 7,  True,  False],
    [8,  1, ORANGE, 174, -1.13 * pi,  True,  0.013, 7,  True,  False],
    [8,  1, ORANGE, 209, -0.865 * pi, True,  0.013, 7,  True,  False],
    [8,  1, ORANGE, 209, -1.135 * pi, True,  0.013, 7,  True,  False],
    [8,  1, ORANGE, 197, -0.915 * pi, True,  0.013, 7,  True,  False],
    [8,  1, ORANGE, 197, -1.085 * pi, True,  0.013, 7,  True,  False],
    [8,  1, ORANGE, 246, -0.865 * pi, True,  0.013, 7,  True,  False],
    [8,  1, ORANGE, 246, -1.135 * pi, True,  0.013, 7,  True,  False],
    [8,  1, ORANGE, 227, -0.946 * pi, True,  0.013, 7,  True,  False],
    [8,  1, ORANGE, 227, -1.054 * pi, True,  0.013, 7,  True,  False],
    [14, 1, ORANGE, 227, -0.86 * pi,  True,  0.024, 14, True,  False],
    [14, 1, ORANGE, 227, -1.14 * pi,  True,  0.024, 14, True,  False],
    [14, 1, ORANGE, 209, -0.937 * pi, True,  0.024, 14, True,  False],
    [14, 1, ORANGE, 209, -1.063 * pi, True,  0.024, 14, True,  False],
    [14, 1, ORANGE, 256, -0.883 * pi, True,  0.024, 14, True,  False],
    [14, 1, ORANGE, 256, -1.117 * pi, True,  0.024, 14, True,  False],
    [14, 1, ORANGE, 243, -0.938 * pi, True,  0.024, 14, True,  False],
    [14, 1, ORANGE, 243, -1.062 * pi, True,  0.024, 14, True,  False],
    [15, 1, ORANGE, 193, -0.885 * pi, True,  0.024, 14, True,  False],
    [15, 1, ORANGE, 193, -1.115 * pi, True,  0.024, 14, True,  False],
    [19, 1, VIOLET, 19,  -1.15 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 31,  -1.35 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 45,  -0.78 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 45,  -1.22 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 42,  -1.75 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [18, 1, VIOLET, 56,  -1.8 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [24, 1, VIOLET, 41,  -0.18 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 11,  -0.5 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 54,  -0.4 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [17, 1, VIOLET, 31,  -0.35 * pi,  False, 0.0,   0,  False, False, 0, 0]

]

BOSS_LEG_PARAMS = {
    "name": "BossLeg",
    "x": SCR_W2,
    "y": SCR_H2 + HF(832),
    "health": 250,
    "health_states": ((0, ),),
    "bubbles": {"small": 0, "medium": 5, "big": 3},
    "radius": HF(107),
    "body": scaled_body(BOSS_LEG_BODY),
    "gun_type": 'GunBossLeg',
    "angular_vel": 0,
    "body_size": HF(427),
    "trajectory": no_trajectory
}

BOSS_HAND_BODY = [

    [128, 5, BLUE,   0,   0,          True,  0.071, 42, True,  False],
    [31,  3, BLUE,   142, 0.48 * pi,  True,  0.051, 31, True,  False],
    [31,  3, BLUE,   142, 0.96 * pi,  True,  0.051, 31, True,  False],
    [48,  4, BLUE,   149, -0.54 * pi, True,  0.077, 45, True,  False],
    [48,  4, BLUE,   149, -0.03 * pi, True,  0.077, 45, True,  False],
    [48,  4, BLUE,   149, -0.29 * pi, True,  0.077, 45, True,  False],
    [29,  3, ORANGE, 0,   0,          True,  0.05,  29, True,  True,  5,  0],
    [14,  1, ORANGE, 0,   0,          True,  0.02,  11, True,  True,  36, 0.68 * pi],
    [14,  1, ORANGE, 0,   0,          True,  0.02,  11, True,  True,  36, -0.68 * pi],
    [14,  1, ORANGE, 0,   0,          True,  0.02,  11, True,  True,  36, pi],
    [8,   1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  32, 0],
    [8,   1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  45, 0],
    [8,   1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  41, 0.22 * pi],
    [8,   1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  41, -0.22 * pi],
    [8,   1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  52, 0.17 * pi],
    [8,   1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  52, -0.17 * pi],
    [19,  1, VIOLET, 19,  -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 31,  -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 45,  0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 45,  -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 42,  -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18,  1, VIOLET, 56,  -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24,  1, VIOLET, 41,  0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 11,  0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 54,  0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17,  1, VIOLET, 31,  0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

BOSS_HAND_RIGHT_PARAMS = {
    "name": "BossHandRight",
    "x": SCR_W + HF(18),
    "y": -HF(158),
    "health": 250,
    "health_states": ((0, ),),
    "bubbles": {"small": 0, "medium": 5, "big": 3},
    "radius": HF(107),
    "body": scaled_body(BOSS_HAND_BODY),
    "gun_type": 'GunBossHand',
    "angular_vel": 0,
    "body_size": HF(370),
    "trajectory": no_trajectory
}

BOSS_HAND_LEFT_PARAMS = {
    "name": "BossHandLeft",
    "x": -HF(18),
    "y": -HF(158),
    "health": 250,
    "health_states": ((0, ),),
    "bubbles": {"small": 0, "medium": 5, "big": 3},
    "radius": HF(107),
    "body": scaled_body(BOSS_HAND_BODY),
    "gun_type": 'GunBossHand',
    "angular_vel": 0,
    "body_size": HF(370),
    "trajectory": no_trajectory
}

for row in BOSS_HAND_LEFT_PARAMS["body"]:
    row[4] *= -1

BOSS_SKELETON_BODY = [

    [120, 3, PURPLE, 1008, -0.564 * pi, False, 0.0, 0, True, False],
    [120, 3, PURPLE, 1008, -0.436 * pi, False, 0.0, 0, True, False],
    [96,  3, PURPLE, 856,  -0.554 * pi, False, 0.0, 0, True, False],
    [96,  3, PURPLE, 856,  -0.446 * pi, False, 0.0, 0, True, False],
    [104, 3, PURPLE, 720,  -0.536 * pi, False, 0.0, 0, True, False],
    [104, 3, PURPLE, 720,  -0.464 * pi, False, 0.0, 0, True, False],
    [84,  2, PURPLE, 592,  -0.532 * pi, False, 0.0, 0, True, False],
    [84,  2, PURPLE, 592,  -0.468 * pi, False, 0.0, 0, True, False],
    [72,  2, PURPLE, 472,  -0.532 * pi, False, 0.0, 0, True, False],
    [72,  2, PURPLE, 472,  -0.468 * pi, False, 0.0, 0, True, False],
    [100, 3, PURPLE, 344,  -0.5 * pi,   False, 0.0, 0, True, False],
    [86,  2, PURPLE, 216,  -0.5 * pi,   False, 0.0, 0, True, False],
    [80,  2, PURPLE, 96,   -0.5 * pi,   False, 0.0, 0, True, False],
    [68,  2, PURPLE, 9,    0.5 * pi,    False, 0.0, 0, True, False],
    [72,  2, PURPLE, 112,  0.5 * pi,    False, 0.0, 0, True, False],
    [72,  2, PURPLE, 216,  0.5 * pi,    False, 0.0, 0, True, False],
    [80,  2, PURPLE, 320,  0.5 * pi,    False, 0.0, 0, True, False],
    [89,  3, PURPLE, 440,  0.5 * pi,    False, 0.0, 0, True, False],
    [99,  3, PURPLE, 568,  0.5 * pi,    False, 0.0, 0, True, False],
    [84,  2, PURPLE, 656,  0.528 * pi,  False, 0.0, 0, True, False],
    [84,  2, PURPLE, 656,  0.472 * pi,  False, 0.0, 0, True, False],
    [99,  3, PURPLE, 760,  0.5 * pi,    False, 0.0, 0, True, False],
    [72,  2, PURPLE, 784,  0.55 * pi,   False, 0.0, 0, True, False],
    [72,  2, PURPLE, 784,  0.45 * pi,   False, 0.0, 0, True, False],
    [129, 4, PURPLE, 888,  0.5 * pi,    False, 0.0, 0, True, False],
    [96,  3, PURPLE, 912,  0.552 * pi,  False, 0.0, 0, True, False],
    [96,  3, PURPLE, 912,  0.448 * pi,  False, 0.0, 0, True, False],
    [145, 5, PURPLE, 1016, 0.5 * pi,    False, 0.0, 0, True, False],
    [115, 3, PURPLE, 1048, 0.555 * pi,  False, 0.0, 0, True, False],
    [115, 3, PURPLE, 1048, 0.445 * pi,  False, 0.0, 0, True, False],
    [60,  2, BLUE,   1224, 0.541 * pi,  False, 0.0, 0, True, False],
    [60,  2, BLUE,   1224, 0.459 * pi,  False, 0.0, 0, True, False],
    [60,  2, BLUE,   1136, 0.54 * pi,   False, 0.0, 0, True, False],
    [60,  2, BLUE,   1136, 0.46 * pi,   False, 0.0, 0, True, False],
    [49,  2, BLUE,   1200, 0.629 * pi,  False, 0.0, 0, True, False],
    [49,  2, BLUE,   1200, 0.371 * pi,  False, 0.0, 0, True, False],
    [43,  2, BLUE,   1128, 0.629 * pi,  False, 0.0, 0, True, False],
    [43,  2, BLUE,   1128, 0.371 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1192, 0.687 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1192, 0.313 * pi,  False, 0.0, 0, True, False],
    [33,  2, BLUE,   1139, 0.685 * pi,  False, 0.0, 0, True, False],
    [33,  2, BLUE,   1139, 0.315 * pi,  False, 0.0, 0, True, False],
    [40,  2, BLUE,   1192, 0.731 * pi,  False, 0.0, 0, True, False],
    [40,  2, BLUE,   1192, 0.269 * pi,  False, 0.0, 0, True, False],
    [36,  2, BLUE,   1144, 0.731 * pi,  False, 0.0, 0, True, False],
    [36,  2, BLUE,   1144, 0.269 * pi,  False, 0.0, 0, True, False],
    [54,  1, BLUE,   1088, 0.77 * pi,   False, 0.0, 0, True, False],
    [54,  1, BLUE,   1088, 0.23 * pi,   False, 0.0, 0, True, False],
    [70,  1, BLUE,   1032, 0.762 * pi,  False, 0.0, 0, True, False],
    [70,  1, BLUE,   1032, 0.238 * pi,  False, 0.0, 0, True, False],
    [152, 2, BLUE,   1176, 0.58 * pi,   False, 0.0, 0, True, False],
    [152, 2, BLUE,   1176, 0.42 * pi,   False, 0.0, 0, True, False],
    [97,  2, BLUE,   1168, 0.655 * pi,  False, 0.0, 0, True, False],
    [97,  2, BLUE,   1168, 0.345 * pi,  False, 0.0, 0, True, False],
    [78,  2, BLUE,   1168, 0.708 * pi,  False, 0.0, 0, True, False],
    [78,  2, BLUE,   1168, 0.292 * pi,  False, 0.0, 0, True, False],
    [54,  1, BLUE,   1171, 0.747 * pi,  False, 0.0, 0, True, False],
    [54,  1, BLUE,   1171, 0.253 * pi,  False, 0.0, 0, True, False],
    [116, 2, BLUE,   1200, 0.775 * pi,  False, 0.0, 0, True, False],
    [116, 2, BLUE,   1200, 0.225 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1304, 0.76 * pi,   False, 0.0, 0, True, False],
    [41,  2, BLUE,   1304, 0.24 * pi,   False, 0.0, 0, True, False],
    [41,  2, BLUE,   1304, 0.791 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1304, 0.209 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1203, 0.806 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1203, 0.194 * pi,  False, 0.0, 0, True, False],
    [19,  2, BLUE,   1318, 0.561 * pi,  False, 0.0, 0, True, False],
    [19,  2, BLUE,   1318, 0.439 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1329, 0.569 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1329, 0.431 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1336, 0.582 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1336, 0.418 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1388, 0.586 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1388, 0.414 * pi,  False, 0.0, 0, True, False],
    [19,  1, RED,    1425, 0.589 * pi,  False, 0.0, 0, True, False],
    [19,  1, RED,    1425, 0.411 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1376, 0.612 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1376, 0.388 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1419, 0.62 * pi,   False, 0.0, 0, True, False],
    [32,  2, BLUE,   1419, 0.38 * pi,   False, 0.0, 0, True, False],
    [19,  1, RED,    1448, 0.625 * pi,  False, 0.0, 0, True, False],
    [19,  1, RED,    1448, 0.375 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1280, 0.587 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1280, 0.413 * pi,  False, 0.0, 0, True, False],
    [57,  2, BLUE,   1320, 0.6 * pi,    False, 0.0, 0, True, False],
    [57,  2, BLUE,   1320, 0.4 * pi,    False, 0.0, 0, True, False],
    [41,  2, BLUE,   1256, 0.671 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1256, 0.329 * pi,  False, 0.0, 0, True, False],
    [28,  2, BLUE,   1288, 0.679 * pi,  False, 0.0, 0, True, False],
    [28,  2, BLUE,   1288, 0.321 * pi,  False, 0.0, 0, True, False],
    [33,  2, BLUE,   1232, 0.723 * pi,  False, 0.0, 0, True, False],
    [33,  2, BLUE,   1232, 0.277 * pi,  False, 0.0, 0, True, False],
    [22,  2, BLUE,   1260, 0.731 * pi,  False, 0.0, 0, True, False],
    [22,  2, BLUE,   1260, 0.269 * pi,  False, 0.0, 0, True, False],
    [19,  2, BLUE,   1155, 0.586 * pi,  False, 0.0, 0, True, False],
    [19,  2, BLUE,   1155, 0.414 * pi,  False, 0.0, 0, True, False],
    [19,  2, BLUE,   1155, 0.573 * pi,  False, 0.0, 0, True, False],
    [19,  2, BLUE,   1155, 0.427 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1128, 0.565 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1128, 0.435 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1124, 0.594 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1124, 0.406 * pi,  False, 0.0, 0, True, False],
    [49,  1, BLUE,   1080, 0.608 * pi,  False, 0.0, 0, True, False],
    [49,  1, BLUE,   1080, 0.392 * pi,  False, 0.0, 0, True, False],
    [49,  1, BLUE,   1088, 0.551 * pi,  False, 0.0, 0, True, False],
    [49,  1, BLUE,   1088, 0.449 * pi,  False, 0.0, 0, True, False],
    [56,  1, BLUE,   1075, 0.515 * pi,  False, 0.0, 0, True, False],
    [56,  1, BLUE,   1075, 0.485 * pi,  False, 0.0, 0, True, False],
    [136, 2, BLUE,   1208, 0.5 * pi,    False, 0.0, 0, True, False],
    [46,  1, BLUE,   1368, 0.541 * pi,  False, 0.0, 0, True, False],
    [46,  1, BLUE,   1368, 0.459 * pi,  False, 0.0, 0, True, False],
    [46,  1, BLUE,   1432, 0.5 * pi,    False, 0.0, 0, True, False],
    [41,  2, BLUE,   1424, 0.548 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1424, 0.452 * pi,  False, 0.0, 0, True, False],
    [41,  2, BLUE,   1496, 0.5 * pi,    False, 0.0, 0, True, False],
    [32,  2, BLUE,   1472, 0.554 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1472, 0.446 * pi,  False, 0.0, 0, True, False],
    [32,  2, BLUE,   1552, 0.5 * pi,    False, 0.0, 0, True, False],
    [27,  2, BLUE,   1508, 0.558 * pi,  False, 0.0, 0, True, False],
    [27,  2, BLUE,   1508, 0.442 * pi,  False, 0.0, 0, True, False],
    [27,  2, BLUE,   1596, 0.5 * pi,    False, 0.0, 0, True, False],
    [19,  1, RED,    1537, 0.56 * pi,   False, 0.0, 0, True, False],
    [19,  1, RED,    1537, 0.44 * pi,   False, 0.0, 0, True, False],
    [19,  1, RED,    1627, 0.5 * pi,    False, 0.0, 0, True, False],
    [57,  1, BLUE,   1304, 0.532 * pi,  False, 0.0, 0, True, False],
    [57,  1, BLUE,   1304, 0.468 * pi,  False, 0.0, 0, True, False],
    [57,  1, BLUE,   1360, 0.5 * pi,    False, 0.0, 0, True, False],
    [32,  2, BLUE,   1088, 0.5 * pi,    False, 0.0, 0, True, False],
    [32,  2, BLUE,   1208, 0.5 * pi,    False, 0.0, 0, True, False],
    [43,  2, BLUE,   1147, 0.5 * pi,    False, 0.0, 0, True, False],
    [19,  2, BLUE,   1169, 0.512 * pi,  False, 0.0, 0, True, False],
    [19,  2, BLUE,   1169, 0.488 * pi,  False, 0.0, 0, True, False],
    [19,  2, BLUE,   1248, 0.5 * pi,    False, 0.0, 0, True, False],
    [12,  1, RED,    1131, 0.51 * pi,   False, 0.0, 0, True, False],
    [12,  1, RED,    1131, 0.49 * pi,   False, 0.0, 0, True, False],
    [12,  1, RED,    1105, 0.5 * pi,    False, 0.0, 0, True, False],
    [67,  2, BLUE,   1232, -0.535 * pi, False, 0.0, 0, True, False],
    [67,  2, BLUE,   1232, -0.465 * pi, False, 0.0, 0, True, False],
    [96,  2, BLUE,   976,  -0.5 * pi,   False, 0.0, 0, True, False],
    [67,  2, BLUE,   1232, -0.535 * pi, False, 0.0, 0, True, False],
    [67,  2, BLUE,   1232, -0.465 * pi, False, 0.0, 0, True, False],
    [136, 2, BLUE,   1136, -0.56 * pi,  False, 0.0, 0, True, False],
    [136, 2, BLUE,   1136, -0.44 * pi,  False, 0.0, 0, True, False],
    [112, 2, BLUE,   1120, -0.5 * pi,   False, 0.0, 0, True, False],
    [59,  2, BLUE,   1232, -0.59 * pi,  False, 0.0, 0, True, False],
    [59,  2, BLUE,   1232, -0.41 * pi,  False, 0.0, 0, True, False],
    [40,  2, BLUE,   1272, -0.605 * pi, False, 0.0, 0, True, False],
    [40,  2, BLUE,   1272, -0.395 * pi, False, 0.0, 0, True, False],
    [48,  1, BLUE,   1225, -0.5 * pi,   False, 0.0, 0, True, False],
    [41,  2, BLUE,   1299, -0.5 * pi,   False, 0.0, 0, True, False],
    [32,  2, BLUE,   1353, -0.5 * pi,   False, 0.0, 0, True, False],
    [28,  2, BLUE,   1396, -0.5 * pi,   False, 0.0, 0, True, False],
    [22,  1, RED,    1430, -0.5 * pi,   False, 0.0, 0, True, False]

]

TURTLE_BODY =  [

    [31, 3, BLUE,   71,  pi,          True,  0.023, 21, False, False],
    [31, 3, BLUE,   71,  0,           True,  0.023, 21, False, False],
    [31, 3, BLUE,   71,  0.667 * pi,  True,  0.023, 21, False, False],
    [31, 3, BLUE,   71,  -0.667 * pi, True,  0.023, 21, False, False],
    [31, 3, BLUE,   71,  0.25 * pi,   True,  0.023, 21, True,  False],
    [31, 3, BLUE,   71,  0.75 * pi,   True,  0.023, 21, True,  False],
    [31, 3, BLUE,   71,  -0.75 * pi,  True,  0.023, 21, True,  False],
    [31, 3, BLUE,   71,  -0.25 * pi,  True,  0.023, 21, True,  False],
    [21, 2, BLUE,   98,  0,           True,  0.011, 11, True,  False],
    [17, 2, BLUE,   71,  0,           True,  0.011, 11, True,  False],
    [17, 2, BLUE,   96,  0.05 * pi,   True,  0.011, 11, False, False],
    [17, 2, BLUE,   96,  -0.05 * pi,  True,  0.011, 11, False, False],
    [17, 2, BLUE,   105, 0.1 * pi,    True,  0.011, 11, True,  False],
    [17, 2, BLUE,   105, -0.1 * pi,   True,  0.011, 11, True,  False],
    [68, 6, BLUE,   0,   0,           True,  0.057, 42, True,  False],
    [17, 2, BLUE,   73,  0.85 * pi,   True,  0.011, 11, True,  False],
    [17, 2, BLUE,   73,  -0.85 * pi,  True,  0.011, 11, True,  False],
    [17, 2, BLUE,   73,  pi,          True,  0.011, 11, True,  False],
    [14, 1, ORANGE, 0,   0,           True,  0.011, 9,  True,  True,  41, 0.25 * pi],
    [14, 1, ORANGE, 0,   0,           True,  0.011, 9,  True,  True,  41, -0.25 * pi],
    [14, 1, ORANGE, 0,   0,           True,  0.011, 9,  True,  True,  59, 0.167 * pi],
    [14, 1, ORANGE, 0,   0,           True,  0.011, 9,  True,  True,  59, -0.167 * pi],
    [12, 1, ORANGE, 0,   0,           True,  0.011, 9,  True,  True,  78, 0.125 * pi],
    [12, 1, ORANGE, 0,   0,           True,  0.011, 9,  True,  True,  78, -0.125 * pi],
    [8,  1, ORANGE, 0,   0,           True,  0.01,  8,  True,  True,  79, -0.19 * pi],
    [8,  1, ORANGE, 0,   0,           True,  0.01,  8,  True,  True,  79, 0.19 * pi],
    [39, 4, ORANGE, 0,   0,           True,  0.038, 25, True,  True,  0,  0],
    [17, 2, ORANGE, 0,   0,           True,  0.014, 11, True,  True,  42, -1.0 * pi],
    [17, 2, ORANGE, 0,   0,           True,  0.014, 11, True,  True,  42, -0.667 * pi],
    [17, 2, ORANGE, 0,   0,           True,  0.014, 11, True,  True,  42, 0.667 * pi],
    [19, 1, VIOLET, 19,  -0.15 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31,  -0.35 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45,  0.22 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45,  -0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42,  -0.75 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56,  -0.8 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41,  0.82 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11,  0.5 * pi,    False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54,  0.6 * pi,    False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31,  0.65 * pi,   False, 0.0,   0,  False, False, 0,  0]

]

TURTLE_HEALTH_STATES = (
    (21, (0, 4), (10, 12)),
    (20, (0, 4), (8, 9), (12, 14)),
    (19, (0, 4), (10, 14)),
    (18, (0, 4), (8, 9), (10, 14)),
    (17, (0, 4), (8, 9), (10, 14), (17, 18)),
    (14, (0, 4), (8, 9), (10, 14), (15, 17)),
    (11, (0, 4), (8, 9), (10, 14), (15, 18)),
    (7, (0, 1), (4, 14), (15, 18)),
    (4, (0, 2), (4, 14), (15, 18)),
    (3, (1, 14), (15, 18)),
    (2, (0, 14), (15, 18))
)

TURTLE_PARAMS = {
    "name": "Turtle",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 21,
    "health_states": TURTLE_HEALTH_STATES,
    "bubbles": {"small": 6, "medium": 0, "big": 0},
    "radius": HF(76),
    "body": scaled_body(TURTLE_BODY),
    "gun_type": 'GunTurtle',
    "angular_vel": 0.0005,
    "body_size": HF(213),
    "trajectory": epicycloid
}

TURTLE_DAMAGING_PARAMS = {
    "name": 'Turtle_dmg',
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 21,
    "health_states": TURTLE_HEALTH_STATES,
    "bubbles": {"small": 3, "medium": 1, "big": 0},
    "radius": HF(76),
    "body": scaled_body([row for i, row in enumerate(TURTLE_BODY) if i not in range(22, 26)]),
    "gun_type": 'GunTurtleDMG',
    "angular_vel": 0.0005,
    "body_size": HF(213),
    "trajectory": epicycloid
}

TERRORIST_BODY = [

    [56, 2, BLUE,         85,  0.5 * pi,   True,  0.031, 21, True,  False],
    [56, 2, BLUE,         85,  -0.5 * pi,  True,  0.028, 21, True,  False],
    [17, 2, BLUE,         145, -0.59 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,         145, 0.59 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,         145, -0.41 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,         145, 0.41 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,         62,  0.75 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,         62,  -0.75 * pi, False, 0.0,   0,  True,  False],
    [9,  1, ORANGE,       42,  0.2 * pi,   True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       42,  -0.2 * pi,  True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       32,  0.28 * pi,  True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       32,  -0.28 * pi, True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       25,  -0.43 * pi, True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       25,  0.43 * pi,  True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       27,  -0.62 * pi, True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       27,  0.62 * pi,  True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       34,  -0.73 * pi, True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       34,  0.73 * pi,  True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       44,  -0.8 * pi,  True,  0.007, 5,  True,  False],
    [9,  1, ORANGE,       44,  0.8 * pi,   True,  0.007, 5,  True,  False],
    [18, 2, LIGHT_ORANGE, 56,  0.15 * pi,  False, 0.0,   0,  True,  False, 0, 0, True, pi],
    [18, 2, LIGHT_ORANGE, 56,  -0.15 * pi, False, 0.0,   0,  True,  False, 0, 0, True, pi],
    [25, 2, ORANGE,       35,  0,          True,  0.018, 11, True,  False],
    [17, 2, BLUE,         62,  0.25 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,         62,  -0.25 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,         59,  0.12 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,         59,  -0.12 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,         58,  0,          False, 0.0,   0,  True,  False],
    [19, 1, VIOLET,       19,  -0.15 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       31,  -0.35 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       45,  0.22 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       45,  -0.22 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       42,  -0.75 * pi, False, 0.0,   0,  False, False, 0, 0],
    [18, 1, VIOLET,       56,  -0.8 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [24, 1, VIOLET,       41,  0.82 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       11,  0.5 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       54,  0.6 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [17, 1, VIOLET,       31,  0.65 * pi,  False, 0.0,   0,  False, False, 0, 0]

]

TERRORIST_HEALTH_STATES = (
    (18,),
    (14, (2, 6)),
    (8, (2, 8)),
    (4, (2, 23))
)

TERRORIST_PARAMS = {
    "name": "Terrorist",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 18,
    "health_states": TERRORIST_HEALTH_STATES,
    "bubbles": {"small": 9, "medium": 0, "big": 0},
    "radius": HF(100),
    "body": scaled_body(TERRORIST_BODY),
    "gun_type": 'GunTerrorist',
    "angular_vel": 0.00015,
    "body_size": HF(299),
    "trajectory": rose_curve_2
}

BENLADEN_BODY = [

    [11,  1, ORANGE,       122, 0.572 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       122, 0.428 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, 0.564 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, 0.436 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, 0.558 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, 0.442 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, 0.551 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, 0.449 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, 0.546 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, 0.454 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, 0.542 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, 0.458 * pi,  True,  0.01,  7,  True,  False],
    [18,  2, LIGHT_ORANGE, 122, 0.572 * pi,  False, 0.0,   0,  True,  False, 0, 0, True, 0.5 * pi],
    [18,  2, LIGHT_ORANGE, 122, 0.428 * pi,  False, 0.0,   0,  True,  False, 0, 0, True, 0.5 * pi],
    [25,  2, ORANGE,       119, 0.5 * pi,    True,  0.028, 17, True,  False],
    [11,  1, ORANGE,       122, -0.572 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       122, -0.428 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, -0.564 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, -0.436 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, -0.558 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, -0.442 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, -0.551 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, -0.449 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, -0.546 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, -0.454 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, -0.542 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, -0.458 * pi, True,  0.01,  7,  True,  False],
    [18,  2, LIGHT_ORANGE, 122, -0.572 * pi, False, 0.0,   0,  True,  False, 0, 0, True, -0.5 * pi],
    [18,  2, LIGHT_ORANGE, 122, -0.428 * pi, False, 0.0,   0,  True,  False, 0, 0, True, -0.5 * pi],
    [25,  2, ORANGE,       119, -0.5 * pi,   True,  0.028, 17, True,  False],
    [11,  1, ORANGE,       122, 0.322 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       122, 0.178 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, 0.314 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, 0.186 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, 0.308 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, 0.192 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, 0.301 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, 0.199 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, 0.296 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, 0.204 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, 0.292 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, 0.208 * pi,  True,  0.01,  7,  True,  False],
    [18,  2, LIGHT_ORANGE, 122, 0.322 * pi,  False, 0.0,   0,  True,  False, 0, 0, True, 0.25 * pi],
    [18,  2, LIGHT_ORANGE, 122, 0.178 * pi,  False, 0.0,   0,  True,  False, 0, 0, True, 0.25 * pi],
    [25,  2, ORANGE,       119, 0.25 * pi,   True,  0.028, 17, True,  False],
    [11,  1, ORANGE,       122, -0.322 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       122, -0.178 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, -0.314 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, -0.186 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, -0.308 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, -0.192 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, -0.301 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, -0.199 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, -0.296 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, -0.204 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, -0.292 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, -0.208 * pi, True,  0.01,  7,  True,  False],
    [18,  2, LIGHT_ORANGE, 122, -0.322 * pi, False, 0.0,   0,  True,  False, 0, 0, True, -0.25 * pi],
    [18,  2, LIGHT_ORANGE, 122, -0.178 * pi, False, 0.0,   0,  True,  False, 0, 0, True, -0.25 * pi],
    [25,  2, ORANGE,       119, -0.25 * pi,  True,  0.028, 17, True,  False],
    [11,  1, ORANGE,       122, 0.822 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       122, 0.678 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, 0.814 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, 0.686 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, 0.808 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, 0.692 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, 0.801 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, 0.699 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, 0.796 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, 0.704 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, 0.792 * pi,  True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, 0.708 * pi,  True,  0.01,  7,  True,  False],
    [18,  2, LIGHT_ORANGE, 122, 0.822 * pi,  False, 0.0,   0,  True,  False, 0, 0, True, 0.75 * pi],
    [18,  2, LIGHT_ORANGE, 122, 0.678 * pi,  False, 0.0,   0,  True,  False, 0, 0, True, 0.75 * pi],
    [25,  2, ORANGE,       119, 0.75 * pi,   True,  0.028, 17, True,  False],
    [11,  1, ORANGE,       122, -0.822 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       122, -0.678 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, -0.814 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       139, -0.686 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, -0.808 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       156, -0.692 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, -0.801 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       173, -0.699 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, -0.796 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       190, -0.704 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, -0.792 * pi, True,  0.01,  7,  True,  False],
    [11,  1, ORANGE,       207, -0.708 * pi, True,  0.01,  7,  True,  False],
    [18,  2, LIGHT_ORANGE, 122, -0.822 * pi, False, 0.0,   0,  True,  False, 0, 0, True, -0.75 * pi],
    [18,  2, LIGHT_ORANGE, 122, -0.678 * pi, False, 0.0,   0,  True,  False, 0, 0, True, -0.75 * pi],
    [25,  2, ORANGE,       119, -0.75 * pi,  True,  0.028, 17, True,  False],
    [29,  3, BLUE,         147, 0.9 * pi,    True,  0.046, 25, True,  False],
    [29,  3, BLUE,         147, -0.9 * pi,   True,  0.046, 25, True,  False],
    [128, 5, BLUE,         0,   0,           True,  0.071, 51, True,  False],
    [22,  2, BLUE,         142, pi,          True,  0.031, 18, True,  False],
    [17,  1, BLUE,         113, pi,          True,  0.026, 14, True,  False],
    [17,  1, BLUE,         17,  pi,          True,  0.026, 14, True,  False],
    [34,  3, BLUE,         31,  0,           True,  0.044, 25, True,  False],
    [17,  1, BLUE,         31,  0.5 * pi,    True,  0.026, 14, True,  False],
    [17,  1, BLUE,         31,  -0.5 * pi,   True,  0.026, 14, True,  False],
    [19,  1, BLUE,         91,  0,           True,  0.027, 15, True,  False],
    [22,  2, BLUE,         65,  0,           True,  0.031, 18, True,  False],
    [34,  3, BLUE,         130, 0,           True,  0.044, 25, True,  False],
    [17,  1, BLUE,         164, 0.04 * pi,   True,  0.026, 14, True,  False],
    [17,  1, BLUE,         164, -0.04 * pi,  True,  0.026, 14, True,  False],
    [19,  1, VIOLET,       19,  -0.15 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15,  1, VIOLET,       31,  -0.35 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15,  1, VIOLET,       45,  0.22 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [15,  1, VIOLET,       45,  -0.22 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15,  1, VIOLET,       42,  -0.75 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [18,  1, VIOLET,       56,  -0.8 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [24,  1, VIOLET,       41,  0.82 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [15,  1, VIOLET,       11,  0.5 * pi,    False, 0.0,   0,  False, False, 0, 0],
    [15,  1, VIOLET,       54,  0.6 * pi,    False, 0.0,   0,  False, False, 0, 0],
    [17,  1, VIOLET,       31,  0.65 * pi,   False, 0.0,   0,  False, False, 0, 0],

]

BENLADEN_PARAMS = {
    "name": "BenLaden",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 50,
    "health_states": ((0, ),),
    "bubbles": {"small": 20, "medium": 0, "big": 0},
    "radius": HF(128),
    "body": scaled_body(BENLADEN_BODY),
    "gun_type": 'GunBenLaden',
    "angular_vel": 0.00018,
    "body_size": HF(412),
    "trajectory": rose_curve_3
}

ANT_BODY = [

    [24, 2, BLUE,   0,  0,          True,  0.028, 18, True,  True],
    [18, 2, BLUE,   38, 0.74 * pi,  True,  0.014, 8,  True,  False],
    [18, 2, BLUE,   38, -0.74 * pi, True,  0.014, 8,  True,  False],
    [17, 2, BLUE,   34, 0,          True,  0.026, 15, True,  False],
    [14, 1, BLUE,   55, 0.1 * pi,   True,  0.017, 11, True,  False],
    [14, 1, BLUE,   55, -0.1 * pi,  True,  0.017, 11, True,  False],
    [19, 2, ORANGE, 0,  0,          True,  0.036, 21, True,  True],
    [7,  1, ORANGE, 0,  0,          True,  0.014, 7,  True,  True,  25],
    [19, 1, VIOLET, 19, -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31, -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, 0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42, -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56, -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41, 0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11, 0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54, 0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31, 0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

ANT_PARAMS = {
    "name": "Ant",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 4,
    "health_states": ((0, ),),
    "bubbles": {"small": 2, "medium": 0, "big": 0},
    "radius": HF(36),
    "body": scaled_body(ANT_BODY),
    "gun_type": 'GunAnt',
    "angular_vel": 0.0013,
    "body_size": HF(135),
    "trajectory": rose_curve_4
}

SCARAB_BODY = [

    [39, 4, BLUE,   0,  0,          True,  0.043, 31, True,  False],
    [28, 2, ORANGE, 0,  0,          True,  0.04,  25, True,  True],
    [11, 1, ORANGE, 0,  0,          True,  0.02,  11, True,  True,  31],
    [22, 2, BLUE,   54, 0.25 * pi,  True,  0.028, 17, True,  False],
    [22, 2, BLUE,   54, -0.25 * pi, True,  0.028, 17, True,  False],
    [22, 2, BLUE,   54, 0.75 * pi,  True,  0.028, 17, True,  False],
    [22, 2, BLUE,   54, -0.75 * pi, True,  0.028, 17, True,  False],
    [17, 2, BLUE,   51, pi,         True,  0.021, 12, True,  False],
    [19, 1, VIOLET, 19, -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31, -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, 0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42, -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56, -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41, 0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11, 0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54, 0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31, 0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

SCARAB_HEALTH_STATES = (
    (6, ),
    (3, (7, 8))
)

SCARAB_PARAMS = {
    "name": "Scarab",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 6,
    "health_states": SCARAB_HEALTH_STATES,
    "bubbles": {"small": 6, "medium": 0, "big": 0},
    "radius": HF(37),
    "body": scaled_body(SCARAB_BODY),
    "gun_type": 'GunScarab',
    "angular_vel": 0.0007,
    "body_size": HF(128),
    "trajectory": rose_curve_1
}

GULL_BODY = [

    [45, 4, BLUE,   8,  0,          True,  0.043, 28, True,  False],
    [22, 2, BLUE,   56, 0.72 * pi,  True,  0.033, 19, True,  False],
    [22, 2, BLUE,   56, -0.72 * pi, True,  0.033, 19, True,  False],
    [22, 2, BLUE,   56, pi,         True,  0.033, 19, False, False],
    [18, 1, BLUE,   93, 0.72 * pi,  True,  0.027, 15, True,  False],
    [18, 1, BLUE,   93, -0.72 * pi, True,  0.027, 15, True,  False],
    [28, 2, ORANGE, 0,  0,          True,  0.04,  25, True,  True],
    [11, 1, ORANGE, 0,  0,          True,  0.02,  11, True,  True,  32],
    [19, 1, VIOLET, 19, -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31, -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, 0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42, -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56, -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41, 0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11, 0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54, 0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31, 0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

GULL_HEALTH_STATES = (
    (5, (3, 4)),
    (4, (3, 6)),
    (2, (1, 3), (4, 6)),
    (1, (1, 6))
)

GULL_PARAMS = {
    "name": "Gull",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 5,
    "health_states": GULL_HEALTH_STATES,
    "bubbles": {"small": 6, "medium": 0, "big": 0},
    "radius": HF(50),
    "body": scaled_body(GULL_BODY),
    "gun_type": 'GunGull',
    "angular_vel": 0.0007,
    "body_size": HF(171),
    "trajectory": rose_curve_1
}

MOTHER_BODY = [

    [17, 1, BLUE,         200, 0.95 * pi,  True,  0.028, 17, True,  False],
    [19, 2, BLUE,         172, 0.95 * pi,  True,  0.033, 18, True,  False],
    [28, 3, BLUE,         136, 0.95 * pi,  True,  0.04,  22, True,  False],
    [17, 1, BLUE,         194, 0.32 * pi,  True,  0.028, 17, True,  False],
    [19, 2, BLUE,         166, 0.32 * pi,  True,  0.03,  18, True,  False],
    [28, 3, BLUE,         130, 0.32 * pi,  True,  0.04,  22, True,  False],
    [17, 1, BLUE,         206, 0.63 * pi,  True,  0.028, 17, True,  False],
    [19, 2, BLUE,         177, 0.63 * pi,  True,  0.03,  18, True,  False],
    [28, 3, BLUE,         142, 0.63 * pi,  True,  0.04,  22, True,  False],
    [17, 1, BLUE,         184, -0.39 * pi, True,  0.028, 17, True,  False],
    [19, 2, BLUE,         156, -0.4 * pi,  True,  0.03,  18, True,  False],
    [28, 3, BLUE,         120, -0.42 * pi, True,  0.04,  22, True,  False],
    [17, 1, BLUE,         213, -0.76 * pi, True,  0.028, 17, True,  False],
    [19, 2, BLUE,         184, -0.76 * pi, True,  0.033, 18, True,  False],
    [28, 3, BLUE,         149, -0.76 * pi, True,  0.04,  22, True,  False],
    [39, 1, BLUE,         102, 0.23 * pi,  True,  0.028, 17, True,  False],
    [39, 1, BLUE,         92,  0.45 * pi,  True,  0.028, 17, True,  False],
    [39, 1, BLUE,         99,  0.66 * pi,  True,  0.028, 17, True,  False],
    [39, 1, BLUE,         99,  0.87 * pi,  True,  0.028, 17, True,  False],
    [39, 1, BLUE,         99,  -0.94 * pi, True,  0.028, 17, True,  False],
    [39, 1, BLUE,         99,  -0.75 * pi, True,  0.028, 17, True,  False],
    [39, 1, BLUE,         88,  -0.57 * pi, True,  0.028, 17, True,  False],
    [39, 1, BLUE,         89,  -0.37 * pi, True,  0.028, 17, True,  False],
    [39, 1, BLUE,         93,  -0.16 * pi, True,  0.028, 17, True,  False],
    [18, 1, ORANGE,       79,  0.26 * pi,  True,  0.024, 14, True,  False],
    [18, 1, ORANGE,       79,  -0.26 * pi, True,  0.024, 14, True,  False],
    [18, 1, ORANGE,       79,  0.74 * pi,  True,  0.024, 14, True,  False],
    [18, 1, ORANGE,       79,  -0.74 * pi, True,  0.024, 14, True,  False],
    [7,  1, LIGHT_ORANGE, 0,   0,          False, 0.0,   0,  True,  False, 0, 0, False, 0, True, 56, 0],
    [7,  1, LIGHT_ORANGE, 0,   0,          False, 0.0,   0,  True,  False, 0, 0, False, 0, True, 56, 0.65 * pi],
    [19, 1, VIOLET,       19,  -0.15 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       31,  -0.35 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       45,  0.22 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       45,  -0.22 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       42,  -0.75 * pi, False, 0.0,   0,  False, False, 0, 0],
    [18, 1, VIOLET,       56,  -0.8 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [24, 1, VIOLET,       41,  0.82 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       11,  0.5 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET,       54,  0.6 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [17, 1, VIOLET,       31,  0.65 * pi,  False, 0.0,   0,  False, False, 0, 0],

]

MOTHER_HEALTH_STATES = (
    (90, ),
    (60, (0, 1), (3, 4), (6, 7), (9, 10), (12, 13)),
    (30, (0, 2), (3, 5), (6, 8), (9, 11), (12, 14))
)

MOTHER_PARAMS = {
    "name": "Mother",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 90,
    "health_states": MOTHER_HEALTH_STATES,
    "bubbles": {"small": 5, "medium": 0, "big": 1},
    "radius": HF(135),
    "body": scaled_body(MOTHER_BODY),
    "gun_type": 'GunPeaceful',
    "angular_vel": 0.00015,
    "body_size": HF(370),
    "trajectory": rose_curve_1
}

COCKROACH_BODY = [

    [17, 1, BLUE,   31, 0.66 * pi,  True,  0.024, 14, True,  False],
    [17, 1, BLUE,   31, -0.66 * pi, True,  0.024, 14, True,  False],
    [14, 1, BLUE,   55, 0.59 * pi,  True,  0.017, 9,  True,  False],
    [14, 1, BLUE,   55, -0.59 * pi, True,  0.017, 9,  True,  False],
    [18, 1, BLUE,   78, 0.48 * pi,  True,  0.027, 15, True,  False],
    [18, 1, BLUE,   78, -0.48 * pi, True,  0.027, 15, True,  False],
    [14, 1, BLUE,   54, 0.47 * pi,  True,  0.017, 9,  True,  False],
    [14, 1, BLUE,   54, -0.47 * pi, True,  0.017, 9,  True,  False],
    [14, 1, BLUE,   66, 0.39 * pi,  True,  0.017, 9,  True,  False],
    [14, 1, BLUE,   66, -0.39 * pi, True,  0.017, 9,  True,  False],
    [14, 1, BLUE,   72, 0.29 * pi,  True,  0.017, 9,  True,  False],
    [14, 1, BLUE,   72, -0.29 * pi, True,  0.017, 9,  True,  False],
    [14, 1, BLUE,   79, 0.2 * pi,   True,  0.017, 9,  True,  False],
    [14, 1, BLUE,   79, -0.2 * pi,  True,  0.017, 9,  True,  False],
    [25, 2, BLUE,   5,  0,          True,  0.028, 17, True,  False],
    [21, 2, ORANGE, 0,  0,          True,  0.021, 14, True,  True],
    [8,  1, ORANGE, 0,  0,          True,  0.014, 8,  True,  True,  27],
    [19, 1, VIOLET, 19, -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31, -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, 0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42, -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56, -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41, 0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11, 0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54, 0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31, 0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

COCKROACH_HEALTH_STATES = (
    (10, ),
    (9, (12, 14)),
    (7, (4, 6), (12, 14)),
    (5, (4, 6), (10, 14)),
    (3, (2, 14), (15, 17))
)

COCKROACH_PARAMS = {
    "name": "Cockroach",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 10,
    "health_states": COCKROACH_HEALTH_STATES,
    "bubbles": {"small": 5, "medium": 0, "big": 0},
    "radius": HF(64),
    "body": scaled_body(COCKROACH_BODY),
    "gun_type": 'GunCockroach',
    "angular_vel": 0.0013,
    "body_size": HF(156),
    "trajectory": rose_curve_4
}

BOMBERSHOOTER_BODY = [

    [25, 2, BLUE,         54,  0.54 * pi,   True,  0.038, 22, True,  False],
    [25, 2, BLUE,         54,  -0.54 * pi,  True,  0.038, 22, True,  False],
    [25, 2, BLUE,         108, 0.17 * pi,   True,  0.038, 22, True,  False],
    [25, 2, BLUE,         108, -0.17 * pi,  True,  0.038, 22, True,  False],
    [25, 2, BLUE,         38,  0.73 * pi,   True,  0.038, 22, True,  False],
    [25, 2, BLUE,         38,  -0.73 * pi,  True,  0.038, 22, True,  False],
    [25, 2, BLUE,         85,  0.83 * pi,   True,  0.038, 22, True,  False],
    [25, 2, BLUE,         85,  -0.83 * pi,  True,  0.038, 22, True,  False],
    [25, 2, BLUE,         120, 0.9 * pi,    True,  0.038, 22, True,  False],
    [25, 2, BLUE,         120, -0.9 * pi,   True,  0.032, 22, True,  False],
    [15, 1, BLUE,         140, 0.15 * pi,   True,  0.023, 12, True,  False],
    [15, 1, BLUE,         140, -0.15 * pi,  True,  0.023, 12, True,  False],
    [15, 1, BLUE,         115, 0.27 * pi,   True,  0.023, 12, True,  False],
    [15, 1, BLUE,         115, -0.27 * pi,  True,  0.023, 12, True,  False],
    [15, 1, BLUE,         153, 0.91 * pi,   True,  0.023, 12, True,  False],
    [15, 1, BLUE,         153, -0.91 * pi,  True,  0.023, 12, True,  False],
    [15, 1, BLUE,         128, 0.82 * pi,   True,  0.023, 12, True,  False],
    [15, 1, BLUE,         128, -0.82 * pi,  True,  0.023, 12, True,  False],
    [54, 4, BLUE,         42,  0,           True,  0.065, 39, True,  False],
    [27, 2, ORANGE,       42,  0,           True,  0.05,  29, True,  True],
    [12, 1, ORANGE,       42,  0,           True,  0.02,  11, True,  True,  32],
    [11, 1, ORANGE,       46,  0.85 * pi,   True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       46,  -0.85 * pi,  True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       61,  0.888 * pi,  True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       61,  -0.888 * pi, True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       76,  0.91 * pi,   True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       76,  -0.91 * pi,  True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       92,  0.925 * pi,  True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       92,  -0.925 * pi, True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       108, 0.935 * pi,  True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       108, -0.935 * pi, True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       123, 0.944 * pi,  True,  0.01,  7,  True,  False],
    [11, 1, ORANGE,       123, -0.944 * pi, True,  0.01,  7,  True,  False],
    [18, 2, LIGHT_ORANGE, 46,  0.85 * pi,   False, 0.0,   0,  True,  False, 0,  0, True, pi],
    [18, 2, LIGHT_ORANGE, 46,  -0.85 * pi,  False, 0.0,   0,  True,  False, 0,  0, True, pi],
    [19, 2, ORANGE,       42,  pi,          True,  0.027, 17, True,  False],
    [19, 1, VIOLET,       19,  -0.15 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET,       31,  -0.35 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET,       45,  0.22 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET,       45,  -0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET,       42,  -0.75 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET,       56,  -0.8 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET,       41,  0.82 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET,       11,  0.5 * pi,    False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET,       54,  0.6 * pi,    False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET,       31,  0.65 * pi,   False, 0.0,   0,  False, False, 0,  0]

]

BOMBERSHOOTER_HEALTH_STATES = (
    (27, ),
    (24, (16, 18)),
    (21, (12, 14), (16, 18)),
    (18, (10, 18)),
    (12, (2, 4), (10, 18))
)

BOMBERSHOOTER_PARAMS = {
    "name": "BomberShooter",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 27,
    "health_states": BOMBERSHOOTER_HEALTH_STATES,
    "bubbles": {"small": 11, "medium": 0, "big": 0},
    "radius": HF(107),
    "body": scaled_body(BOMBERSHOOTER_BODY),
    "gun_type": 'GunBomberShooter',
    "angular_vel": 0.00045,
    "body_size": HF(384),
    "trajectory": rose_curve_1
}

BUG_BODY = [

    [21, 2, BLUE,   41, 0.5 * pi,   True,  0.026, 15, True,  False],
    [21, 2, BLUE,   41, -0.5 * pi,  True,  0.026, 15, True,  False],
    [14, 1, BLUE,   56, 0.64 * pi,  True,  0.014, 8,  True,  False],
    [14, 1, BLUE,   56, -0.64 * pi, True,  0.014, 8,  True,  False],
    [29, 3, BLUE,   0,  0,          True,  0.034, 21, True,  False],
    [21, 2, BLUE,   38, pi,         True,  0.026, 15, True,  False],
    [24, 2, ORANGE, 0,  0,          True,  0.043, 25, True,  True],
    [9,  1, ORANGE, 0,  0,          True,  0.014, 8,  True,  True,  24],
    [19, 1, VIOLET, 5,  -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31, -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, 0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42, -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56, -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41, 0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11, 0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54, 0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31, 0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

BUG_PARAMS = {
    "name": "Bug",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 5,
    "health_states": ((0, ),),
    "bubbles": {"small": 3, "medium": 0, "big": 0},
    "radius": HF(28),
    "body": scaled_body(BUG_BODY),
    "gun_type": 'GunBug',
    "angular_vel": 0.0007,
    "body_size": HF(121),
    "trajectory": rose_curve_1
}

AMEBA_BODY = [

    [7,  1, BLUE,   36, 0.1 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   30, 0.2 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   25, 0.3 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   26, 0.4 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   32, 0.5 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   38, 0.6 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   39, 0.7 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   34, 0.8 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   28, 0.9 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   25, pi,          False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   28, 1.1 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   34, 1.2 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   39, 1.3 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   38, 1.4 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   32, 1.5 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   26, 1.6 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   25, 1.7 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   30, 1.8 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   36, 1.9 * pi,    False, 0.0,  0,  True,  False],
    [7,  1, BLUE,   39, 2.0 * pi,    False, 0.0,  0,  True,  False],
    [15, 2, BLUE,   15, 0,           True,  0.02, 11, True,  False],
    [15, 2, BLUE,   15, 0.667 * pi,  True,  0.02, 11, True,  False],
    [15, 2, BLUE,   15, -0.667 * pi, True,  0.02, 11, True,  False],
    [19, 1, VIOLET, 19, -0.15 * pi,  False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 31, -0.35 * pi,  False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, 0.22 * pi,   False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, -0.22 * pi,  False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 42, -0.75 * pi,  False, 0.0,  0,  False, False, 0, 0],
    [18, 1, VIOLET, 56, -0.8 * pi,   False, 0.0,  0,  False, False, 0, 0],
    [24, 1, VIOLET, 41, 0.82 * pi,   False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 11, 0.5 * pi,    False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 54, 0.6 * pi,    False, 0.0,  0,  False, False, 0, 0],
    [17, 1, VIOLET, 31, 0.65 * pi,   False, 0.0,  0,  False, False, 0, 0]

]

AMEBA_HEALTH_STATES = (
    (4,),
    (3, (22, 23)),
    (2, (21, 23)),
    (1, (20, 23))
)

AMEBA_PARAMS = {
    "name": "Ameba",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 4,
    "health_states": AMEBA_HEALTH_STATES,
    "bubbles": {"small": 2, "medium": 0, "big": 0},
    "radius": HF(36),
    "body": scaled_body(AMEBA_BODY),
    "gun_type": 'GunPeaceful',
    "angular_vel": 0.0002,
    "body_size": HF(80),
    "trajectory": rose_curve_1
}

CELL_BODY = [

    [8,  1, BLUE,   28, 0.167 * pi, False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 0.333 * pi, False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 0.5 * pi,   False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 0.667 * pi, False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 0.833 * pi, False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, pi,         False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 1.167 * pi, False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 1.333 * pi, False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 1.5 * pi,   False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 1.667 * pi, False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 1.833 * pi, False, 0.0,  0,  True,  False],
    [8,  1, BLUE,   28, 2.0 * pi,   False, 0.0,  0,  True,  False],
    [19, 2, BLUE,   0,  0,          True,  0.02, 11, True,  False],
    [19, 1, VIOLET, 19, -0.15 * pi, False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 31, -0.35 * pi, False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, 0.22 * pi,  False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, -0.22 * pi, False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 42, -0.75 * pi, False, 0.0,  0,  False, False, 0, 0],
    [18, 1, VIOLET, 56, -0.8 * pi,  False, 0.0,  0,  False, False, 0, 0],
    [24, 1, VIOLET, 41, 0.82 * pi,  False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 11, 0.5 * pi,   False, 0.0,  0,  False, False, 0, 0],
    [15, 1, VIOLET, 54, 0.6 * pi,   False, 0.0,  0,  False, False, 0, 0],
    [17, 1, VIOLET, 31, 0.65 * pi,  False, 0.0,  0,  False, False, 0, 0],

]

CELL_HEALTH_STATES = (
    (4,),
    (3, (0, 1), (4, 5), (8, 9)),
    (2, (0, 4), (5, 6), (7, 8), (9, 10), (11, 12)),
    (1, (0, 4), (5, 6), (7, 11))
)

CELL_PARAMS = {
    "name": "Cell",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 4,
    "health_states": CELL_HEALTH_STATES,
    "bubbles": {"small": 3, "medium": 0, "big": 0},
    "radius": HF(21),
    "body": scaled_body(CELL_BODY),
    "gun_type": 'GunPeaceful',
    "angular_vel": 0.00065,
    "body_size": HF(72),
    "trajectory": rose_curve_1
}

INFUSORIA_BODY = [

    [14, 1, BLUE,   36, 0.833 * pi,  True,  0.017, 9,  True,  False],
    [14, 1, BLUE,   36, -0.833 * pi, True,  0.017, 9,  True,  False],
    [25, 2, BLUE,   0,  0,           True,  0.024, 14, True,  False],
    [11, 1, BLUE,   31, 0,           True,  0.011, 7,  True,  False],
    [19, 1, VIOLET, 19, -0.15 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 31, -0.35 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, 0.22 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, -0.22 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 42, -0.75 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [18, 1, VIOLET, 56, -0.8 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [24, 1, VIOLET, 41, 0.82 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 11, 0.5 * pi,    False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 54, 0.6 * pi,    False, 0.0,   0,  False, False, 0, 0],
    [17, 1, VIOLET, 31, 0.65 * pi,   False, 0.0,   0,  False, False, 0, 0]

]

INFUSORIA_HEALTH_STATES = (
    (2,),
    (1, (3, 4))
)

INFUSORIA_PARAMS = {
    "name": "Infusoria",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 2,
    "health_states": INFUSORIA_HEALTH_STATES,
    "bubbles": {"small": 6, "medium": 0, "big": 0},
    "radius": HF(36),
    "body": scaled_body(INFUSORIA_BODY),
    "gun_type": 'GunPeaceful',
    "angular_vel": 0.00045,
    "body_size": HF(100),
    "trajectory": rose_curve_1
}

BABY_BODY = [

    [11, 1, BLUE,   19, 0.8 * pi,   True,  0.014, 8,  True,  False],
    [15, 1, BLUE,   0,  0,          True,  0.018, 11, True,  False],
    [11, 1, BLUE,   19, -0.8 * pi,  True,  0.014, 8,  True,  False],
    [19, 1, VIOLET, 19, -0.15 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 31, -0.35 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, 0.22 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, -0.22 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 42, -0.75 * pi, False, 0.0,   0,  False, False, 0, 0],
    [18, 1, VIOLET, 56, -0.8 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [24, 1, VIOLET, 41, 0.82 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 11, 0.5 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 54, 0.6 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [17, 1, VIOLET, 31, 0.65 * pi,  False, 0.0,   0,  False, False, 0, 0]

]

BABY_PARAMS = {
    "name": "Baby",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 1,
    "health_states": ((0, ),),
    "bubbles": {"small": 1, "medium": 0, "big": 0},
    "radius": HF(21),
    "body": scaled_body(BABY_BODY),
    "gun_type": 'GunPeaceful',
    "angular_vel": 0.0003,
    "body_size": HF(57),
    "trajectory": rose_curve_1
}

BEETLE_BODY = [

    [17, 1, BLUE,   160, 0.075 * pi,  True,  0.028, 17, True,  False],
    [17, 1, BLUE,   160, -0.075 * pi, True,  0.028, 17, True,  False],
    [17, 1, BLUE,   133, 0.06 * pi,   True,  0.028, 17, True,  False],
    [17, 1, BLUE,   133, -0.06 * pi,  True,  0.028, 17, True,  False],
    [17, 1, BLUE,   169, 0.13 * pi,   True,  0.028, 17, True,  False],
    [17, 1, BLUE,   169, -0.13 * pi,  True,  0.028, 17, True,  False],
    [17, 1, BLUE,   173, 0.18 * pi,   True,  0.028, 17, True,  False],
    [17, 1, BLUE,   173, -0.18 * pi,  True,  0.028, 17, True,  False],
    [17, 1, BLUE,   173, 0.23 * pi,   True,  0.028, 17, True,  False],
    [17, 1, BLUE,   173, -0.23 * pi,  True,  0.028, 17, True,  False],
    [17, 1, BLUE,   164, 0.28 * pi,   True,  0.028, 17, True,  False],
    [17, 1, BLUE,   164, -0.28 * pi,  True,  0.028, 17, True,  False],
    [27, 2, BLUE,   118, 0.2 * pi,    True,  0.037, 21, True,  False],
    [27, 2, BLUE,   118, -0.2 * pi,   True,  0.037, 21, True,  False],
    [27, 2, BLUE,   105, 0.74 * pi,   True,  0.037, 21, True,  False],
    [27, 2, BLUE,   105, -0.74 * pi,  True,  0.037, 21, True,  False],
    [27, 2, BLUE,   115, 0.5 * pi,    True,  0.037, 21, True,  False],
    [27, 2, BLUE,   115, -0.5 * pi,   True,  0.037, 21, True,  False],
    [27, 2, BLUE,   76,  0.5 * pi,    True,  0.037, 21, True,  False],
    [27, 2, BLUE,   76,  -0.5 * pi,   True,  0.037, 21, True,  False],
    [65, 2, BLUE,   71,  0,           True,  0.038, 22, True,  False],
    [85, 2, BLUE,   35,  pi,          True,  0.048, 28, True,  False],
    [27, 2, BLUE,   130, 0.82 * pi,   True,  0.037, 21, True,  False],
    [27, 2, BLUE,   130, -0.82 * pi,  True,  0.037, 21, True,  False],
    [27, 2, BLUE,   133, pi,          True,  0.037, 21, True,  False],
    [28, 2, ORANGE, 82,  0,           True,  0.047, 27, True,  True],
    [12, 1, ORANGE, 82,  0,           True,  0.023, 12, True,  True,  35],
    [38, 3, ORANGE, 49,  pi,          True,  0.063, 35, True,  True],
    [15, 1, ORANGE, 49,  pi,          True,  0.024, 14, True,  True,  49],
    [19, 1, VIOLET, 5,   -0.15 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31,  -0.35 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45,  0.22 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45,  -0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42,  -0.75 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56,  -0.8 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41,  0.82 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11,  0.5 * pi,    False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54,  0.6 * pi,    False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31,  0.65 * pi,   False, 0.0,   0,  False, False, 0,  0]

]

BEETLE_HEALTH_STATES = (
    (30, ),
    (27, (10, 12)),
    (24, (8, 12)),
    (21, (6, 12)),
    (18, (4, 12)),
    (15, (0, 12)),
    (12, (0, 14)),
    (6, (0, 21), (25, 27)),
    (3, (0, 21), (24, 27))
)

BEETLE_PARAMS = {
    "name": "Beetle",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 30,
    "health_states": BEETLE_HEALTH_STATES,
    "bubbles": {"small": 9, "medium": 0, "big": 0},
    "radius": HF(100),
    "body": scaled_body(BEETLE_BODY),
    "gun_type": 'GunBeetle',
    "angular_vel": 0.00045,
    "body_size": HF(327),
    "trajectory": rose_curve_1
}

SPREADER_BODY = [

    [19, 2, BLUE,   64, 0.1 * pi,   False, 0.0,   0,  True,  False],
    [19, 2, BLUE,   64, 0.3 * pi,   False, 0.0,   0,  True,  False],
    [19, 2, BLUE,   64, 0.5 * pi,   False, 0.0,   0,  True,  False],
    [19, 2, BLUE,   64, 0.7 * pi,   False, 0.0,   0,  True,  False],
    [19, 2, BLUE,   64, 0.9 * pi,   False, 0.0,   0,  True,  False],
    [19, 2, BLUE,   64, -0.9 * pi,  False, 0.0,   0,  True,  False],
    [19, 2, BLUE,   64, -0.7 * pi,  False, 0.0,   0,  True,  False],
    [19, 2, BLUE,   64, -0.5 * pi,  False, 0.0,   0,  True,  False],
    [19, 2, BLUE,   64, -0.3 * pi,  False, 0.0,   0,  True,  False],
    [19, 2, BLUE,   64, -0.1 * pi,  False, 0.0,   0,  True,  False],
    [61, 2, BLUE,   0,  0,          True,  0.04,  24, True,  False],
    [28, 3, ORANGE, 0,  0,          True,  0.037, 21, True,  True],
    [9,  1, ORANGE, 38, 0,          True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, 0,          True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 38, 0.2 * pi,   True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, 0.2 * pi,   True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 38, 0.4 * pi,   True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, 0.4 * pi,   True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 38, 0.6 * pi,   True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, 0.6 * pi,   True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 38, 0.8 * pi,   True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, 0.8 * pi,   True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 38, pi,         True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, pi,         True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 38, -0.8 * pi,  True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, -0.8 * pi,  True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 38, -0.6 * pi,  True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, -0.6 * pi,  True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 38, -0.4 * pi,  True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, -0.4 * pi,  True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 38, -0.2 * pi,  True,  0.016, 9,  True,  False],
    [9,  1, ORANGE, 54, -0.2 * pi,  True,  0.016, 9,  True,  False],
    [19, 1, VIOLET, 5,  -0.15 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 31, -0.35 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, 0.22 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 45, -0.22 * pi, False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 42, -0.75 * pi, False, 0.0,   0,  False, False, 0, 0],
    [18, 1, VIOLET, 56, -0.8 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [24, 1, VIOLET, 41, 0.82 * pi,  False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 11, 0.5 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [15, 1, VIOLET, 54, 0.6 * pi,   False, 0.0,   0,  False, False, 0, 0],
    [17, 1, VIOLET, 31, 0.65 * pi,  False, 0.0,   0,  False, False, 0, 0]

]

SPREADER_HEALTH_STATES = (
    (18, ),
    (15, (0, 1), (5, 6)),
    (12, (0, 2), (5, 7)),
    (9, (0, 2), (4, 7), (9, 10)),
    (6, (0, 3), (4, 8), (9, 10)),
    (3, (0, 10))
)

SPREADER_PARAMS = {
    "name": "Spreader",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 40,
    "health_states": SPREADER_HEALTH_STATES,
    "bubbles": {"small": 15, "medium": 0, "big": 0},
    "radius": HF(74),
    "body": scaled_body(SPREADER_BODY),
    "gun_type": 'GunSpreader',
    "angular_vel": 0.00015,
    "body_size": HF(156),
    "trajectory": rose_curve_1
}

BIGEGG_BODY = [

    [113, 5, RED,    0,  0,          True,  0.014, 8,  True,  False],
    [61,  2, BLUE,   0,  0,          True,  0.04,  24, True,  True],
    [28,  3, ORANGE, 0,  0,          True,  0.037, 21, True,  True],
    [11,  1, ORANGE, 0,  0,          True,  0.016, 9,  True,  True,  38],
    [19,  1, VIOLET, 5,  -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 31, -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 45, 0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 45, -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 42, -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18,  1, VIOLET, 56, -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24,  1, VIOLET, 41, 0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 11, 0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15,  1, VIOLET, 54, 0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17,  1, VIOLET, 31, 0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

BIGEGG_PARAMS = {
    "name": "BigEgg",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 50,
    "health_states": ((0, ),),
    "bubbles": {"small": 15, "medium": 0, "big": 0},
    "radius": HF(107),
    "body": scaled_body(BIGEGG_BODY),
    "gun_type": 'GunBigEgg',
    "angular_vel": 0.0006,
    "body_size": HF(213),
    "trajectory": rose_curve_2
}

SPIDER_BODY = [

    [32, 3, BLUE,   143, 0.5 * pi,   True,  0.046, 27, True,  False],
    [32, 3, BLUE,   143, -0.5 * pi,  True,  0.046, 27, True,  False],
    [32, 3, BLUE,   173, 0.79 * pi,  True,  0.046, 27, True,  False],
    [32, 3, BLUE,   173, -0.79 * pi, True,  0.046, 27, True,  False],
    [32, 3, BLUE,   147, 0.23 * pi,  True,  0.046, 27, True,  False],
    [32, 3, BLUE,   147, -0.23 * pi, True,  0.046, 27, True,  False],
    [32, 3, BLUE,   106, 0,          True,  0.046, 27, True,  False],
    [25, 2, BLUE,   99,  0.5 * pi,   True,  0.037, 21, True,  False],
    [25, 2, BLUE,   99,  -0.5 * pi,  True,  0.037, 21, True,  False],
    [25, 2, BLUE,   105, 0.2 * pi,   True,  0.037, 21, True,  False],
    [25, 2, BLUE,   105, -0.2 * pi,  True,  0.037, 21, True,  False],
    [51, 1, BLUE,   49,  0.28 * pi,  True,  0.034, 19, True,  False],
    [51, 1, BLUE,   49,  -0.28 * pi, True,  0.034, 19, True,  False],
    [36, 1, BLUE,   17,  0,          True,  0.028, 17, True,  False],
    [99, 3, BLUE,   99,  pi,         True,  0.078, 46, True,  False],
    [15, 1, BLUE,   91,  0.45 * pi,  True,  0.024, 14, True,  False],
    [15, 1, BLUE,   91,  -0.45 * pi, True,  0.024, 14, True,  False],
    [15, 1, BLUE,   105, 0.3 * pi,   True,  0.024, 14, True,  False],
    [15, 1, BLUE,   105, -0.3 * pi,  True,  0.024, 14, True,  False],
    [32, 3, BLUE,   116, -0.63 * pi, True,  0.046, 27, False, False],
    [32, 3, BLUE,   116, 0.63 * pi,  True,  0.046, 27, False, False],
    [99, 3, BLUE,   2,   pi,         True,  0.078, 46, False, False],
    [15, 1, ORANGE, 99,  pi,         True,  0.02,  11, True,  True,  48, -0.2 * pi],
    [15, 1, ORANGE, 99,  pi,         True,  0.02,  11, True,  True,  48, 0.2 * pi],
    [15, 1, ORANGE, 99,  pi,         True,  0.02,  11, True,  True,  71, -0.13 * pi],
    [15, 1, ORANGE, 99,  pi,         True,  0.02,  11, True,  True,  71, 0.13 * pi],
    [42, 4, ORANGE, 99,  pi,         True,  0.054, 32, True,  True],
    [17, 1, ORANGE, 99,  pi,         True,  0.024, 14, True,  True,  54, -0.78 * pi],
    [17, 1, ORANGE, 99,  pi,         True,  0.024, 14, True,  True,  54, 0.78 * pi],
    [27, 3, ORANGE, 36,  0,          True,  0.037, 21, True,  True],
    [11, 1, ORANGE, 36,  0,          True,  0.016, 9,  True,  True,  34],
    [19, 1, VIOLET, 5,   -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31,  -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45,  0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45,  -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42,  -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56,  -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41,  0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11,  0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54,  0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31,  0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

SPIDER_HEALTH_STATES = (
    (130, (19, 22)),
    (70, (0, 4), (7, 9), (11, 19), (29, 31)),
    (50, (0, 6), (7, 9), (11, 19), (29, 31)),
    (35, (0, 6), (7, 19), (29, 31)),
    (20, (0, 19), (29, 31))
)

SPIDER_PARAMS = {
    "name": "Spider",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 130,
    "health_states": SPIDER_HEALTH_STATES,
    "bubbles": {"small": 12, "medium": 0, "big": 0},
    "radius": HF(124),
    "body": scaled_body(SPIDER_BODY),
    "gun_type": 'GunSpider',
    "angular_vel": 0.00045,
    "body_size": HF(327),
    "trajectory": rose_curve_2
}

MACHINEGUNNER_BODY = [

    [14, 1, BLUE,   89, 0.07 * pi,  True,  0.018, 11, True,  False],
    [14, 1, BLUE,   89, -0.07 * pi, True,  0.018, 11, True,  False],
    [22, 2, BLUE,   62, 0,          True,  0.031, 18, True,  False],
    [25, 2, BLUE,   52, 0.72 * pi,  True,  0.037, 21, True,  False],
    [25, 2, BLUE,   52, -0.72 * pi, True,  0.037, 21, True,  False],
    [54, 2, BLUE,   0,  0,          True,  0.05,  28, True,  False],
    [17, 1, BLUE,   91, 0.72 * pi,  True,  0.023, 14, True,  False],
    [17, 1, BLUE,   91, -0.72 * pi, True,  0.023, 14, True,  False],
    [17, 1, BLUE,   58, pi,         True,  0.023, 14, True,  False],
    [25, 3, ORANGE, 0,  0,          True,  0.037, 19, True,  True],
    [11, 1, ORANGE, 0,  0,          True,  0.016, 9,  True,  True,  32],
    [14, 1, ORANGE, 0,  0,          True,  0.018, 11, True,  True,  35, 0.77 * pi],
    [14, 1, ORANGE, 0,  0,          True,  0.018, 11, True,  True,  35, -0.77 * pi],
    [19, 1, VIOLET, 5,  -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31, -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, 0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45, -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42, -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56, -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41, 0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11, 0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54, 0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31, 0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

MACHINEGUNNER_HEALTH_STATES = (
    (50, ),
    (35, (8, 9)),
    (25, (6, 8)),
    (15, (6, 9)),
    (5, (0, 2), (6, 9))
)

MACHINEGUNNER_PARAMS = {
    "name": "MachineGunner",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 50,
    "health_states": MACHINEGUNNER_HEALTH_STATES,
    "bubbles": {"small": 12, "medium": 0, "big": 0},
    "radius": HF(78),
    "body": scaled_body(MACHINEGUNNER_BODY),
    "gun_type": 'GunMachineGunner',
    "angular_vel": 0.0008,
    "body_size": HF(185),
    "trajectory": rose_curve_2
}

TURRET_BODY = [

    [17, 2, BLUE,   159, 0.41 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   159, -0.41 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   159, 0.59 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   159, -0.59 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   159, 0.09 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   159, -0.09 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   159, 0.91 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   159, -0.91 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   140, 0.07 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   140, -0.07 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   140, 0.93 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   140, -0.93 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   140, 0.43 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   140, -0.43 * pi, False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   140, 0.57 * pi,  False, 0.0,   0,  True,  False],
    [17, 2, BLUE,   140, -0.57 * pi, False, 0.0,   0,  True,  False],
    [36, 3, BLUE,   102, 0,          True,  0.053, 31, True,  False],
    [36, 3, BLUE,   102, 0.5 * pi,   True,  0.053, 31, True,  False],
    [36, 3, BLUE,   102, -0.5 * pi,  True,  0.053, 31, True,  False],
    [36, 3, BLUE,   102, pi,         True,  0.053, 31, True,  False],
    [99, 3, BLUE,   0,   0,          True,  0.057, 38, True,  False],
    [45, 1, BLUE,   0,   0,          True,  0.044, 25, True,  False],
    [8,  1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  31, 0.23 * pi],
    [8,  1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  31, -0.23 * pi],
    [8,  1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  39, 0.13 * pi],
    [8,  1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  39, -0.13 * pi],
    [8,  1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  48, 0.06 * pi],
    [8,  1, ORANGE, 0,   0,          True,  0.014, 8,  True,  True,  48, -0.06 * pi],
    [28, 3, ORANGE, 0,   0,          True,  0.037, 21, True,  True],
    [12, 1, ORANGE, 0,   0,          True,  0.018, 11, True,  True,  59],
    [19, 1, VIOLET, 5,   -0.15 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 31,  -0.35 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45,  0.22 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 45,  -0.22 * pi, False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 42,  -0.75 * pi, False, 0.0,   0,  False, False, 0,  0],
    [18, 1, VIOLET, 56,  -0.8 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [24, 1, VIOLET, 41,  0.82 * pi,  False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 11,  0.5 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [15, 1, VIOLET, 54,  0.6 * pi,   False, 0.0,   0,  False, False, 0,  0],
    [17, 1, VIOLET, 31,  0.65 * pi,  False, 0.0,   0,  False, False, 0,  0]

]

TURRET_PARAMS = {
    "name": "Turret",
    "x": SCR_W2,
    "y": SCR_H2,
    "health": 55,
    "health_states": ((0, ),),
    "bubbles": {"small": 18, "medium": 0, "big": 0},
    "radius": HF(102),
    "body": scaled_body(TURRET_BODY),
    "gun_type": 'GunTurret',
    "angular_vel": 0,
    "body_size": HF(327),
    "trajectory": no_trajectory
}


__all__ = [

    "BOSS_SKELETON_BODY",
    "BOSS_HEAD_PARAMS",
    "BOSS_HAND_LEFT_PARAMS",
    "BOSS_HAND_RIGHT_PARAMS",
    "BOSS_LEG_PARAMS",
    "TURTLE_PARAMS",
    "TURTLE_DAMAGING_PARAMS",
    "TERRORIST_PARAMS",
    "BENLADEN_PARAMS",
    "ANT_PARAMS",
    "SCARAB_PARAMS",
    "GULL_PARAMS",
    "MOTHER_PARAMS",
    "COCKROACH_PARAMS",
    "BOMBERSHOOTER_PARAMS",
    "BUG_PARAMS",
    "AMEBA_PARAMS",
    "CELL_PARAMS",
    "INFUSORIA_PARAMS",
    "BABY_PARAMS",
    "BEETLE_PARAMS",
    "SPREADER_PARAMS",
    "BIGEGG_PARAMS",
    "SPIDER_PARAMS",
    "MACHINEGUNNER_PARAMS",
    "TURRET_PARAMS"

]

#print_pretty(TURTLE_BODY, scale=1)

from math import pi

from .constants import *
from components.utils import *


frozen_body = [

    [19,  1, VIOLET, 19,  -0.15 * pi],
    [15,  1, VIOLET, 31,  -0.35 * pi],
    [15,  1, VIOLET, 45,  0.22 * pi],
    [15,  1, VIOLET, 45,  -0.22 * pi],
    [15,  1, VIOLET, 42,  -0.75 * pi],
    [18,  1, VIOLET, 56,  -0.8 * pi],
    [24,  1, VIOLET, 41,  0.82 * pi],
    [15,  1, VIOLET, 11,  0.5 * pi],
    [15,  1, VIOLET, 54,  0.6 * pi],
    [17,  1, VIOLET, 31,  0.65 * pi]

]

FROZEN_BODY = scaled_body(frozen_body)


BOSS_HEAD_BODY = [
    [68,  2, BLUE,   1,   0,           True,  25],
    [49,  5, BLUE,   327, 0.055 * pi,  True,  45],
    [49,  5, BLUE,   327, -0.055 * pi, True,  45],
    [31,  3, BLUE,   391, 0.045 * pi,  True,  29],
    [31,  3, BLUE,   391, -0.045 * pi, True,  29],
    [55,  2, BLUE,   270, 0,           True,  24],
    [116, 5, BLUE,   128, 0,           True,  42],
    [31,  3, BLUE,   14,  0,           True,  31],
    [31,  3, BLUE,   135, 0.31 * pi,   True,  31],
    [31,  3, BLUE,   135, -0.31 * pi,  True,  31],
    [51,  2, BLUE,   213, 0.22 * pi,   True,  21],
    [51,  2, BLUE,   213, -0.22 * pi,  True,  21],
    [36,  4, BLUE,   274, 0.225 * pi,  True,  34],
    [36,  4, BLUE,   274, -0.225 * pi, True,  34],
    [21,  2, BLUE,   312, 0.21 * pi,   True,  19],
    [21,  2, BLUE,   312, -0.21 * pi,  True,  19],
    [14,  2, ORANGE, 113, 0,           False, 0,  True, 39, 0.26 * pi],
    [14,  2, ORANGE, 113, 0,           False, 0,  True, 39, -0.26 * pi],
    [14,  2, ORANGE, 113, 0,           False, 0,  True, 48, 0.16 * pi],
    [14,  2, ORANGE, 113, 0,           False, 0,  True, 48, -0.16 * pi],
    [14,  2, ORANGE, 113, 0,           False, 0,  True, 59, 0.065 * pi],
    [14,  2, ORANGE, 113, 0,           False, 0,  True, 59, -0.065 * pi],
    [21,  2, ORANGE, 113, 0,           False, 0,  True, 81, 0],
    [42,  4, ORANGE, 113, 0,           False, 0,  True, 1,  0],
    [14,  2, ORANGE, 298, 0,           True,  13, True, 41, 0.25 * pi],
    [14,  2, ORANGE, 298, 0,           True,  13, True, 41, -0.25 * pi],
    [14,  2, ORANGE, 298, 0,           True,  13, True, 59, 0.167 * pi],
    [14,  2, ORANGE, 298, 0,           True,  13, True, 59, -0.167 * pi],
    [12,  1, ORANGE, 298, 0,           True,  12, True, 78, 0.125 * pi],
    [12,  1, ORANGE, 298, 0,           True,  12, True, 78, -0.125 * pi],
    [8,   1, ORANGE, 298, 0,           True,  8,  True, 79, -0.19 * pi],
    [8,   1, ORANGE, 298, 0,           True,  8,  True, 79, 0.19 * pi],
    [39,  4, ORANGE, 298, 0,           True,  36, True, 1,  0],
    [17,  2, ORANGE, 298, 0,           True,  16, True, 42, -1.0 * pi],
    [17,  2, ORANGE, 298, 0,           True,  16, True, 42, -0.667 * pi],
    [17,  2, ORANGE, 298, 0,           True,  16, True, 42, 0.667 * pi]

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

    [58, 2, BLUE,         85,  0.75 * pi,  True,  24],
    [58, 2, BLUE,         85,  0.25 * pi,  True,  24],
    [34, 3, BLUE,         142, 0.66 * pi,  True,  31],
    [34, 3, BLUE,         142, 0.34 * pi,  True,  31],
    [85, 3, BLUE,         28,  1.5 * pi,   True,  34],
    [34, 3, BLUE,         113, 1.16 * pi,  True,  31],
    [34, 3, BLUE,         113, -0.16 * pi, True,  31],
    [25, 3, BLUE,         156, 1.16 * pi,  True,  22],
    [25, 3, BLUE,         156, -0.16 * pi, True,  22],
    [19, 2, BLUE,         190, 1.16 * pi,  True,  17],
    [19, 2, BLUE,         190, -0.16 * pi, True,  17],
    [8,  1, ORANGE,       174, 0.63 * pi,  True,  8],
    [8,  1, ORANGE,       174, 0.37 * pi,  True,  8],
    [8,  1, ORANGE,       209, 0.635 * pi, True,  8],
    [8,  1, ORANGE,       209, 0.365 * pi, True,  8],
    [8,  1, ORANGE,       197, 0.585 * pi, True,  8],
    [8,  1, ORANGE,       197, 0.415 * pi, True,  8],
    [8,  1, ORANGE,       246, 0.635 * pi, True,  8],
    [8,  1, ORANGE,       246, 0.365 * pi, True,  8],
    [8,  1, ORANGE,       227, 0.554 * pi, True,  8],
    [8,  1, ORANGE,       227, 0.446 * pi, True,  8],
    [14, 2, ORANGE,       227, 0.64 * pi,  True,  14],
    [14, 2, ORANGE,       227, 0.36 * pi,  True,  14],
    [14, 2, ORANGE,       209, 0.563 * pi, True,  14],
    [14, 2, ORANGE,       209, 0.437 * pi, True,  14],
    [14, 2, ORANGE,       256, 0.617 * pi, True,  14],
    [14, 2, ORANGE,       256, 0.383 * pi, True,  14],
    [14, 2, ORANGE,       243, 0.562 * pi, True,  14],
    [14, 2, ORANGE,       243, 0.438 * pi, True,  14],
    [15, 1, ORANGE,       193, 0.615 * pi, True,  14],
    [15, 2, ORANGE,       193, 0.385 * pi, True,  14],
    [16, 2, LIGHT_ORANGE, 200, 0.69 * pi,  False, 0,  False, 0, 0, True, 0,  86],
    [16, 2, LIGHT_ORANGE, 200, 0.31 * pi,  False, 0,  False, 0, 0, True, pi, 86]

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

    [128, 5, BLUE,   0,   0,          True,  42],
    [31,  3, BLUE,   142, -0.02 * pi, True,  31],
    [31,  3, BLUE,   142, 0.46 * pi,  True,  31],
    [48,  4, BLUE,   149, 0.96 * pi,  True,  45],
    [48,  4, BLUE,   149, -0.53 * pi, True,  45],
    [48,  4, BLUE,   149, -0.79 * pi, True,  45],
    [29,  3, ORANGE, 0,   0,          True,  28, True,  5,  0],
    [14,  2, ORANGE, 0,   0,          True,  13, True,  36, 0.68 * pi],
    [14,  2, ORANGE, 0,   0,          True,  13, True,  36, -0.68 * pi],
    [14,  2, ORANGE, 0,   0,          True,  13, True,  36, pi],
    [8,   0, ORANGE, 0,   0,          True,  8,  True,  32, 0],
    [8,   0, ORANGE, 0,   0,          True,  8,  True,  45, 0],
    [8,   0, ORANGE, 0,   0,          True,  8,  True,  41, 0.22 * pi],
    [8,   0, ORANGE, 0,   0,          True,  8,  True,  41, -0.22 * pi],
    [8,   0, ORANGE, 0,   0,          True,  8,  True,  52, 0.17 * pi],
    [8,   0, ORANGE, 0,   0,          True,  8,  True,  52, -0.17 * pi]

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
    row[4] = pi - row[4]

BOSS_SKELETON_BODY = [
    [120, 3, PURPLE, 1008, -0.564 * pi],
    [120, 3, PURPLE, 1008, -0.436 * pi],
    [96,  3, PURPLE, 856,  -0.554 * pi],
    [96,  3, PURPLE, 856,  -0.446 * pi],
    [104, 3, PURPLE, 720,  -0.536 * pi],
    [104, 3, PURPLE, 720,  -0.464 * pi],
    [84,  2, PURPLE, 592,  -0.532 * pi],
    [84,  2, PURPLE, 592,  -0.468 * pi],
    [72,  2, PURPLE, 472,  -0.532 * pi],
    [72,  2, PURPLE, 472,  -0.468 * pi],
    [100, 3, PURPLE, 344,  -0.5 * pi],
    [86,  3, PURPLE, 216,  -0.5 * pi],
    [80,  2, PURPLE, 96,   -0.5 * pi],
    [68,  2, PURPLE, 9,    0.5 * pi],
    [72,  2, PURPLE, 112,  0.5 * pi],
    [72,  2, PURPLE, 216,  0.5 * pi],
    [80,  2, PURPLE, 320,  0.5 * pi],
    [89,  3, PURPLE, 440,  0.5 * pi],
    [99,  3, PURPLE, 568,  0.5 * pi],
    [84,  3, PURPLE, 656,  0.528 * pi],
    [84,  3, PURPLE, 656,  0.472 * pi],
    [99,  3, PURPLE, 760,  0.5 * pi],
    [72,  2, PURPLE, 784,  0.55 * pi],
    [72,  2, PURPLE, 784,  0.45 * pi],
    [129, 4, PURPLE, 888,  0.5 * pi],
    [96,  3, PURPLE, 912,  0.552 * pi],
    [96,  3, PURPLE, 912,  0.448 * pi],
    [145, 5, PURPLE, 1016, 0.5 * pi],
    [115, 3, PURPLE, 1048, 0.555 * pi],
    [115, 3, PURPLE, 1048, 0.445 * pi],
    [60,  2, BLUE,   1224, 0.541 * pi],
    [60,  2, BLUE,   1224, 0.459 * pi],
    [60,  2, BLUE,   1136, 0.54 * pi],
    [60,  2, BLUE,   1136, 0.46 * pi],
    [49,  2, BLUE,   1200, 0.629 * pi],
    [49,  2, BLUE,   1200, 0.371 * pi],
    [43,  2, BLUE,   1128, 0.629 * pi],
    [43,  2, BLUE,   1128, 0.371 * pi],
    [41,  2, BLUE,   1192, 0.687 * pi],
    [41,  2, BLUE,   1192, 0.313 * pi],
    [33,  2, BLUE,   1139, 0.685 * pi],
    [33,  2, BLUE,   1139, 0.315 * pi],
    [40,  2, BLUE,   1192, 0.731 * pi],
    [40,  2, BLUE,   1192, 0.269 * pi],
    [36,  2, BLUE,   1144, 0.731 * pi],
    [36,  2, BLUE,   1144, 0.269 * pi],
    [54,  2, BLUE,   1088, 0.77 * pi],
    [54,  2, BLUE,   1088, 0.23 * pi],
    [70,  2, BLUE,   1032, 0.762 * pi],
    [70,  2, BLUE,   1032, 0.238 * pi],
    [152, 3, BLUE,   1176, 0.58 * pi],
    [152, 3, BLUE,   1176, 0.42 * pi],
    [97,  3, BLUE,   1168, 0.655 * pi],
    [97,  3, BLUE,   1168, 0.345 * pi],
    [78,  2, BLUE,   1168, 0.708 * pi],
    [78,  2, BLUE,   1168, 0.292 * pi],
    [54,  2, BLUE,   1171, 0.747 * pi],
    [54,  2, BLUE,   1171, 0.253 * pi],
    [116, 3, BLUE,   1200, 0.775 * pi],
    [116, 3, BLUE,   1200, 0.225 * pi],
    [41,  2, BLUE,   1304, 0.76 * pi],
    [41,  2, BLUE,   1304, 0.24 * pi],
    [41,  2, BLUE,   1304, 0.791 * pi],
    [41,  2, BLUE,   1304, 0.209 * pi],
    [41,  2, BLUE,   1203, 0.806 * pi],
    [41,  2, BLUE,   1203, 0.194 * pi],
    [19,  2, BLUE,   1318, 0.561 * pi],
    [19,  2, BLUE,   1318, 0.439 * pi],
    [32,  2, BLUE,   1329, 0.569 * pi],
    [32,  2, BLUE,   1329, 0.431 * pi],
    [41,  2, BLUE,   1336, 0.582 * pi],
    [41,  2, BLUE,   1336, 0.418 * pi],
    [32,  2, BLUE,   1388, 0.586 * pi],
    [32,  2, BLUE,   1388, 0.414 * pi],
    [19,  2, RED,    1425, 0.589 * pi],
    [19,  2, RED,    1425, 0.411 * pi],
    [41,  2, BLUE,   1376, 0.612 * pi],
    [41,  2, BLUE,   1376, 0.388 * pi],
    [32,  2, BLUE,   1419, 0.62 * pi],
    [32,  2, BLUE,   1419, 0.38 * pi],
    [19,  2, RED,    1448, 0.625 * pi],
    [19,  2, RED,    1448, 0.375 * pi],
    [41,  2, BLUE,   1280, 0.587 * pi],
    [41,  2, BLUE,   1280, 0.413 * pi],
    [57,  2, BLUE,   1320, 0.6 * pi],
    [57,  2, BLUE,   1320, 0.4 * pi],
    [41,  2, BLUE,   1256, 0.671 * pi],
    [41,  2, BLUE,   1256, 0.329 * pi],
    [28,  2, BLUE,   1288, 0.679 * pi],
    [28,  2, BLUE,   1288, 0.321 * pi],
    [33,  2, BLUE,   1232, 0.723 * pi],
    [33,  2, BLUE,   1232, 0.277 * pi],
    [22,  2, BLUE,   1260, 0.731 * pi],
    [22,  2, BLUE,   1260, 0.269 * pi],
    [19,  2, BLUE,   1155, 0.586 * pi],
    [19,  2, BLUE,   1155, 0.414 * pi],
    [19,  2, BLUE,   1155, 0.573 * pi],
    [19,  2, BLUE,   1155, 0.427 * pi],
    [32,  2, BLUE,   1128, 0.565 * pi],
    [32,  2, BLUE,   1128, 0.435 * pi],
    [32,  2, BLUE,   1124, 0.594 * pi],
    [32,  2, BLUE,   1124, 0.406 * pi],
    [49,  2, BLUE,   1080, 0.608 * pi],
    [49,  2, BLUE,   1080, 0.392 * pi],
    [49,  2, BLUE,   1088, 0.551 * pi],
    [49,  2, BLUE,   1088, 0.449 * pi],
    [56,  2, BLUE,   1075, 0.515 * pi],
    [56,  2, BLUE,   1075, 0.485 * pi],
    [136, 3, BLUE,   1208, 0.5 * pi],
    [46,  2, BLUE,   1368, 0.541 * pi],
    [46,  2, BLUE,   1368, 0.459 * pi],
    [46,  2, BLUE,   1432, 0.5 * pi],
    [41,  2, BLUE,   1424, 0.548 * pi],
    [41,  2, BLUE,   1424, 0.452 * pi],
    [41,  2, BLUE,   1496, 0.5 * pi],
    [32,  2, BLUE,   1472, 0.554 * pi],
    [32,  2, BLUE,   1472, 0.446 * pi],
    [32,  2, BLUE,   1552, 0.5 * pi],
    [27,  2, BLUE,   1508, 0.558 * pi],
    [27,  2, BLUE,   1508, 0.442 * pi],
    [27,  2, BLUE,   1596, 0.5 * pi],
    [19,  2, RED,    1537, 0.56 * pi],
    [19,  2, RED,    1537, 0.44 * pi],
    [19,  2, RED,    1627, 0.5 * pi],
    [57,  2, BLUE,   1304, 0.532 * pi],
    [57,  2, BLUE,   1304, 0.468 * pi],
    [57,  2, BLUE,   1360, 0.5 * pi],
    [32,  2, BLUE,   1088, 0.5 * pi],
    [32,  2, BLUE,   1208, 0.5 * pi],
    [43,  2, BLUE,   1147, 0.5 * pi],
    [19,  2, BLUE,   1169, 0.512 * pi],
    [19,  2, BLUE,   1169, 0.488 * pi],
    [19,  2, BLUE,   1248, 0.5 * pi],
    [12,  1, RED,    1131, 0.51 * pi],
    [12,  1, RED,    1131, 0.49 * pi],
    [12,  1, RED,    1105, 0.5 * pi],
    [67,  2, BLUE,   1232, -0.535 * pi],
    [67,  2, BLUE,   1232, -0.465 * pi],
    [96,  3, BLUE,   976,  -0.5 * pi],
    [67,  2, BLUE,   1232, -0.535 * pi],
    [67,  2, BLUE,   1232, -0.465 * pi],
    [136, 3, BLUE,   1136, -0.56 * pi],
    [136, 3, BLUE,   1136, -0.44 * pi],
    [112, 3, BLUE,   1120, -0.5 * pi],
    [59,  2, BLUE,   1232, -0.59 * pi],
    [59,  2, BLUE,   1232, -0.41 * pi],
    [40,  2, BLUE,   1272, -0.605 * pi],
    [40,  2, BLUE,   1272, -0.395 * pi],
    [48,  2, BLUE,   1225, -0.5 * pi],
    [41,  2, BLUE,   1299, -0.5 * pi],
    [32,  2, BLUE,   1353, -0.5 * pi],
    [28,  2, BLUE,   1396, -0.5 * pi],
    [22,  2, RED,    1430, -0.5 * pi]

]

TURTLE_BODY = [
    [31, 3, BLUE,   71,  pi,          True, 24],
    [31, 3, BLUE,   71,  0,           True, 24],
    [31, 3, BLUE,   71,  0.667 * pi,  True, 24],
    [31, 3, BLUE,   71,  -0.667 * pi, True, 24],
    [31, 3, BLUE,   71,  0.25 * pi,   True, 24],
    [31, 3, BLUE,   71,  0.75 * pi,   True, 23],
    [31, 3, BLUE,   71,  -0.75 * pi,  True, 23],
    [31, 3, BLUE,   71,  -0.25 * pi,  True, 23],
    [21, 2, BLUE,   98,  0,           True, 11],
    [17, 2, BLUE,   71,  0,           True, 15],
    [17, 2, BLUE,   96,  0.05 * pi,   True, 15],
    [17, 2, BLUE,   96,  -0.05 * pi,  True, 15],
    [17, 2, BLUE,   105, 0.1 * pi,    True, 15],
    [17, 2, BLUE,   105, -0.1 * pi,   True, 15],
    [68, 6, BLUE,   0,   0,           True, 42],
    [17, 2, BLUE,   73,  0.85 * pi,   True, 15],
    [17, 2, BLUE,   73,  -0.85 * pi,  True, 15],
    [17, 2, BLUE,   73,  pi,          True, 15],
    [14, 2, ORANGE, 0,   0,           True, 13, True,  41, 0.25 * pi],
    [14, 2, ORANGE, 0,   0,           True, 13, True,  41, -0.25 * pi],
    [14, 2, ORANGE, 0,   0,           True, 13, True,  59, 0.167 * pi],
    [14, 2, ORANGE, 0,   0,           True, 13, True,  59, -0.167 * pi],
    [12, 1, ORANGE, 0,   0,           True, 12, True,  78, 0.125 * pi],
    [12, 1, ORANGE, 0,   0,           True, 12, True,  78, -0.125 * pi],
    [8,  1, ORANGE, 0,   0,           True, 8,  True,  79, -0.19 * pi],
    [8,  1, ORANGE, 0,   0,           True, 8,  True,  79, 0.19 * pi],
    [39, 5, ORANGE, 0,   0,           True, 25, True,  0,  0],
    [17, 2, ORANGE, 0,   0,           True, 15, True,  42, -1.0 * pi],
    [17, 2, ORANGE, 0,   0,           True, 15, True,  42, -0.667 * pi],
    [17, 2, ORANGE, 0,   0,           True, 15, True,  42, 0.667 * pi]

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
    "name": 'TurtleDamaging',
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
    [56, 2, BLUE,         85,  0.5 * pi,   True,  21],
    [56, 2, BLUE,         85,  -0.5 * pi,  True,  21],
    [17, 2, BLUE,         145, -0.59 * pi],
    [17, 2, BLUE,         145, 0.59 * pi],
    [17, 2, BLUE,         145, -0.41 * pi],
    [17, 2, BLUE,         145, 0.41 * pi],
    [17, 2, BLUE,         62,  0.75 * pi],
    [17, 2, BLUE,         62,  -0.75 * pi],
    [9,  1, ORANGE,       42,  0.2 * pi,   True,  9],
    [9,  1, ORANGE,       42,  -0.2 * pi,  True,  9],
    [9,  1, ORANGE,       32,  0.28 * pi,  True,  9],
    [9,  1, ORANGE,       32,  -0.28 * pi, True,  9],
    [9,  1, ORANGE,       25,  -0.43 * pi, True,  9],
    [9,  1, ORANGE,       25,  0.43 * pi,  True,  9],
    [9,  1, ORANGE,       27,  -0.62 * pi, True,  9],
    [9,  1, ORANGE,       27,  0.62 * pi,  True,  9],
    [9,  1, ORANGE,       34,  -0.73 * pi, True,  9],
    [9,  1, ORANGE,       34,  0.73 * pi,  True,  9],
    [9,  1, ORANGE,       44,  -0.8 * pi,  True,  9],
    [9,  1, ORANGE,       44,  0.8 * pi,   True,  9],
    [18, 2, LIGHT_ORANGE, 56,  0.15 * pi,  False, 0,  False, 0, 0, True, pi],
    [18, 2, LIGHT_ORANGE, 56,  -0.15 * pi, False, 0,  False, 0, 0, True, pi],
    [25, 2, ORANGE,       35,  0,          True,  11],
    [17, 2, BLUE,         62,  0.25 * pi],
    [17, 2, BLUE,         62,  -0.25 * pi],
    [17, 2, BLUE,         59,  0.12 * pi],
    [17, 2, BLUE,         59,  -0.12 * pi],
    [17, 2, BLUE,         58,  0]

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

    [11,  1, ORANGE,       122, 0.572 * pi,  True,  11],
    [11,  1, ORANGE,       122, 0.428 * pi,  True,  11],
    [11,  1, ORANGE,       139, 0.564 * pi,  True,  11],
    [11,  1, ORANGE,       139, 0.436 * pi,  True,  11],
    [11,  1, ORANGE,       156, 0.558 * pi,  True,  11],
    [11,  1, ORANGE,       156, 0.442 * pi,  True,  11],
    [11,  1, ORANGE,       173, 0.551 * pi,  True,  11],
    [11,  1, ORANGE,       173, 0.449 * pi,  True,  11],
    [11,  1, ORANGE,       190, 0.546 * pi,  True,  11],
    [11,  1, ORANGE,       190, 0.454 * pi,  True,  11],
    [11,  1, ORANGE,       207, 0.542 * pi,  True,  11],
    [11,  1, ORANGE,       207, 0.458 * pi,  True,  11],
    [18,  2, LIGHT_ORANGE, 122, 0.572 * pi,  False, 0,  False, 0, 0, True, 0.5 * pi,   92],
    [18,  2, LIGHT_ORANGE, 122, 0.428 * pi,  False, 0,  False, 0, 0, True, 0.5 * pi,   92],
    [25,  2, ORANGE,       119, 0.5 * pi,    True,  19],
    [11,  1, ORANGE,       122, -0.572 * pi, True,  11],
    [11,  1, ORANGE,       122, -0.428 * pi, True,  11],
    [11,  1, ORANGE,       139, -0.564 * pi, True,  11],
    [11,  1, ORANGE,       139, -0.436 * pi, True,  11],
    [11,  1, ORANGE,       156, -0.558 * pi, True,  11],
    [11,  1, ORANGE,       156, -0.442 * pi, True,  11],
    [11,  1, ORANGE,       173, -0.551 * pi, True,  11],
    [11,  1, ORANGE,       173, -0.449 * pi, True,  11],
    [11,  1, ORANGE,       190, -0.546 * pi, True,  11],
    [11,  1, ORANGE,       190, -0.454 * pi, True,  11],
    [11,  1, ORANGE,       207, -0.542 * pi, True,  11],
    [11,  1, ORANGE,       207, -0.458 * pi, True,  11],
    [18,  2, LIGHT_ORANGE, 122, -0.572 * pi, False, 0,  False, 0, 0, True, -0.5 * pi,  92],
    [18,  2, LIGHT_ORANGE, 122, -0.428 * pi, False, 0,  False, 0, 0, True, -0.5 * pi,  92],
    [25,  2, ORANGE,       119, -0.5 * pi,   True,  19],
    [11,  1, ORANGE,       122, 0.322 * pi,  True,  11],
    [11,  1, ORANGE,       122, 0.178 * pi,  True,  11],
    [11,  1, ORANGE,       139, 0.314 * pi,  True,  11],
    [11,  1, ORANGE,       139, 0.186 * pi,  True,  11],
    [11,  1, ORANGE,       156, 0.308 * pi,  True,  11],
    [11,  1, ORANGE,       156, 0.192 * pi,  True,  11],
    [11,  1, ORANGE,       173, 0.301 * pi,  True,  11],
    [11,  1, ORANGE,       173, 0.199 * pi,  True,  11],
    [11,  1, ORANGE,       190, 0.296 * pi,  True,  11],
    [11,  1, ORANGE,       190, 0.204 * pi,  True,  11],
    [11,  1, ORANGE,       207, 0.292 * pi,  True,  11],
    [11,  1, ORANGE,       207, 0.208 * pi,  True,  11],
    [18,  2, LIGHT_ORANGE, 122, 0.322 * pi,  False, 0,  False, 0, 0, True, 0.25 * pi,  92],
    [18,  2, LIGHT_ORANGE, 122, 0.178 * pi,  False, 0,  False, 0, 0, True, 0.25 * pi,  92],
    [25,  2, ORANGE,       119, 0.25 * pi,   True,  17],
    [11,  1, ORANGE,       122, -0.322 * pi, True,  11],
    [11,  1, ORANGE,       122, -0.178 * pi, True,  11],
    [11,  1, ORANGE,       139, -0.314 * pi, True,  11],
    [11,  1, ORANGE,       139, -0.186 * pi, True,  11],
    [11,  1, ORANGE,       156, -0.308 * pi, True,  11],
    [11,  1, ORANGE,       156, -0.192 * pi, True,  11],
    [11,  1, ORANGE,       173, -0.301 * pi, True,  11],
    [11,  1, ORANGE,       173, -0.199 * pi, True,  11],
    [11,  1, ORANGE,       190, -0.296 * pi, True,  11],
    [11,  1, ORANGE,       190, -0.204 * pi, True,  11],
    [11,  1, ORANGE,       207, -0.292 * pi, True,  11],
    [11,  1, ORANGE,       207, -0.208 * pi, True,  11],
    [18,  2, LIGHT_ORANGE, 122, -0.322 * pi, False, 0,  False, 0, 0, True, -0.25 * pi, 92],
    [18,  2, LIGHT_ORANGE, 122, -0.178 * pi, False, 0,  False, 0, 0, True, -0.25 * pi, 92],
    [25,  2, ORANGE,       119, -0.25 * pi,  True,  19],
    [11,  1, ORANGE,       122, 0.822 * pi,  True,  11],
    [11,  1, ORANGE,       122, 0.678 * pi,  True,  11],
    [11,  1, ORANGE,       139, 0.814 * pi,  True,  11],
    [11,  1, ORANGE,       139, 0.686 * pi,  True,  11],
    [11,  1, ORANGE,       156, 0.808 * pi,  True,  11],
    [11,  1, ORANGE,       156, 0.692 * pi,  True,  11],
    [11,  1, ORANGE,       173, 0.801 * pi,  True,  11],
    [11,  1, ORANGE,       173, 0.699 * pi,  True,  11],
    [11,  1, ORANGE,       190, 0.796 * pi,  True,  11],
    [11,  1, ORANGE,       190, 0.704 * pi,  True,  11],
    [11,  1, ORANGE,       207, 0.792 * pi,  True,  11],
    [11,  1, ORANGE,       207, 0.708 * pi,  True,  11],
    [18,  2, LIGHT_ORANGE, 122, 0.822 * pi,  False, 0,  False, 0, 0, True, 0.75 * pi,  92],
    [18,  2, LIGHT_ORANGE, 122, 0.678 * pi,  False, 0,  False, 0, 0, True, 0.75 * pi,  92],
    [25,  2, ORANGE,       119, 0.75 * pi,   True,  19],
    [11,  1, ORANGE,       122, -0.822 * pi, True,  11],
    [11,  1, ORANGE,       122, -0.678 * pi, True,  11],
    [11,  1, ORANGE,       139, -0.814 * pi, True,  11],
    [11,  1, ORANGE,       139, -0.686 * pi, True,  11],
    [11,  1, ORANGE,       156, -0.808 * pi, True,  11],
    [11,  1, ORANGE,       156, -0.692 * pi, True,  11],
    [11,  1, ORANGE,       173, -0.801 * pi, True,  11],
    [11,  1, ORANGE,       173, -0.699 * pi, True,  11],
    [11,  1, ORANGE,       190, -0.796 * pi, True,  11],
    [11,  1, ORANGE,       190, -0.704 * pi, True,  11],
    [11,  1, ORANGE,       207, -0.792 * pi, True,  11],
    [11,  1, ORANGE,       207, -0.708 * pi, True,  11],
    [18,  2, LIGHT_ORANGE, 122, -0.822 * pi, False, 0,  False, 0, 0, True, -0.75 * pi, 92],
    [18,  2, LIGHT_ORANGE, 122, -0.678 * pi, False, 0,  False, 0, 0, True, -0.75 * pi, 92],
    [25,  2, ORANGE,       119, -0.75 * pi,  True,  19],
    [29,  3, BLUE,         147, 0.9 * pi,    True,  25],
    [29,  3, BLUE,         147, -0.9 * pi,   True,  25],
    [128, 5, BLUE,         0,   0,           True,  51],
    [22,  2, BLUE,         142, pi,          True,  19],
    [17,  2, BLUE,         113, pi,          True,  16],
    [17,  2, BLUE,         17,  pi,          True,  16],
    [34,  3, BLUE,         31,  0,           True,  29],
    [17,  2, BLUE,         31,  0.5 * pi,    True,  16],
    [17,  2, BLUE,         31,  -0.5 * pi,   True,  16],
    [19,  2, BLUE,         91,  0,           True,  17],
    [22,  2, BLUE,         65,  0,           True,  20],
    [34,  3, BLUE,         130, 0,           True,  25],
    [17,  2, BLUE,         164, 0.04 * pi,   True,  16],
    [17,  2, BLUE,         164, -0.04 * pi,  True,  16]

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
    [24, 2, BLUE,   0,  0,          True,  18],
    [18, 2, BLUE,   38, 0.74 * pi,  True,  8],
    [18, 2, BLUE,   38, -0.74 * pi, True,  8],
    [17, 2, BLUE,   34, 0,          True,  16],
    [14, 1, BLUE,   55, 0.1 * pi,   True,  13],
    [14, 1, BLUE,   55, -0.1 * pi,  True,  1],
    [19, 2, ORANGE, 0,  0,          True,  20, True,  0],
    [7,  1, ORANGE, 0,  0,          True,  7,  True,  25]
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
    [39, 4, BLUE,   0,  0,          True,  34],
    [28, 2, ORANGE, 0,  0,          True,  25, True, 0],
    [11, 1, ORANGE, 0,  0,          True,  11, True, 31],
    [22, 2, BLUE,   54, 0.25 * pi,  True,  19],
    [22, 2, BLUE,   54, -0.25 * pi, True,  19],
    [22, 2, BLUE,   54, 0.75 * pi,  True,  19],
    [22, 2, BLUE,   54, -0.75 * pi, True,  19],
    [17, 2, BLUE,   51, pi,         True,  14]
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
    [45, 4, BLUE,   8,  0,          True,  28],
    [22, 2, BLUE,   56, 0.72 * pi,  True,  19],
    [22, 2, BLUE,   56, -0.72 * pi, True,  19],
    [22, 2, BLUE,   56, pi,         True,  19],
    [18, 1, BLUE,   93, 0.72 * pi,  True,  17],
    [18, 1, BLUE,   93, -0.72 * pi, True,  17],
    [28, 2, ORANGE, 0,  0,          True,  25, True, 0],
    [11, 1, ORANGE, 0,  0,          True,  11, True, 32]
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
    [17, 2, BLUE,         200, 0.95 * pi,  True,  17],
    [19, 2, BLUE,         172, 0.95 * pi,  True,  18],
    [28, 3, BLUE,         136, 0.95 * pi,  True,  22],
    [17, 2, BLUE,         194, 0.32 * pi,  True,  17],
    [19, 2, BLUE,         166, 0.32 * pi,  True,  18],
    [28, 3, BLUE,         130, 0.32 * pi,  True,  22],
    [17, 2, BLUE,         206, 0.63 * pi,  True,  17],
    [19, 2, BLUE,         177, 0.63 * pi,  True,  18],
    [28, 3, BLUE,         142, 0.63 * pi,  True,  22],
    [17, 2, BLUE,         184, -0.39 * pi, True,  17],
    [19, 2, BLUE,         156, -0.4 * pi,  True,  18],
    [28, 3, BLUE,         120, -0.42 * pi, True,  22],
    [17, 2, BLUE,         213, -0.76 * pi, True,  17],
    [19, 2, BLUE,         184, -0.76 * pi, True,  18],
    [28, 3, BLUE,         149, -0.76 * pi, True,  22],
    [39, 2, BLUE,         102, 0.23 * pi,  True,  17],
    [39, 2, BLUE,         92,  0.45 * pi,  True,  17],
    [39, 2, BLUE,         99,  0.66 * pi,  True,  17],
    [39, 2, BLUE,         99,  0.87 * pi,  True,  17],
    [39, 2, BLUE,         99,  -0.94 * pi, True,  17],
    [39, 2, BLUE,         99,  -0.75 * pi, True,  17],
    [39, 2, BLUE,         88,  -0.57 * pi, True,  17],
    [39, 2, BLUE,         89,  -0.37 * pi, True,  17],
    [39, 2, BLUE,         93,  -0.16 * pi, True,  17],
    [18, 2, ORANGE,       79,  0.26 * pi,  True,  16],
    [18, 2, ORANGE,       79,  -0.26 * pi, True,  16],
    [18, 2, ORANGE,       79,  0.74 * pi,  True,  16],
    [18, 2, ORANGE,       79,  -0.74 * pi, True,  16],
    [7,  1, LIGHT_ORANGE, 0,   0,          False, 0,  False, 0, 0, False, 0, 0, True, 56, 0],
    [7,  1, LIGHT_ORANGE, 0,   0,          False, 0,  False, 0, 0, False, 0, 0, True, 56, 0.65 * pi]
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
    "body_size": HF(410),
    "trajectory": rose_curve_1
}

COCKROACH_BODY = [
    [17, 2, BLUE,   31, 0.66 * pi,  True, 16],
    [17, 2, BLUE,   31, -0.66 * pi, True, 16],
    [14, 2, BLUE,   55, 0.59 * pi,  True, 13],
    [14, 2, BLUE,   55, -0.59 * pi, True, 13],
    [18, 2, BLUE,   78, 0.48 * pi,  True, 16],
    [18, 2, BLUE,   78, -0.48 * pi, True, 16],
    [14, 2, BLUE,   54, 0.47 * pi,  True, 12],
    [14, 2, BLUE,   54, -0.47 * pi, True, 12],
    [14, 2, BLUE,   66, 0.39 * pi,  True, 12],
    [14, 2, BLUE,   66, -0.39 * pi, True, 12],
    [14, 2, BLUE,   72, 0.29 * pi,  True, 12],
    [14, 2, BLUE,   72, -0.29 * pi, True, 12],
    [14, 2, BLUE,   79, 0.2 * pi,   True, 12],
    [14, 2, BLUE,   79, -0.2 * pi,  True, 12],
    [25, 2, BLUE,   5,  0,          True, 19],
    [21, 2, ORANGE, 0,  0,          True, 16, True,  0],
    [8,  1, ORANGE, 0,  0,          True, 8,  True,  27]
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

    [25, 2, BLUE,         54,  0.54 * pi,   True,  23],
    [25, 2, BLUE,         54,  -0.54 * pi,  True,  23],
    [25, 2, BLUE,         108, 0.17 * pi,   True,  23],
    [25, 2, BLUE,         108, -0.17 * pi,  True,  23],
    [25, 2, BLUE,         38,  0.73 * pi,   True,  23],
    [25, 2, BLUE,         38,  -0.73 * pi,  True,  23],
    [25, 2, BLUE,         85,  0.83 * pi,   True,  23],
    [25, 2, BLUE,         85,  -0.83 * pi,  True,  23],
    [25, 2, BLUE,         120, 0.9 * pi,    True,  23],
    [25, 2, BLUE,         120, -0.9 * pi,   True,  23],
    [15, 2, BLUE,         140, 0.15 * pi,   True,  14],
    [15, 2, BLUE,         140, -0.15 * pi,  True,  14],
    [15, 2, BLUE,         115, 0.27 * pi,   True,  14],
    [15, 2, BLUE,         115, -0.27 * pi,  True,  14],
    [15, 2, BLUE,         153, 0.91 * pi,   True,  14],
    [15, 2, BLUE,         153, -0.91 * pi,  True,  14],
    [15, 2, BLUE,         128, 0.82 * pi,   True,  14],
    [15, 2, BLUE,         128, -0.82 * pi,  True,  14],
    [54, 4, BLUE,         42,  0,           True,  39],
    [27, 2, ORANGE,       42,  0,           True,  28, True,  0],
    [12, 1, ORANGE,       42,  0,           True,  12, True,  32],
    [11, 1, ORANGE,       46,  0.85 * pi,   True,  11],
    [11, 1, ORANGE,       46,  -0.85 * pi,  True,  11],
    [11, 1, ORANGE,       61,  0.888 * pi,  True,  11],
    [11, 1, ORANGE,       61,  -0.888 * pi, True,  11],
    [11, 1, ORANGE,       76,  0.91 * pi,   True,  11],
    [11, 1, ORANGE,       76,  -0.91 * pi,  True,  11],
    [11, 1, ORANGE,       92,  0.925 * pi,  True,  11],
    [11, 1, ORANGE,       92,  -0.925 * pi, True,  11],
    [11, 1, ORANGE,       108, 0.935 * pi,  True,  11],
    [11, 1, ORANGE,       108, -0.935 * pi, True,  11],
    [11, 1, ORANGE,       123, 0.944 * pi,  True,  11],
    [11, 1, ORANGE,       123, -0.944 * pi, True,  11],
    [18, 2, LIGHT_ORANGE, 46,  0.85 * pi,   False, 0,  False, 0,  0, True, pi, 92],
    [18, 2, LIGHT_ORANGE, 46,  -0.85 * pi,  False, 0,  False, 0,  0, True, pi, 92],
    [19, 2, ORANGE,       42,  pi,          True,  18]

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
    [21, 2, BLUE,   41, 0.5 * pi,   True,  18],
    [21, 2, BLUE,   41, -0.5 * pi,  True,  18],
    [14, 2, BLUE,   56, 0.64 * pi,  True,  12],
    [14, 2, BLUE,   56, -0.64 * pi, True,  12],
    [29, 3, BLUE,   0,  0,          True,  23],
    [21, 2, BLUE,   38, pi,         True,  18],
    [24, 2, ORANGE, 0,  0,          True,  24, True,  True, 0],
    [9,  1, ORANGE, 0,  0,          True,  9,  True,  True, 24]
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
    [7,  1, BLUE,   31, -pi],
    [7,  1, BLUE,   36, -0.877 * pi],
    [7,  1, BLUE,   39, -0.767 * pi],
    [7,  1, BLUE,   39, -0.667 * pi],
    [7,  1, BLUE,   39, -0.567 * pi],
    [7,  1, BLUE,   36, -0.457 * pi],
    [7,  1, BLUE,   31, -0.333 * pi],
    [7,  1, BLUE,   36, -0.21 * pi],
    [7,  1, BLUE,   39, -0.1 * pi],
    [7,  1, BLUE,   39, 0],
    [7,  1, BLUE,   39, 0.1 * pi],
    [7,  1, BLUE,   36, 0.21 * pi],
    [7,  1, BLUE,   31, 0.333 * pi],
    [7,  1, BLUE,   36, 0.457 * pi],
    [7,  1, BLUE,   39, 0.567 * pi],
    [7,  1, BLUE,   39, 0.667 * pi],
    [7,  1, BLUE,   39, 0.767 * pi],
    [7,  1, BLUE,   36, 0.877 * pi],
    [15, 1.6, BLUE,   15, 0,           True,  15],
    [15, 1.6, BLUE,   15, 0.667 * pi,  True,  15],
    [15, 1.6, BLUE,   15, -0.667 * pi, True,  15]
]

AMEBA_HEALTH_STATES = (
    (4, ),
    (3, (20, 21)),
    (2, (19, 21)),
    (1, (18, 21))
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
    [8,  1, BLUE,   28, 0.167 * pi],
    [8,  1, BLUE,   28, 0.333 * pi],
    [8,  1, BLUE,   28, 0.5 * pi],
    [8,  1, BLUE,   28, 0.667 * pi],
    [8,  1, BLUE,   28, 0.833 * pi],
    [8,  1, BLUE,   28, pi],
    [8,  1, BLUE,   28, 1.167 * pi],
    [8,  1, BLUE,   28, 1.333 * pi],
    [8,  1, BLUE,   28, 1.5 * pi],
    [8,  1, BLUE,   28, 1.667 * pi],
    [8,  1, BLUE,   28, 1.833 * pi],
    [8,  1, BLUE,   28, 2.0 * pi],
    [19, 2, BLUE,   0,  0,          True,  18]
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
    "radius": HF(28),
    "body": scaled_body(CELL_BODY),
    "gun_type": 'GunPeaceful',
    "angular_vel": 0.00065,
    "body_size": HF(72),
    "trajectory": rose_curve_1
}

INFUSORIA_BODY = [
    [14, 1, BLUE,   39, 0.813 * pi,  True,  13],
    [14, 1, BLUE,   39, -0.813 * pi, True,  13],
    [25, 3, BLUE,   0,  0,           True,  22],
    [11, 1, BLUE,   31, 0,           True,  11]
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
    [11, 1, BLUE,   19, 0.8 * pi,   True,  11],
    [15, 1, BLUE,   0,  0,          True,  14],
    [11, 1, BLUE,   19, -0.8 * pi,  True,  11]
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
    [17, 2, BLUE,   160, 0.075 * pi,  True, 17],
    [17, 2, BLUE,   160, -0.075 * pi, True, 17],
    [17, 2, BLUE,   133, 0.06 * pi,   True, 17],
    [17, 2, BLUE,   133, -0.06 * pi,  True, 17],
    [17, 2, BLUE,   169, 0.13 * pi,   True, 17],
    [17, 2, BLUE,   169, -0.13 * pi,  True, 17],
    [17, 2, BLUE,   173, 0.18 * pi,   True, 17],
    [17, 2, BLUE,   173, -0.18 * pi,  True, 17],
    [17, 2, BLUE,   173, 0.23 * pi,   True, 17],
    [17, 2, BLUE,   173, -0.23 * pi,  True, 17],
    [17, 2, BLUE,   164, 0.28 * pi,   True, 17],
    [17, 2, BLUE,   164, -0.28 * pi,  True, 17],
    [27, 2, BLUE,   118, 0.2 * pi,    True, 24],
    [27, 2, BLUE,   118, -0.2 * pi,   True, 24],
    [27, 2, BLUE,   105, 0.74 * pi,   True, 24],
    [27, 2, BLUE,   105, -0.74 * pi,  True, 24],
    [27, 2, BLUE,   115, 0.5 * pi,    True, 24],
    [27, 2, BLUE,   115, -0.5 * pi,   True, 24],
    [27, 2, BLUE,   76,  0.5 * pi,    True, 24],
    [27, 2, BLUE,   76,  -0.5 * pi,   True, 24],
    [65, 2, BLUE,   71,  0,           True, 22],
    [85, 2, BLUE,   35,  pi,          True, 28],
    [27, 2, BLUE,   130, 0.82 * pi,   True, 24],
    [27, 2, BLUE,   130, -0.82 * pi,  True, 24],
    [27, 2, BLUE,   133, pi,          True, 24],
    [28, 4, ORANGE, 82,  0,           True, 27, True],
    [12, 1, ORANGE, 82,  0,           True, 12, True,  35],
    [38, 4, ORANGE, 49,  pi,          True, 35, True],
    [15, 2, ORANGE, 49,  pi,          True, 14, True,  49]
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
    [19, 2, BLUE,   64, 0.1 * pi],
    [19, 2, BLUE,   64, 0.3 * pi],
    [19, 2, BLUE,   64, 0.5 * pi],
    [19, 2, BLUE,   64, 0.7 * pi],
    [19, 2, BLUE,   64, 0.9 * pi],
    [19, 2, BLUE,   64, -0.9 * pi],
    [19, 2, BLUE,   64, -0.7 * pi],
    [19, 2, BLUE,   64, -0.5 * pi],
    [19, 2, BLUE,   64, -0.3 * pi],
    [19, 2, BLUE,   64, -0.1 * pi],
    [61, 2, BLUE,   0,  0,         True,  24],
    [28, 4, ORANGE, 0,  0,         True,  26, True],
    [9,  1, ORANGE, 38, 0,         True,  9],
    [9,  1, ORANGE, 54, 0,         True,  9],
    [9,  1, ORANGE, 38, 0.2 * pi,  True,  9],
    [9,  1, ORANGE, 54, 0.2 * pi,  True,  9],
    [9,  1, ORANGE, 38, 0.4 * pi,  True,  9],
    [9,  1, ORANGE, 54, 0.4 * pi,  True,  9],
    [9,  1, ORANGE, 38, 0.6 * pi,  True,  9],
    [9,  1, ORANGE, 54, 0.6 * pi,  True,  9],
    [9,  1, ORANGE, 38, 0.8 * pi,  True,  9],
    [9,  1, ORANGE, 54, 0.8 * pi,  True,  9],
    [9,  1, ORANGE, 38, pi,        True,  9],
    [9,  1, ORANGE, 54, pi,        True,  9],
    [9,  1, ORANGE, 38, -0.8 * pi, True,  9],
    [9,  1, ORANGE, 54, -0.8 * pi, True,  9],
    [9,  1, ORANGE, 38, -0.6 * pi, True,  9],
    [9,  1, ORANGE, 54, -0.6 * pi, True,  9],
    [9,  1, ORANGE, 38, -0.4 * pi, True,  9],
    [9,  1, ORANGE, 54, -0.4 * pi, True,  9],
    [9,  1, ORANGE, 38, -0.2 * pi, True,  9],
    [9,  1, ORANGE, 54, -0.2 * pi, True,  9]
]


SPREADER_HEALTH_STATES = (
    (30, ),
    (25, (0, 1), (5, 6)),
    (20, (0, 2), (5, 7)),
    (15, (0, 2), (4, 7), (9, 10)),
    (10, (0, 3), (4, 8), (9, 10)),
    (5, (0, 10))
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
    [113, 8, RED,    0,  0,          True,  8],
    [61,  4, BLUE,   0,  0,          True,  24],
    [28,  5, ORANGE, 0,  0,          True,  24, True, 0],
    [11,  1, ORANGE, 0,  0,          True,  11,  True,  38]
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
    [32, 3, BLUE,   143, 0.5 * pi,   True, 29],
    [32, 3, BLUE,   143, -0.5 * pi,  True, 29],
    [32, 3, BLUE,   173, 0.79 * pi,  True, 29],
    [32, 3, BLUE,   173, -0.79 * pi, True, 29],
    [32, 3, BLUE,   147, 0.23 * pi,  True, 29],
    [32, 3, BLUE,   147, -0.23 * pi, True, 29],
    [32, 3, BLUE,   106, 0,          True, 29],
    [25, 2, BLUE,   99,  0.5 * pi,   True, 23],
    [25, 2, BLUE,   99,  -0.5 * pi,  True, 23],
    [25, 2, BLUE,   105, 0.2 * pi,   True, 23],
    [25, 2, BLUE,   105, -0.2 * pi,  True, 23],
    [51, 2, BLUE,   49,  0.28 * pi,  True, 19],
    [51, 2, BLUE,   49,  -0.28 * pi, True, 19],
    [36, 2, BLUE,   17,  0,          True, 17],
    [99, 3, BLUE,   99,  pi,         True, 46],
    [15, 2, BLUE,   91,  0.45 * pi,  True, 14],
    [15, 2, BLUE,   91,  -0.45 * pi, True, 14],
    [15, 2, BLUE,   105, 0.3 * pi,   True, 14],
    [15, 2, BLUE,   105, -0.3 * pi,  True, 14],
    [32, 3, BLUE,   116, -0.63 * pi, True, 29],
    [32, 3, BLUE,   116, 0.63 * pi,  True, 29],
    [99, 3, BLUE,   2,   pi,         True, 46],
    [15, 2, ORANGE, 99,  pi,         True, 14, True,  48, -0.2 * pi],
    [15, 2, ORANGE, 99,  pi,         True, 14, True,  48, 0.2 * pi],
    [15, 2, ORANGE, 99,  pi,         True, 14, True,  71, -0.13 * pi],
    [15, 2, ORANGE, 99,  pi,         True, 14, True,  71, 0.13 * pi],
    [42, 4, ORANGE, 99,  pi,         True, 32, True],
    [17, 2, ORANGE, 99,  pi,         True, 16, True,  54, -0.78 * pi],
    [17, 2, ORANGE, 99,  pi,         True, 16, True,  54, 0.78 * pi],
    [27, 3, ORANGE, 36,  0,          True, 24, True],
    [11, 1, ORANGE, 36,  0,          True, 11, True,  34]
]


SPIDER_HEALTH_STATES = (
    (130, (19, 22)),
    (100, (0, 4), (7, 9), (11, 19), (29, 31)),
    (70, (0, 6), (7, 9), (11, 19), (29, 31)),
    (40, (0, 6), (7, 19), (29, 31)),
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
    [14, 2, BLUE,   89, 0.07 * pi,  True,  14],
    [14, 2, BLUE,   89, -0.07 * pi, True,  14],
    [22, 2, BLUE,   62, 0,          True,  19],
    [25, 2, BLUE,   52, 0.72 * pi,  True,  23],
    [25, 2, BLUE,   52, -0.72 * pi, True,  23],
    [54, 2, BLUE,   0,  0,          True,  28],
    [17, 2, BLUE,   91, 0.72 * pi,  True,  16],
    [17, 2, BLUE,   91, -0.72 * pi, True,  16],
    [17, 2, BLUE,   58, pi,         True,  14],
    [25, 3, ORANGE, 0,  0,          True,  23,  True,  0],
    [11, 1, ORANGE, 0,  0,          True,  11,  True,  32],
    [14, 2, ORANGE, 0,  0,          True,  14,  True,  35, 0.77 * pi],
    [14, 2, ORANGE, 0,  0,          True,  14,  True,  35, -0.77 * pi]
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
    [17, 2, BLUE,   159, 0.41 * pi],
    [17, 2, BLUE,   159, -0.41 * pi],
    [17, 2, BLUE,   159, 0.59 * pi],
    [17, 2, BLUE,   159, -0.59 * pi],
    [17, 2, BLUE,   159, 0.09 * pi],
    [17, 2, BLUE,   159, -0.09 * pi],
    [17, 2, BLUE,   159, 0.91 * pi],
    [17, 2, BLUE,   159, -0.91 * pi],
    [17, 2, BLUE,   140, 0.07 * pi],
    [17, 2, BLUE,   140, -0.07 * pi],
    [17, 2, BLUE,   140, 0.93 * pi],
    [17, 2, BLUE,   140, -0.93 * pi],
    [17, 2, BLUE,   140, 0.43 * pi],
    [17, 2, BLUE,   140, -0.43 * pi],
    [17, 2, BLUE,   140, 0.57 * pi],
    [17, 2, BLUE,   140, -0.57 * pi],
    [36, 3, BLUE,   102, 0,          True,  33],
    [36, 3, BLUE,   102, 0.5 * pi,   True,  33],
    [36, 3, BLUE,   102, -0.5 * pi,  True,  33],
    [36, 3, BLUE,   102, pi,         True,  33],
    [99, 3, BLUE,   0,   0,          True,  38],
    [45, 2, BLUE,   0,   0,          True,  25],
    [8,  1, ORANGE, 0,   0,          True,  8,  True,  31, 0.23 * pi],
    [8,  1, ORANGE, 0,   0,          True,  8,  True,  31, -0.23 * pi],
    [8,  1, ORANGE, 0,   0,          True,  8,  True,  39, 0.13 * pi],
    [8,  1, ORANGE, 0,   0,          True,  8,  True,  39, -0.13 * pi],
    [8,  1, ORANGE, 0,   0,          True,  8,  True,  48, 0.06 * pi],
    [8,  1, ORANGE, 0,   0,          True,  8,  True,  48, -0.06 * pi],
    [28, 3, ORANGE, 0,   0,          True,  25, True,  0],
    [12, 1, ORANGE, 0,   0,          True,  12, True,  59]
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

    "FROZEN_BODY",
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

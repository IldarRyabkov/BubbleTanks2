from math import pi, hypot, cos, sin, atan2
import numpy as np

from data.config import *
from data.colors import *


def calculate_angle(x1, y1, x2, y2) -> float:
    return atan2(y1 - y2, x2 - x1)


def circle_collidepoint(x0, y0, r, x, y) -> bool:
    """Returns True if a point with coordinates x, y
    is inside a circle with center (x0; y0) and radius r.
    """
    return hypot(x - x0, y - y0) <= r


def no_trajectory(pos: np.array, angle: float) -> np.array:
    return pos


def rose_curve_1(pos: np.array, angle: float) -> np.array:
    dist = HF(272)
    x = dist * (cos(9/4 * angle) + 7/3) * cos(angle)
    y = dist * (cos(9/4 * angle) + 7/3) * sin(angle)
    return np.array([x, y]) + pos

def rose_curve_2(pos: np.array, angle: float) -> np.array:
    dist = HF(800)
    x = dist * sin(3/4 * angle) * cos(angle)
    y = dist * sin(3/4 * angle) * sin(angle)
    return np.array([x, y]) + pos


def rose_curve_3(pos: np.array, angle: float) -> np.array:
    dist, r = HF(600), HF(30)
    x = dist * cos(angle) + r * cos(5 * angle)
    y = dist * sin(angle) + r * sin(5 * angle)
    return np.array([x, y]) + pos


def rose_curve_4(pos: np.array, angle: float) -> np.array:
    dist = HF(400)
    x = dist * sin(2/3 * angle) * cos(angle)
    y = dist * sin(2/3 * angle) * sin(angle)
    return np.array([x, y]) + pos


def epicycloid(pos: np.array, angle: float) -> np.array:
    dist, r = HF(400), HF(20)
    x = dist * cos(angle) + r * cos(5 * angle)
    y = dist * sin(angle) + r * sin(5 * angle)
    return np.array([x, y]) + pos


def print_pretty(ugly_body, scale=1.0):
    body = [row.copy() for row in ugly_body]
    max_sizes = [0] * 20
    for j in range(len(body)):
        for i in range(len(body[j])):
            if i == 2:
                if body[j][2] == ORANGE: body[j][2] = 'ORANGE'
                elif body[j][2] == BLUE: body[j][2] = 'BLUE'
                elif body[j][2] == VIOLET: body[j][2] = 'VIOLET'
                elif body[j][2] == LIGHT_ORANGE: body[j][2] = 'LIGHT_ORANGE'
                elif body[j][2] == RED: body[j][2] = 'RED'
                elif body[j][2] == DARK_RED: body[j][2] = 'DARK_RED'
                elif body[j][2] == PURPLE: body[j][2] = 'PURPLE'
                elif body[j][2] == BUBBLE_COLOR_2: body[j][2] = 'BUBBLE_COLOR_2'
                elif body[j][2] == BUBBLE_COLOR: body[j][2] = 'BUBBLE_COLOR'

            elif i == 6:
                body[j][i] = str(round(body[j][i] / scale, 3))

            elif i in (0, 1, 3, 7, 10, 15):
                body[j][i] = str(round(body[j][i] / scale))

            elif i in (4, 11, 13, 16):
                sign = '' if body[j][i] > 0 else '-'
                if body[j][i] == 0:
                    body[j][i] = '0'
                elif body[j][i] == pi:
                    body[j][i] = 'pi'
                else:
                    body[j][i] = sign + str(round(abs(body[j][i]/pi), 3)) + ' * pi'

            else:
                body[j][i] = str(body[j][i])

            if len(body[j][i]) > max_sizes[i]:
                max_sizes[i] = len(str(body[j][i]))

    for i in range(len(body)):
        row = '    ['
        for j in range(len(body[i])):
            row += str(body[i][j])
            if j != len(body[i]) - 1:
                row += ', ' + ' '*(max_sizes[j]-len(str(body[i][j])))
        row += '],' if i != len(body) - 1 else ']'
        print(row)


def scaled_body(body: list) -> list:
    """returns copy of body scaled by screen size."""
    scaled = [row.copy() for row in body]
    for row in scaled:
        for i in range(len(row)):
            if i in (0, 1, 3, 6, 7, 10, 15):
                row[i] = HF(row[i])
    return scaled


def H(v):
    """ Returns the scaled rounded value to fit the height of the screen.
    Initially, all sizes of objects were matched to the height of 960,
    so the scaling factor is SCR_H / 960.
    """
    return round(v * HEIGHT_SCALE_FACTOR)


def W(v):
    """ Returns the scaled integer value to fit the width of the screen.
    Initially, all sizes of objects were matched to the width of 1280,
    so the scaling factor is SCR_W / 1280.
    """
    return round(v * WIDTH_SCALE_FACTOR)


def HF(v):
    """ Returns the scaled float value to fit the height of the screen.
    Initially, all sizes of objects were matched to the height of 960,
    so the scaling factor is SCR_H / 960.
    """
    return v * HEIGHT_SCALE_FACTOR


def WF(v: float):
    """ Returns the scaled float value to fit the width of the screen.
    Initially, all sizes of objects were matched to the width of 1280,
    so the scaling factor is SCR_W / 1280.
    """
    return v * WIDTH_SCALE_FACTOR


__all__ = [

    "calculate_angle",
    "circle_collidepoint",
    "no_trajectory",
    "rose_curve_1",
    "rose_curve_2",
    "rose_curve_3",
    "rose_curve_4",
    "epicycloid",
    "print_pretty",
    "H",
    "W",
    "HF",
    "WF",
    "scaled_body"

]

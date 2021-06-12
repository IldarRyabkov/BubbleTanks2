from math import pi, hypot, cos, sin, atan2
import pygame as pg

from data.constants import *


def calculate_angle(x1, y1, x2, y2) -> float:
    """Calculates angle in radians between x-axis and
    2D vector with coordinates (x2 - x1; y2 - y1). For example:
    x1 = 1, y1 = 1, x2 = 2, y2 = 0 -> 0.25 * pi
    x1 = 1, y1 = 1, x2 = 1, y2 = 5 -> -0.5 * pi
    """
    return atan2(y1 - y2, x2 - x1)


def circle_collidepoint(x0, y0, r, x, y) -> bool:
    """Returns True if a point with coordinates x, y
    is inside a circle with center (x0; y0) and radius r.
    """
    return hypot(x - x0, y - y0) <= r


def no_trajectory(xo, yo, angle):
    return xo, yo


def rose_curve_1(xo, yo, angle):
    dist = HF(272)
    x = dist * (cos(9/4 * angle) + 7/3) * cos(angle)
    y = dist * (cos(9/4 * angle) + 7/3) * sin(angle)
    return xo + x, yo + y

def rose_curve_2(xo, yo, angle):
    dist = HF(800)
    x = dist * sin(3/4 * angle) * cos(angle)
    y = dist * sin(3/4 * angle) * sin(angle)
    return xo + x, yo + y


def rose_curve_3(xo, yo, angle):
    dist, r = HF(600), HF(30)
    x = dist * cos(angle) + r * cos(5 * angle)
    y = dist * sin(angle) + r * sin(5 * angle)
    return xo + x, yo + y


def rose_curve_4(xo, yo, angle):
    dist = HF(400)
    x = dist * sin(2/3 * angle) * cos(angle)
    y = dist * sin(2/3 * angle) * sin(angle)
    return xo + x, yo + y


def epicycloid(xo, yo, angle):
    dist, r = HF(400), HF(20)
    x = dist * cos(angle) + r * cos(5 * angle)
    y = dist * sin(angle) + r * sin(5 * angle)
    return xo + x, yo + y


def set_cursor_grab(grab):
    """A game scene wrapper. Sets the state of grabbing the cursor for the
    duration of the game scene, and then returns it to its original state.
    """
    def decorator(game_scene):
        def wrapper(*args, **kwargs):
            old_grab = pg.event.get_grab()
            pg.event.set_grab(grab)
            game_scene(*args, **kwargs)
            pg.event.set_grab(old_grab)
        return wrapper
    return decorator


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

            elif i in (0, 3, 6, 8, 12, 14):
                value = round(body[j][i] / scale, 1)
                if value == int(value):
                    value = int(value)
                body[j][i] = str(value)

            elif i in (4, 9, 11, 15):
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
            if i in (0, 1, 3, 6, 8, 12, 14):
                row[i] = HF(row[i])
    return scaled


def H(v):
    """ Returns the scaled rounded value to fit the height of the screen.
    Initially, all sizes of objects were matched to the height of 960,
    so the scaling factor is SCR_H / 960.
    """
    return round(v * H_SCALE_FACTOR)


def W(v):
    """ Returns the scaled integer value to fit the width of the screen.
    Initially, all sizes of objects were matched to the width of 1280,
    so the scaling factor is SCR_W / 1280.
    """
    return round(v * W_SCALE_FACTOR)


def HF(v):
    """ Returns the scaled float value to fit the height of the screen.
    Initially, all sizes of objects were matched to the height of 960,
    so the scaling factor is SCR_H / 960.
    """
    return v * H_SCALE_FACTOR


def WF(v: float):
    """ Returns the scaled float value to fit the width of the screen.
    Initially, all sizes of objects were matched to the width of 1280,
    so the scaling factor is SCR_W / 1280.
    """
    return v * W_SCALE_FACTOR


def pretty_resolution(resolution) -> str:
    """Returns text representation of game resolution."""
    return '%d x %d' % tuple(resolution)


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
    "scaled_body",
    "set_cursor_grab",
    "pretty_resolution"

]

from math import pi, atan, hypot, cos, sin
import numpy as np

from data.config import SCR_H
from data.colors import *


def calculate_angle(x_1, y_1, x_2, y_2):
    if x_2 != x_1:
        arctan = atan(-(y_2 - y_1) / (x_2 - x_1))
        alpha = arctan if x_2 > x_1 else pi + arctan
    else:
        alpha = pi/2 if y_2 < y_1 else -pi/2
    return alpha


def circle_collidepoint(x0, y0, r, x, y):
    return x0-r <= x <= x0+r and y0-r <= y <= y0+r and hypot(x-x0, y-y0) <= r


def no_trajectory(pos: np.array, angle: float) -> np.array:
    return pos


def rose_curve_1(pos: np.array, angle: float) -> np.array:
    dist = 17/60 * SCR_H
    x = dist * (cos(9/4 * angle) + 7/3) * cos(angle)
    y = dist * (cos(9/4 * angle) + 7/3) * sin(angle)
    return np.array([x, y]) + pos

def rose_curve_2(pos: np.array, angle: float) -> np.array:
    dist = 5/6 * SCR_H
    x = dist * sin(3/4 * angle) * cos(angle)
    y = dist * sin(3/4 * angle) * sin(angle)
    return np.array([x, y]) + pos


def rose_curve_3(pos: np.array, angle: float) -> np.array:
    dist = 5/8 * SCR_H
    x = dist * cos(angle) + 30 * cos(5 * angle)
    y = dist * sin(angle) + 30 * sin(5 * angle)
    return np.array([x, y]) + pos


def rose_curve_4(pos: np.array, angle: float) -> np.array:
    dist = 5/12 * SCR_H
    x = dist * sin(2/3 * angle) * cos(angle)
    y = dist * sin(2/3 * angle) * sin(angle)
    return np.array([x, y]) + pos


def epicycloid(pos: np.array, angle: float) -> np.array:
    dist = 5/12 * SCR_H
    x = dist * cos(angle) + 20 * cos(5 * angle)
    y = dist * sin(angle) + 20 * sin(5 * angle)
    return np.array([x, y]) + pos


def print_pretty(body, name='', scale=1.0):
    max_sizes = [0] * 20
    for j in range(len(body)):
        for i in range(len(body[j])):
            if i == 2:
                if body[j][2] == ORANGE: body[j][2] = 'ORANGE'
                elif body[j][2] == BLUE: body[j][2] = 'BLUE'
                elif body[j][2] == VIOLET: body[j][2] = 'VIOLET'
                elif body[j][2] == LIGHT_ORANGE: body[j][2] = 'LIGHT_ORANGE'
                elif body[j][2] == RED: body[j][2] = 'RED'
                elif body[j][2] == PURPLE: body[j][2] = 'PURPLE'
            elif i == 6:
                body[j][i] = str(round(body[j][i] / scale, 3))
            elif i in (0, 3, 7, 11, 16):
                body[j][i] = str(int(body[j][i] / scale))
            elif i in (4, 12, 14, 17):
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
        row = ' ' * (len(name) + 4) + '['
        for j in range(len(body[i])):
            row += str(body[i][j])
            if j != len(body[i]) - 1:
                row += ', ' + ' '*(max_sizes[j]-len(str(body[i][j])))
        row += '],'
        print(row)

from math import pi, atan, hypot


def calculate_angle(x_1, y_1, x_2, y_2):
    if x_2 != x_1:
        arctan = atan(-(y_2 - y_1) / (x_2 - x_1))
        alpha = arctan if x_2 > x_1 else pi + arctan
    else:
        alpha = pi/2 if y_2 < y_1 else -pi/2
    return alpha


def circle_collidepoint(x0, y0, r, x, y):
    return x0-r <= x <= x0+r and y0-r <= y <= y0+r and hypot(x-x0, y-y0) <= r

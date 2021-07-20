from math import hypot, atan2, pi
from copy import deepcopy
import pygame as pg

from data.constants import *
from data.languages import TEXTS


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0


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


def H(v):
    """ Returns the scaled rounded value to fit the height of the screen.
    Initially, all sizes of objects were matched to the window height of 960,
    so the scale factor is SCR_H / 960.
    """
    return round(v * H_SCALE_FACTOR)


def W(v):
    """ Returns the scaled integer value to fit the width of the screen.
    Initially, all sizes of objects were matched to the window width of 1280,
    so the scale factor is SCR_W / 1280.
    """
    return round(v * W_SCALE_FACTOR)


def HF(v):
    """ Returns the scaled float value to fit the height of the screen.
    Initially, all sizes of objects were matched to window the height of 960,
    so the scale factor is SCR_H / 960.
    """
    return v * H_SCALE_FACTOR


def WF(v):
    """ Returns the scaled float value to fit the width of the screen.
    Initially, all sizes of objects were matched to the window width of 1280,
    so the scale factor is SCR_W / 1280.
    """
    return v * W_SCALE_FACTOR


def pretty_resolution(resolution) -> str:
    """Returns text representation of game resolution."""
    return '%d x %d' % tuple(resolution)


def screen_mode_texts(screen_mode: int) -> str:
    if screen_mode == WINDOWED_MODE:
        return TEXTS["windowed mode"]
    if screen_mode == BORDERLESS_MODE:
        return TEXTS["borderless mode"]
    if screen_mode == FULLSCREEN_MODE:
        return TEXTS["fullscreen mode"]


def print_circle_params(dx, dy, radius, scale):
    s = 960/4/scale
    distance = round(hypot(dx, dy) * s, 3)
    angle = calculate_angle(0, 0, dx, dy)
    angle = round(angle/pi, 3)
    angle = str(angle) + ' * pi'
    radius = round(radius * s, 3)
    print(radius, distance, angle)


def dict_to_list(original_data: dict):
    def delete_element(element):
        for value in data.values():
            if element in value:
                while value.index(element) != 0:
                    delete_element(value[0])
                break
        for value in data.values():
            if element in value:
                value.remove(element)
        result.append(element)

    result = []
    data = deepcopy(original_data)
    while any(value for value in data.values()):
        for value in data.values():
            if value:
                delete_element(value[0])
                break
    return result


def make_states_dict(data: dict, circles_list: list):
    return {k: [circles_list.index(circle) for circle in v] for k, v in data.items()}


__all__ = [

    "sign",
    "calculate_angle",
    "circle_collidepoint",
    "H",
    "W",
    "HF",
    "WF",
    "set_cursor_grab",
    "pretty_resolution",
    "screen_mode_texts",
    "print_circle_params",
    "make_states_dict",
    "dict_to_list"

]

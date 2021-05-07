"""
This module contains functions that create surfaces used in the game.
To improve game performance these surfaces were saved as .pgn files
in images directory to be loaded by pygame.image.load.
So these functions are not used in the game whatsoever,
but I saved them here just in case.

"""

import pygame as pg
import numpy as np
import os
from math import hypot, cos, sin, pi, sqrt

from data.colors import *
from data.paths import ROOT_DIR, FONT_1
from data.languages.english import UPGRADEMENU_CAPTION as ENG_UPG_CAPTION
from data.languages.russian import UPGRADEMENU_CAPTION as RUS_UPG_CAPTION


def save(surface, filename):
    pg.image.save(surface, os.path.join(ROOT_DIR, "images\%s.png" % filename))


def background() -> pg.Surface:
    w, h = 1920, 1080
    surface = pg.Surface((w, h))
    color_1 = np.array(BG_COLOR_1, dtype=float)
    color_2 = np.array(BG_COLOR_2, dtype=float)
    color_delta = color_2 - color_1
    for i in range(h):
        color = color_1 + color_delta * i/(h - 1)
        pg.draw.rect(surface, color.astype(int), pg.Rect(0, i, w, 1))
    return surface


def bubble_halo() -> pg.Surface:
    radius = 150
    diam = 2 * radius
    edge = 100
    surface = pg.Surface((diam, diam), pg.SRCALPHA)
    arr = pg.PixelArray(surface)
    for x in range(0, radius):
        for y in range(0, radius):
            dist = hypot(x - radius, y - radius)
            if edge <= dist <= radius:
                alpha = int((radius - dist) / (radius - edge) * 150)
            else:
                alpha = 0
            color = (255, 255, 255, alpha)
            arr[x, y] = color
            arr[diam - x - 1, y] = color
            arr[x, diam - y - 1] = color
            arr[diam - x - 1, diam - y - 1] = color
    surface = arr.make_surface()
    return surface


def boss_aim() -> pg.Surface:
    radius = 150
    alpha = 90
    beta = 126
    vertexes = []
    for i in range(10):
        if i % 2 == 0:
            x = int(radius + radius * cos(alpha * pi / 180))
            y = int(radius - radius * sin(alpha * pi / 180))
            alpha += 72
        else:
            x = int(radius + 0.62 * radius * cos(beta * pi / 180))
            y = int(radius - 0.62 * radius * sin(beta * pi / 180))
            beta += 72
        vertexes.append((x, y))
    vertexes.append(vertexes[0])

    surface = pg.Surface((2 * radius, 2 * radius))
    surface.set_colorkey(RED)
    surface.fill(RED)
    pg.draw.polygon(surface, WHITE, vertexes)
    pg.draw.circle(surface, RED, (radius, radius), int(0.6 * radius))
    main_surface = pg.Surface((2 * radius, 2 * radius), pg.SRCALPHA)
    main_surface.blit(surface, (0, 0))
    return main_surface


def room_aim() -> pg.Surface:
    r1 = 75
    r2 = 150
    beta = 0.08 * pi
    x0, y0 = r2, r2

    x1 = r1 * cos(0)
    y1 = r1 * sin(0)
    x2 = r2 * cos(beta)
    y2 = r2 * sin(beta)
    x3 = r2 * cos(-beta)
    y3 = r2 * sin(-beta)

    x4 = r1 * cos(pi / 2)
    y4 = r1 * sin(pi / 2)
    x5 = r2 * cos(pi / 2 + beta)
    y5 = r2 * sin(pi / 2 + beta)
    x6 = r2 * cos(pi / 2 - beta)
    y6 = r2 * sin(pi / 2 - beta)

    surface = pg.Surface((2 * r2, 2 * r2), pg.SRCALPHA)
    pg.draw.polygon(surface, GREY, ((x0 + x1, y0 + y1), (x0 + x2, y0 + y2), (x0 + x3, y0 + y3)))
    pg.draw.polygon(surface, GREY, ((x0 - x1, y0 - y1), (x0 - x2, y0 - y2), (x0 - x3, y0 - y3)))
    pg.draw.polygon(surface, GREY, ((x0 + x4, y0 + y4), (x0 + x5, y0 + y5), (x0 + x6, y0 + y6)))
    pg.draw.polygon(surface, GREY, ((x0 - x4, y0 - y4), (x0 - x5, y0 - y5), (x0 - x6, y0 - y6)))
    return surface


def popup_window(w, h) -> pg.Surface:
    surface = pg.Surface((w, h), pg.SRCALPHA)
    surface.fill(POPUP_WINDOW_COLOR)
    transparent_color = (0, 0, 0, 0)
    pixels = pg.PixelArray(surface)
    r = h // 8
    for x in range(0, w // 2):
        for y in range(0, h // 2):
            if x <= r and y <= r and (x - r) * (x - r) + (y - r) * (y - r) >= r * r:
                pixels[x, y] = transparent_color
                pixels[w - 1 - x, y] = transparent_color
                pixels[x, h - 1 - y] = transparent_color
                pixels[w - 1 - x, h - 1 - y] = transparent_color
    surface = pixels.make_surface()
    return surface


def cooldown_window() -> pg.Surface:
    return popup_window(620, 240)


def health_window() -> pg.Surface:
    return popup_window(1710, 198)


def exit_button(color_1=(33, 51, 62), color_2=(200, 200, 200)) -> pg.Surface:
    r = 150
    d = int(r / sqrt(2))
    surface = pg.Surface((2 * r, 2 * r), pg.SRCALPHA)
    pg.draw.circle(surface, color_2, (r, r), r)
    pg.draw.circle(surface, color_1, (r, r), r - 14)
    pg.draw.line(surface, color_2, (r - d + 5, r + d - 5),
                 (r + d - 5, r - d + 5), 21)
    pg.draw.line(surface, color_2, (r - d + 5, r - d + 5),
                 (r + d - 5, r + d - 5), 21)
    return surface


def exit_button_pressed() -> pg.Surface:
    return exit_button(LIGHT_GREY, WHITE)


def paralyzing_explosion() -> pg.Surface:
    radius = 600
    d = 2 * radius
    edge_0 = radius - 15
    edge_1 = radius - 45
    edge_2 = radius - 165
    edge_3 = radius - 195
    edge_4 = radius - 225

    surface = pg.Surface((d, d), pg.SRCALPHA)
    arr = pg.PixelArray(surface)

    for x in range(0, radius):
        for y in range(0, radius):
            dist = hypot(x - radius, y - radius)
            if edge_0 < dist <= radius:
                alpha = int((radius - dist) / 15 * 255)
            elif edge_1 < dist <= edge_0:
                alpha = int((dist - edge_1) / 30 * 255)
            elif edge_2 < dist <= edge_1:
                alpha = int((edge_1 - dist) / 120 * 127)
            elif edge_3 < dist <= edge_2:
                alpha = int(127 + (edge_2 - dist) / 30 * 128)
            elif edge_4 < dist <= edge_3:
                alpha = int((dist - edge_4) / 30 * 255)
            elif dist <= edge_4:
                alpha = int((edge_4 - dist) / 375 * 255)
            else:
                alpha = 0
            color = (255, 255, 255, alpha)
            arr[x, y] = color
            arr[d - 1 - x, y] = color
            arr[x, d - 1 - y] = color
            arr[d - 1 - x, d - 1 - y] = color
    surface = arr.make_surface()
    return surface


def powerful_explosion() -> pg.Surface:
    radius = 600
    d = 2 * radius
    edge_0 = radius - 15
    edge_1 = radius - 30
    edge_2 = radius - 45
    edge_3 = radius - 90
    edge_4 = radius - 120
    edge_5 = radius - 150

    surface = pg.Surface((d, d), pg.SRCALPHA)
    arr = pg.PixelArray(surface)

    pink = np.array([211, 200, 201])
    white = np.array([255, 255, 255])
    color_delta = white - pink
    for x in range(0, radius):
        for y in range(0, radius):
            dist = hypot(x - radius, y - radius)
            if edge_0 < dist <= radius:
                alpha = int((radius - dist) / 15 * 220)
                color = (255, 255, 255, alpha)

            elif edge_1 < dist <= edge_0:
                color = white - color_delta * (edge_0 - dist) / 15
                color = (int(color[0]), int(color[1]), int(color[2]), 220)

            elif edge_2 < dist <= edge_1:
                alpha = int((dist - edge_2) / 15 * 220)
                color = (211, 200, 201, alpha)

            elif edge_3 < dist <= edge_2:
                alpha = int((edge_2 - dist) / 45 * 230)
                color = (211, 200, 201, alpha)

            elif edge_4 < dist <= edge_3:
                color = white - color_delta * (dist - edge_4) / 30
                color = (int(color[0]), int(color[1]), int(color[2]), 240)

            elif edge_5 < dist <= edge_4:
                color = white - color_delta * (edge_4 - dist) / 30
                color = (int(color[0]), int(color[1]), int(color[2]), 255)

            elif dist <= edge_5:
                alpha = int(110 + dist / 450 * 145)
                color = (211, 192, 191, alpha)

            else:
                color = (255, 255, 255, 0)
            arr[x, y] = color
            arr[d - 1 - x, y] = color
            arr[x, d - 1 - y] = color
            arr[d - 1 - x, d - 1 - y] = color
    surface = arr.make_surface()
    return surface


def teleportation() -> pg.Surface:
    radius = 300
    d = 2 * radius
    edge_0 = 240
    edge_1 = 225
    edge_3 = 75

    surface = pg.Surface((d, d), pg.SRCALPHA)
    arr = pg.PixelArray(surface)

    for x in range(0, radius):
        for y in range(0, radius):
            dist = hypot(x - radius, y - radius)
            if edge_0 < dist <= radius:
                alpha = int((radius - dist) / 60 * 155)
            elif edge_1 < dist <= edge_0:
                alpha = int(155 + (edge_0 - dist) / 15 * 100)
            elif edge_3 < dist <= edge_1:
                alpha = int((dist - edge_3) / 150 * 255)
            else:
                alpha = 0
            color = (255, 255, 255, alpha)
            arr[x, y] = color
            arr[d - 1 - x, y] = color
            arr[x, d - 1 - y] = color
            arr[d - 1 - x, d - 1 - y] = color
    surface = arr.make_surface()
    return surface


def room_background() -> pg.Surface:
    radius = 2100
    diameter = 2 * radius
    ring_width = 525
    surface = pg.Surface((diameter, diameter), pg.SRCALPHA)
    array = pg.PixelArray(surface)

    for x in range(0, radius):
        for y in range(0, radius):
            dist = hypot(x - radius, y - radius)
            if radius - ring_width < dist < radius:
                if dist > radius - 15:
                    color = WHITE
                else:
                    k = (dist - radius + ring_width) / ring_width
                    color = (192, 226, 250, int(255 * k))

                array[x, y] = color
                array[diameter - x - 1, y] = color
                array[x, diameter - y - 1] = color
                array[diameter - x - 1, diameter - y - 1] = color

    room_surface = array.make_surface()
    return room_surface


def room_glare() -> pg.Surface:
    radius = 400
    diameter = 2 * radius
    surface = pg.Surface((diameter, diameter), pg.SRCALPHA)
    array = pg.PixelArray(surface)

    for x in range(radius):
        for y in range(radius):
            if hypot(x - radius, y - radius) < radius:
                array[x, y] = ROOM_HIGHLIGHT_COLOR
                array[diameter - x - 1, y] = ROOM_HIGHLIGHT_COLOR
                array[x, diameter - y - 1] = ROOM_HIGHLIGHT_COLOR
                array[diameter - x - 1, diameter - y - 1] = ROOM_HIGHLIGHT_COLOR

    surface = array.make_surface()
    return surface


def side_button(alpha=70) -> pg.Surface:
    w, h = 180, 300
    surface = pg.Surface((w, h))
    surface.fill(COLOR_KEY)
    pg.draw.rect(surface, BLACK, pg.Rect(45, 0, 135, 300))
    pg.draw.rect(surface, BLACK, pg.Rect(0, 45, 45, 210))
    pg.draw.circle(surface, BLACK, (45, 45), 45)
    pg.draw.circle(surface, BLACK, (45, 255), 45)

    surface.set_colorkey(COLOR_KEY)
    surface.set_alpha(alpha)
    main_surface = pg.Surface((w, h), pg.SRCALPHA)
    main_surface.blit(surface, (0, 0))
    return main_surface


def side_button_pressed() -> pg.Surface:
    return side_button(alpha=125)


def start_menu_caption() -> pg.Surface:
    color = (125, 199, 240, 200)
    w, h = 2400, 480
    r = h // 2
    surface = pg.Surface((2400, 480), pg.SRCALPHA)
    array = pg.PixelArray(surface)

    for x in range(w // 2):
        for y in range(h // 2):
            if x >= r or y >= r or hypot(x - r, y - r) < r:
                array[x, y] = color
                array[w - x - 1, y] = color
                array[x, h - y - 1] = color
                array[w - x - 1, h - y - 1] = color

    surface = array.make_surface()
    return surface


def upgrade_caption_eng(text=ENG_UPG_CAPTION) -> pg.Surface:
    w, h = 2220, 210
    surface = pg.Surface((w, h))
    surface.fill(COLOR_KEY)
    pg.draw.rect(surface, WHITE, surface.get_rect(), 0, 30)
    pg.font.init()
    font = pg.font.Font(FONT_1, 156)
    text = font.render(text, True, UPG_LABEL_COLOR)
    surface.blit(text, ((w - text.get_width()) // 2, (h - text.get_height()) // 2 + 8))
    surface.set_colorkey(COLOR_KEY)
    main_surface = pg.Surface((w, h), pg.SRCALPHA)
    main_surface.blit(surface, (0, 0))
    return main_surface


def upgrade_caption_rus() -> pg.Surface:
    return upgrade_caption_eng(text=RUS_UPG_CAPTION)


def upgrade_button(w=660, bg_color=(230, 230, 230)) -> pg.Surface:
    h = 1380
    w2 = w // 2
    surface = pg.Surface((w, h))
    surface.fill(COLOR_KEY)
    pg.draw.rect(surface, bg_color, surface.get_rect(), 0, 30)
    color_1 = np.array(UPG_CIRCLE_COLOR_1, dtype=float)
    color_2 = np.array(UPG_CIRCLE_COLOR_3, dtype=float)
    color_delta = color_2 - color_1
    for i in range(24):
        color = color_1 + color_delta * i / 23
        pg.draw.circle(surface, color, (w2, 198), 99 - i)
    pg.draw.polygon(surface, UPG_ARROW_COLOR,
                    ((w2, 150), (w2 + 33, 195), (w2 + 12, 195), (w2 + 12, 240),
                     (w2 - 12, 240), (w2 - 12, 195), (w2 - 33, 195)))
    surface.set_colorkey(COLOR_KEY)
    main_surface = pg.Surface((w, h), pg.SRCALPHA)
    main_surface.blit(surface, (0, 0))
    return main_surface


def upgrade_button_pressed() -> pg.Surface:
    return upgrade_button(660, WHITE)


def upgrade_button_wide() -> pg.Surface:
    return upgrade_button(900)


def upgrade_button_wide_pressed() -> pg.Surface:
    return upgrade_button(900, WHITE)


def play_button() -> pg.Surface:
    a = 72 * 5
    b = 56 * 5
    surface = pg.Surface((2 * a, 2 * b))
    surface.fill(RED)
    pg.draw.ellipse(surface, (176, 213, 231), surface.get_rect())

    dots = np.array([[-13, -24], [-13, 24], [13, 0.]]) * 5
    edge_dots = np.array([[-18, -37], [-18, 37], [21, 0.]]) * 5
    triangle_pos = np.array([a, b])

    pg.draw.polygon(surface, WHITE, edge_dots + triangle_pos)
    pg.draw.polygon(surface, TRIANGLE_COLOR_MAX, dots + triangle_pos)

    surface.set_colorkey(RED)
    main_surface = pg.Surface((2 * a, 2 * b), pg.SRCALPHA)
    main_surface.blit(surface, (0, 0))
    return main_surface


#save(play_button(), 'play_button')
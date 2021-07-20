import os
import json
import pygame as pg

from components.utils import HF, H
from data.constants import *


def _init_sniper_bullet_surface() -> pg.Surface:
    w = HF(36.382)
    h = HF(21.26)
    edge = H(2)
    surface = pg.Surface((w, h), pg.SRCALPHA)
    pg.draw.ellipse(surface, WHITE, pg.Rect(0, 0, w, h))
    pg.draw.ellipse(surface, RED, pg.Rect(edge, edge, w - 2 * edge, h - 2 * edge))
    pg.draw.circle(surface, RED_GLARE_1, (w // 4, w // 4), H(3))
    return surface


def _init_bullets() -> dict:
    bullets = {}
    root_dir = os.path.abspath(os.path.dirname(__file__))
    all_files = [f for f in os.listdir(root_dir) if f.endswith('.json')]

    for file in all_files:
        name = file.split('.')[0].replace('_', ' ')
        file_path = os.path.join(root_dir, file)
        with open(file_path, 'r') as f:
            bullets[name] = json.load(f)
            bullets[name]["radius"] = HF(bullets[name]["radius"])
            bullets[name]["size"] = HF(bullets[name]["size"])
            if name == "sniper bullet":
                bullets[name]["circles"] = _init_sniper_bullet_surface()
    return bullets


BULLETS = _init_bullets()


__all__ = ["BULLETS"]

import pygame as pg

from data.colors import WHITE
import data.languages.english as eng
import data.languages.russian as rus
from map import Map
from data.config import K


def create_caption(language):
    pg.font.init()
    font = pg.font.SysFont('Calibri', int(round(56 * K)), True)
    if language == 'English':
        text = eng.MAPWINDOW_CAPTION
    else:
        text = rus.MAPWINDOW_CAPTION
    return font.render(text, True, WHITE)


class MapWindow:
    def __init__(self):
        self.caption = None
        self.caption_pos = (int(round(584 * K)), int(round(176 * K)))
        self.map = Map()
        self.set_language("English")

    def set_language(self, language):
        self.caption = create_caption(language)

    def reset(self):
        self.map.reset()

    def update(self, dt):
        self.map.update(dt)

    def draw(self, screen):
        screen.blit(self.caption, self.caption_pos)
        self.map.draw(screen)
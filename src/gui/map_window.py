import pygame as pg

from data.colors import WHITE
import data.languages.english as eng
import data.languages.russian as rus
from gui.game_map import GameMap


def create_caption(language):
    pg.font.init()
    font = pg.font.SysFont('Calibri', 56, True)
    if language == 'English':
        text = eng.MAPWINDOW_CAPTION
    else:
        text = rus.MAPWINDOW_CAPTION
    return font.render(text, True, WHITE)


class MapWindow:
    caption = None
    game_map = GameMap()

    def __init__(self):
        self.set_language("English")

    def set_language(self, language):
        self.caption = create_caption(language)

    def reset(self):
        self.game_map.reset()

    def update(self, dt):
        self.game_map.update(dt)

    def draw(self, screen):
        screen.blit(self.caption, (584, 176))
        self.game_map.draw(screen)
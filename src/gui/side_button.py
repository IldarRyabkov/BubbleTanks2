import pygame as pg

from data.colors import WHITE
from data.paths import FONT_2, SIDE_BUTTON, SIDE_BUTTON_CLICKED
import data.languages.english as eng
import data.languages.russian as rus


BUTTON_TEXT = {
    "stats_button": {
        "English": eng.STATSBUTTON_TEXT,
        "Russian": rus.STATSBUTTON_TEXT
    },
    "options_button": {
        "English": eng.OPTIONSBUTTON_TEXT,
        "Russian": rus.OPTIONSBUTTON_TEXT
    },
    "map_button": {
    "English": eng.MAPBUTTON_TEXT,
    "Russian": rus.MAPBUTTON_TEXT
    }
}


class SideButton:
    def __init__(self,
                 x: int,
                 y: int,
                 button_type: str,
                 clicked: bool):
        self.x = x
        self.y = y
        self.w = 96
        self.h = 160
        self.clicked = clicked
        self.type = button_type
        self.text = None
        self.text_pos = None
        self.bg = {False: pg.image.load(SIDE_BUTTON).convert_alpha(),
                   True: pg.image.load(SIDE_BUTTON_CLICKED).convert_alpha()}

    def set_language(self, language):
        pg.font.init()
        text = BUTTON_TEXT[self.type][language]
        size = 29 if len(text) >= 10 else 35
        font = pg.font.Font(FONT_2, size)
        text = font.render(text, True, WHITE)
        self.text = pg.transform.rotate(text, 90)
        self.text_pos = (self.x + (self.w - self.text.get_width()) // 2,
                         self.y + (self.h - self.text.get_height()) // 2)

    def cursor_on_button(self, pos):
        return abs(self.x - pos[0]) <= self.w and abs(self.y - pos[1]) <= self.h

    def draw(self, screen):
        screen.blit(self.bg[self.clicked], (self.x, self.y))
        screen.blit(self.text, self.text_pos)
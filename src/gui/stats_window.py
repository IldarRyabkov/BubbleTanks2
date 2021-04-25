import pygame as pg

from data.stats_window import PLAYER_BODIES
from data.colors import WHITE, PAUSEMENU_PLAYER_BG
from data.paths import FONT_2
import data.languages.english as eng
import data.languages.russian as rus
from gui.text_box import TextBox
from objects.body import Body


def create_captions(language):
    pg.font.init()
    font_1 = pg.font.SysFont('Calibri', 56, True)
    font_2 = pg.font.SysFont('Calibri', 45, True)
    if language == 'English':
        captions_text = eng.STATSWINDOW_CAPTIONS
    else:
        captions_text = rus.STATSWINDOW_CAPTIONS
    captions = list()
    captions.append(font_1.render(captions_text[0], True, WHITE))
    captions.append(font_2.render(captions_text[1], True, WHITE))
    captions.append(font_2.render(captions_text[2], True, WHITE))
    return captions


class StatsWindow:
    tank_name = None
    tank_desc = None
    tank_body = None
    tank_data = None
    captions = None

    def __init__(self):
        self.set_language("English")

    def set_language(self, language):
        self.captions = create_captions(language)
        if language == 'English':
            self.tank_data = eng.UPGRADE_TEXT
        else:
            self.tank_data = rus.UPGRADE_TEXT

    def set_tank_name(self, player_state):
        pg.font.init()
        font = pg.font.SysFont('Calibri', 42, True)
        self.tank_name = font.render(self.tank_data[player_state][0], True, WHITE)

    def set_tank_desc(self, player_state):
        self.tank_desc = (TextBox(self.tank_data[player_state][3], FONT_2, 32, False, WHITE, (192, 328), False),
                          TextBox(self.tank_data[player_state][1], 'Calibri',  35, True,  WHITE, (192, 656), False),
                          TextBox(self.tank_data[player_state][2], 'Calibri',  35, True,  WHITE, (688, 656), False),
                          TextBox(self.tank_data[player_state][4], FONT_2, 32, False, WHITE, (192, 741), False),
                          TextBox(self.tank_data[player_state][5], FONT_2, 32, False, WHITE, (688, 741), False))

    def set_player_stats(self, player_state):
        self.set_tank_name(player_state)
        self.set_tank_desc(player_state)
        self.tank_body = Body(PLAYER_BODIES[player_state])

    def update(self, dt):
        self.tank_body.update(952, 416, dt, (9000, 416))

    def draw_captions(self, screen):
        screen.blit(self.captions[0], (512, 176))
        screen.blit(self.captions[1], (192, 592))
        screen.blit(self.captions[2], (688, 592))

    def draw_tank_name(self, screen):
        screen.blit(self.tank_name, (192, 272))

    def draw_tank_desc(self, screen):
        for text in self.tank_desc:
            text.draw(screen)

    @staticmethod
    def draw_player_background(screen):
        pg.draw.circle(screen, WHITE, (952, 416), 149)
        pg.draw.circle(screen, PAUSEMENU_PLAYER_BG, (952, 416), 142)

    def draw(self, screen):
        self.draw_captions(screen)
        self.draw_tank_name(screen)
        self.draw_tank_desc(screen)
        self.draw_player_background(screen)
        self.tank_body.draw(screen)
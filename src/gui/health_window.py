import pygame as pg

from gui.popup_window import PopupWindow
from gui.status_bar import StatusBar
from data.paths import HEALTH_WINDOW_BG
from data.config import SCR_H, SCR_W
from data.colors import WHITE
import data.languages.english as eng
import data.languages.russian as rus


class HealthWindow(PopupWindow):
    def __init__(self):
        PopupWindow.__init__(self, 184, SCR_H, SCR_W-368, 106, -1.12, 1250, HEALTH_WINDOW_BG)
        self.max_health = 75
        self.status_bar = StatusBar(self.x+16, self.y+56, self.width-32, 32, self.max_health)
        self.tank_names = eng.TANK_NAMES
        self.bubbles_texts = eng.BUBBLES_TEXTS
        self.tank_name_label = None
        self.bubbles_label = None
        pg.font.init()
        self.font = pg.font.SysFont('calibri', 30, True)

    def set_language(self, language):
        if language == 'English':
            self.tank_names = eng.TANK_NAMES
            self.bubbles_texts = eng.BUBBLES_TEXTS
        else:
            self.tank_names = rus.TANK_NAMES
            self.bubbles_texts = rus.BUBBLES_TEXTS

    def set_status_bar(self, player_state, max_health, health):
        value = max_health if player_state[0] == 5 else health
        self.status_bar.set_max_value(max_health)
        self.status_bar.set_value(value)

    def set_bubbles_label(self, health, player_state):
        if player_state[0] != 5:
            bubbles_text = str(self.max_health - health) + self.bubbles_texts[0]
        else:
            bubbles_text = self.bubbles_texts[1]
        self.bubbles_label = self.font.render(bubbles_text, True, WHITE)

    def set_tank_name_label(self, player_state):
        self.tank_name_label = self.font.render(self.tank_names[player_state], True, WHITE)

    def activate(self, health, player_state):
        super().activate()
        if player_state[0] != 5:
            self.status_bar.set_value(health)
            self.set_bubbles_label(health, player_state)

    def reset(self):
        super().reset()
        self.status_bar.move_to(self.x + 16, self.y + 56)

    def set(self, player_state, player_health, player_max_health):
        self.max_health = player_max_health
        self.set_status_bar(player_state, player_max_health, player_health)
        self.set_tank_name_label(player_state)
        self.set_bubbles_label(player_health, player_state)

    def update(self, dt):
        self.update_state(dt)
        self.status_bar.move_to(self.x + 16, self.y + 56)

    def draw(self, screen):
        if self.is_on_screen():
            screen.blit(self.background, (self.x, int(self.y)))
            self.status_bar.draw(screen)
            x = SCR_W-self.x-23 - self.bubbles_label.get_size()[0]
            screen.blit(self.bubbles_label, (int(x), int(self.y) + 16))
            screen.blit(self.tank_name_label, (self.x + 23, int(self.y) + 16))
import pygame as pg

from gui.status_bar import StatusBar
from gui.popup_window import PopupWindow
from data.config import SCR_W
from data.paths import COOLDOWN_WINDOW_BG
import data.languages.english as eng
import data.languages.russian as rus


class CooldownWindow(PopupWindow):
    """Window that shows status bars for player
    shooting cooldown and player superpower cooldown.
    """
    def __init__(self):
        super().__init__(SCR_W - 264, -96, 248, 96, 1.12, 1000, COOLDOWN_WINDOW_BG)
        self.shooting_status_bar = StatusBar(self.x + 56, self.y + 11, self.width - 72, 32, 300)
        self.superpower_status_bar = StatusBar(self.x + 56, self.y + 53, self.width - 72, 32, 0)
        self.label_1 = None
        self.label_2 = None
        self.set_language("English")

    def set_language(self, language):
        pg.font.init()
        font = pg.font.SysFont('Calibri', 27, True)
        if language == 'English':
            texts = eng.WINDOW_COOLDOWN_LABELS
        else:
            texts = rus.WINDOW_COOLDOWN_LABELS
        self.label_1 = font.render(texts[0], True, (255, 255, 255))
        self.label_2 = font.render(texts[1], True, (255, 255, 255))

    def reset(self):
        super().reset()
        self.shooting_status_bar.move_to(self.x + 56, self.y + 11)
        self.superpower_status_bar.move_to(self.x + 56, self.y + 53)

    def set(self, cooldown_time_1, cooldown_time_2):
        self.shooting_status_bar.set_max_value(cooldown_time_1)
        self.shooting_status_bar.set_value(0)
        self.superpower_status_bar.set_max_value(cooldown_time_2)
        self.superpower_status_bar.set_value(0)

    def update(self, dt, player):
        self.update_state(dt)
        shooting_active = player.is_shooting and not player.invisible[0]
        superpower_active = (player.superpower.on and
                             player.superpower.name not in
                             ("NoneSuperPower", "Ghost", "Shurikens"))
        if shooting_active or superpower_active:
            self.activate()
        self.shooting_status_bar.active = shooting_active
        self.shooting_status_bar.update_value(dt)
        self.shooting_status_bar.move_to(self.x + 56, self.y + 11)
        self.superpower_status_bar.active = superpower_active
        self.superpower_status_bar.update_value(dt)
        self.superpower_status_bar.move_to(self.x + 56, self.y + 53)

    def draw(self, screen):
        if self.is_on_screen():
            screen.blit(self.background, (self.x, int(self.y)))
            screen.blit(self.label_1, (self.x+16, int(self.y)+14))
            screen.blit(self.label_2, (self.x+16, int(self.y)+56))
            self.shooting_status_bar.draw(screen)
            self.superpower_status_bar.draw(screen)

import pygame as pg
import sys

from data.config import SCR_W2, SCR_H2, SCR_SIZE
from data.paths import FONT_1, FONT_2
from data.colors import WHITE
from objects.bubble import Bubble
from gui.long_button import LongButton
from gui.text import Text
from utils import H
from data.gui_texts import VICTORY_MENU_TEXTS


class VictoryMenu:
    """Victory menu opens when player defeated the Final Boss.
    It has a button to return to the Main menu. """
    def __init__(self):
        self.running = True
        self.bg_surface = pg.Surface(SCR_SIZE)
        self.mask = pg.Surface(SCR_SIZE)
        self.mask.set_alpha(195)

        self.quit_button = LongButton(SCR_W2 - H(128), H(688))

        self.labels = (
            Text(SCR_W2, H(128), FONT_1, H(90), WHITE, True),
            Text(SCR_W2, H(232), FONT_2, H(48), WHITE, True),
        )
        self.bubbles = (
            Bubble(SCR_W2 - H(192), SCR_H2 - H(80), 0, 0, "big"),
            Bubble(SCR_W2 + H(192), SCR_H2 - H(80), 0, 0, "big"),
            Bubble(SCR_W2, SCR_H2 - H(80), 0, 0, "big")
        )
        for bubble in self.bubbles:
            bubble.vel = 0

    def set_language(self, language):
        for i, label in enumerate(self.labels):
            label.set_text(VICTORY_MENU_TEXTS[language]["labels"][i])
        self.quit_button.set_text(VICTORY_MENU_TEXTS[language]["button"])

    def set(self):
        """Method is called when Victory menu starts running. """
        self.running = True

    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif (e.type == pg.MOUSEBUTTONDOWN and e.button == pg.BUTTON_LEFT
                  and self.quit_button.cursor_on_button):
                self.running = False

    def update(self, dt):
        for bubble in self.bubbles:
            bubble.update_body(dt)

    def draw(self, screen):
        screen.blit(self.mask, (0, 0))
        for label in self.labels:
            label.draw(screen)
        self.quit_button.draw(screen)
        for bubble in self.bubbles:
            bubble.draw(screen)
        pg.display.update()

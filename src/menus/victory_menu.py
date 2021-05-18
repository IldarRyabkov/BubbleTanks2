import pygame as pg
import sys

from constants import *
from data.paths import FONT_1, FONT_3
from bubble import Bubble
from gui.text_button import TextButton
from gui.text import Text
from utils import H
from data.gui_texts import VICTORY_MENU_LABELS, EXIT_TO_MENU_TEXT


class VictoryMenu:
    """Victory menu opens when player defeated the Final Boss.
    It has a button to return to the Main menu. """
    def __init__(self, game):
        self.game = game

        self.running = True

        self.bg_surface = pg.Surface(SCR_SIZE)
        self.mask = pg.Surface(SCR_SIZE)
        self.mask.set_alpha(195)

        self.exit_button = TextButton(SCR_W2, H(688), EXIT_TO_MENU_TEXT,
                                      FONT_3, H(52), 200, self.game.sound_player)
        self.labels = (
            Text(SCR_W2, H(128), FONT_1, H(90), WHITE, 1),
            Text(SCR_W2, H(232), FONT_1, H(50), WHITE, 1),
        )
        self.bubbles = (
            Bubble(SCR_W2 - H(192), SCR_H2 - H(80), 0, 0, "big"),
            Bubble(SCR_W2 + H(192), SCR_H2 - H(80), 0, 0, "big"),
            Bubble(SCR_W2, SCR_H2 - H(80), 0, 0, "big")
        )
        for bubble in self.bubbles:
            bubble.vel = 0

    def reset(self):
        self.exit_button.reset()

    def set_language(self, language):
        for i, label in enumerate(self.labels):
            label.set_text(VICTORY_MENU_LABELS[language][i])
        self.exit_button.set_language(language)

    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if e.type == pg.MOUSEBUTTONDOWN and e.button == pg.BUTTON_LEFT:
                self.running = not self.exit_button.clicked

    def update(self, dt):
        self.game.update_scaling_objects(dt)
        for bubble in self.bubbles:
            bubble.update_body(dt)
        self.exit_button.update(dt)

    def draw(self, screen):
        """Draws all objects in the background and victory menu items. """
        screen.blit(self.bg_surface, (0, 0))
        self.game.draw_foreground()
        screen.blit(self.mask, (0, 0))
        for label in self.labels:
            label.draw(screen)
        self.exit_button.draw(screen)
        for bubble in self.bubbles:
            bubble.draw(screen)
        pg.display.update()

    def run(self):
        """Victory menu loop which starts after the Boss is defeated. """
        self.game.draw_background(self.bg_surface)

        self.running = True
        dt = 0
        while self.running:
            self.update(dt)
            self.draw(self.game.screen)

            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
            self.handle_events()

        self.game.running = False

__all__ = ["VictoryMenu"]

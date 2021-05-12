import pygame as pg
import sys
from random import uniform

from objects.bubble import Bubble
from gui.text import Text
from gui.main_menu_button import MainMenuButton
from gui.settings_window import SettingsWindow
from data.config import *
from data.config import (MAIN_MENU_ANIMATION_TIME as ANIMATION_TIME,
                         MAIN_MENU_AWAKE_TIME as AWAKE_TIME)
from data.colors import WHITE
from data.gui_texts import MAIN_MENU_CAPTION, PLAY_BUTTON_LABEL, SETTINGS_BUTTON_LABEL
from data.paths import *
from utils import H, HF


class MainMenu:
    """Main menu of the game, where player can choose
    language and start a new game.
    """
    def __init__(self, game):
        self.game = game
        self.running = True

        self.bubbles = []
        self.bubbles_time = 0

        self.settings_window = SettingsWindow(self, game)

        self.play_button = MainMenuButton(SCR_W2, PLAY_BUTTON_LABEL, H(84),
                                          PLAY_BUTTON, self.game.sound_player, 1.3)

        self.settings_button = MainMenuButton(SCR_W2 - H(360), SETTINGS_BUTTON_LABEL, H(63),
                                              SETTINGS_BUTTON, self.game.sound_player, 1)

        self.caption = Text(SCR_W2, H(405), FONT_1, H(112), WHITE, 1)

        self.bg = pg.image.load(BG).convert()
        self.bg = pg.transform.scale(self.bg, SCR_SIZE)

        self.caption_bg = pg.image.load(START_MENU_CAPTION_BG).convert_alpha()
        self.caption_bg = pg.transform.scale(self.caption_bg, (H(1280), H(280)))

        self.language = "English"
        self.set_language(self.language)

    def set_language(self, language):
        self.language = language
        self.caption.set_text(MAIN_MENU_CAPTION[language])
        self.settings_window.set_language(language)
        self.play_button.set_language(language)
        self.settings_button.set_language(language)

    def handle_button_press(self, button):
        self.game.sound_player.reset()
        self.game.sound_player.play_sound(UI_CLICK)
        button.clicked = True
        self.run_animation(CLOSE)

        if button.name == "play_button":
            self.running = False
        else:
            self.settings_window.run()
            self.run_animation(OPEN)

    def handle_events(self, state=WAIT):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if state == WAIT and event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                if self.play_button.clicked:
                    self.running = False
                    self.run_animation(CLOSE)

                elif self.settings_button.clicked:
                    self.run_animation(CLOSE)
                    self.settings_window.run()
                    self.run_animation(OPEN)

    def update_caption_alpha(self, state, time_elapsed):
        """Updates alpha-value of caption and its background,
        based on Main menu state.
        """
        alpha = 255 * time_elapsed if state == OPEN else 255 - 255 * time_elapsed
        self.caption.set_alpha(alpha)
        self.caption_bg.set_alpha(alpha)

    def update_bubbles(self, dt):
        self.bubbles_time = min(self.bubbles_time + dt, 200)
        if self.bubbles_time == 200:
            self.bubbles_time = 0
            new_bubble = Bubble(uniform(0, SCR_W), SCR_H + HF(13), 0, 0, "tiny")
            new_bubble.vel = -uniform(HF(0.32), HF(0.96))
            self.bubbles.append(new_bubble)

        for bubble in self.bubbles:
            bubble.y += bubble.vel * dt
            bubble.update_body(dt)

        self.bubbles = list(filter(lambda b: b.y > -HF(13), self.bubbles))

    def update(self, dt, state=WAIT, time_elapsed=0):
        self.update_bubbles(dt)
        self.play_button.update(dt, state, time_elapsed)
        self.settings_button.update(dt, state, time_elapsed)
        if state != WAIT:
            self.update_caption_alpha(state, time_elapsed)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        for bubble in self.bubbles:
            bubble.draw(screen, 0, 0)

        screen.blit(self.caption_bg, (SCR_W2 - H(640), H(302)))

        self.caption.draw(screen)
        self.play_button.draw(screen)
        self.settings_button.draw(screen)

        pg.display.update()

    def awake(self):
        dt = time = 0
        mask = pg.Surface(SCR_SIZE)
        alpha = 255
        self.game.clock.tick()

        while time <= AWAKE_TIME:
            alpha = max(0, alpha - 255 * dt/AWAKE_TIME)
            mask.set_alpha(alpha)

            self.game.screen.blit(self.bg, (0, 0))
            self.game.screen.blit(mask, (0, 0))
            pg.display.update()

            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
            time += dt

    def run_animation(self, state):
        """Main menu animation loop which begins when
        the main menu starts opening or closing.
        """
        if state == OPEN:
            self.play_button.reset()
            self.settings_button.reset()

        self.game.clock.tick()
        dt = animation_time = 0
        while animation_time <= ANIMATION_TIME:
            self.handle_events(state)
            self.update(dt, state, animation_time/ANIMATION_TIME)
            self.draw(self.game.screen)
            self.game.fps_manager.update(dt)
            dt = self.game.clock.tick()
            animation_time += dt

    def run(self):
        self.game.sound_player.play_music(START_MUSIC)

        self.running = True
        self.bubbles = []
        self.bubbles_time = 0

        self.awake()
        self.run_animation(OPEN)

        self.game.clock.tick()
        dt = 0
        while self.running:
            self.handle_events()
            self.update(dt)
            self.draw(self.game.screen)
            self.game.fps_manager.update(dt)
            dt = self.game.clock.tick()


__all__ = ["MainMenu"]

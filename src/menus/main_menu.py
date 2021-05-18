import pygame as pg
import sys
from random import uniform

from bubble import Bubble
from gui.text import Text
from gui.text_button import *
from gui.slider import Slider
from gui.main_menu_caption import MainMenuCaption
from gui.main_menu_button import MainMenuButton
from data.config import *
from data.resolution import *
from data.colors import WHITE
from data.gui_texts import *
from data.paths import *
from utils import H, HF


class MainMenu:
    """Main menu of the game, where player can change
    game settings and start a new game.
    """
    def __init__(self, game):
        self.game = game
        self.running = True
        self.state = State.MAIN_MENU

        sp = self.game.sound_player
        resolutions = get_available_resolutions()

        self.res_buttons = []
        for i in range(len(resolutions)):
            h = H(240 + 671/len(resolutions)*i)
            button = TextButton(SCR_W2, h, resolutions[i], FONT_3, H(52), 200, sp, H(300))
            button.set_text(button.texts)
            self.res_buttons.append(button)

        self.lang_buttons = []
        for i in range(len(LANGUAGES)):
            h = H(440 + 150*i)
            button = TextButton(SCR_W2, h, LANGUAGES[i], FONT_3, H(62), 200, sp, H(300))
            button.set_text(button.texts)
            self.lang_buttons.append(button)

        self.resolution_warning = Text(SCR_W2, H(890), FONT_3, H(34), WHITE, 1)

        self.lang_window_button = DoubleTextButton(SCR_W2, H(325), LANGUAGE_LABEL, LANGUAGES[0], FONT_3, H(56), 200, sp)
        self.res_window_button = DoubleTextButton(SCR_W2, H(415), RESOLUTION_LABEL, resolutions[cur_res_index()], FONT_3, H(56), 200, sp)

        self.slider = Slider(SCR_W2, H(516), MASTER_VOLUME_TEXT, FONT_3, H(56), sp)
        self.slider.set_value(sp.master_volume)

        self.exit_button = TextButton(SCR_W2, H(610), EXIT_TO_DESKTOP_TEXT, FONT_3, H(56), 200, sp, H(400))
        self.back_button = TextButton(SCR_W2, H(700), BACK_BUTTON_TEXT, FONT_3, H(56), 200, sp, H(200))
        self.yes_button = TextButton(SCR_W2 - H(120), SCR_H2 + H(100), YES_BUTTON_TEXT, FONT_3, H(70), 200, sp, H(200))
        self.no_button = TextButton(SCR_W2 + H(120), SCR_H2 + H(100), NO_BUTTON_TEXT, FONT_3, H(70), 200, sp, H(200))

        self.play_button = MainMenuButton(SCR_W2, PLAY_BUTTON_LABEL, H(84), PLAY_BUTTON_BG, sp, 1.3)
        self.settings_button = MainMenuButton(SCR_W2 - H(360), SETTINGS_BUTTON_LABEL, H(63), SETTINGS_BUTTON_BG, sp, 1)

        self.caption = MainMenuCaption()

        self.bg = pg.image.load(BG).convert()
        self.bg = pg.transform.scale(self.bg, SCR_SIZE)

        self.bubbles = []
        self.bubbles_time = 0

        self.language = ENGLISH
        self.set_language(self.language)

    def set_language(self, language):
        self.language = language
        self.caption.set_format(self.state, MAIN_MENU_CAPTIONS[language][self.state])
        self.resolution_warning.set_text(RESOLUTION_WARNING[language])
        self.lang_window_button.set_language(language)
        self.res_window_button.set_language(language)
        self.slider.set_language(language)
        self.back_button.set_language(language)
        self.exit_button.set_language(language)
        self.yes_button.set_language(language)
        self.no_button.set_language(language)
        self.play_button.set_language(language)
        self.settings_button.set_language(language)

    def set_state(self, state):
        duration = 1000 if self.state == State.MAIN_MENU else 300
        self.run_animation(CLOSE, duration)

        self.state = state
        self.caption.set_format(state, MAIN_MENU_CAPTIONS[self.language][state])

        if state == State.MAIN_MENU:
            self.play_button.reset()
            self.settings_button.reset()
        elif state == State.SETTINGS:
            self.lang_window_button.reset()
            self.res_window_button.reset()
            self.slider.reset()
            self.exit_button.reset()
            self.back_button.reset()
        elif state == State.LANGUAGES:
            for button in self.lang_buttons:
                button.reset()
        elif state == State.RESOLUTIONS:
            for button in self.res_buttons:
                button.reset()
        elif state == State.EXIT_CONFIRMATION:
            self.yes_button.reset()
            self.no_button.reset()

        duration = 1000 if self.state == State.MAIN_MENU else 400
        self.run_animation(OPEN, duration)

    def handle_mouse_down(self, e_type):
        if self.state == State.MAIN_MENU:
            if self.play_button.clicked:
                self.running = False
                self.run_animation(CLOSE, 1700)
                self.play_button.reset()
                self.settings_button.reset()
            elif self.settings_button.clicked:
                self.set_state(State.SETTINGS)

        elif self.state == State.SETTINGS:
            self.slider.handle(e_type)
            if self.lang_window_button.clicked:
                self.set_state(State.LANGUAGES)
            elif self.res_window_button.clicked:
                self.set_state(State.RESOLUTIONS)
            elif self.back_button.clicked:
                self.set_state(State.MAIN_MENU)
            elif self.exit_button.clicked:
                self.set_state(State.EXIT_CONFIRMATION)

        elif self.state == State.EXIT_CONFIRMATION:
            if self.yes_button.clicked:
                self.run_animation(CLOSE)
                pg.quit()
                sys.exit()
            elif self.no_button.clicked:
                self.set_state(State.MAIN_MENU)

        elif self.state == State.LANGUAGES:
            for button in self.lang_buttons:
                if button.clicked:
                    new_language = LANGUAGES.index(button.texts)
                    self.set_language(new_language)
                    self.lang_window_button.set_value(button.texts)
                    self.set_state(State.SETTINGS)
                    break

        elif self.state == State.RESOLUTIONS:
            for button in self.res_buttons:
                if button.clicked:
                    self.res_window_button.set_value(button.texts)
                    new_resolution = raw_resolution(button.texts)
                    if list(SCR_SIZE) != new_resolution:
                        save_resolution(new_resolution)
                    self.set_state(State.SETTINGS)
                    break

    def handle_mouse_up(self, e_type):
        if self.state == State.SETTINGS:
            self.slider.handle(e_type)

    def handle_events(self, animation_state=WAIT):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if animation_state == WAIT:
                if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.game.sound_player.play_sound(UI_CLICK)
                    if self.state in (State.SETTINGS, State.EXIT_CONFIRMATION):
                        self.set_state(State.MAIN_MENU)
                    elif self.state == State.MAIN_MENU:
                        self.set_state(State.EXIT_CONFIRMATION)
                    else:
                        self.set_state(State.SETTINGS)

                elif e.type == pg.MOUSEBUTTONUP and e.button == pg.BUTTON_LEFT:
                    self.handle_mouse_up(e.type)
                elif e.type == pg.MOUSEBUTTONDOWN and e.button == pg.BUTTON_LEFT:
                    self.handle_mouse_down(e.type)

    def update_bubbles(self, dt):
        self.bubbles_time = min(self.bubbles_time + dt, 150)
        if self.bubbles_time == 150:
            self.bubbles_time = 0
            new_bubble = Bubble(uniform(0, SCR_W), SCR_H + HF(13), 0, 0, "tiny")
            new_bubble.vel = -uniform(HF(0.32), HF(0.96))
            self.bubbles.append(new_bubble)

        for bubble in self.bubbles:
            bubble.y += bubble.vel * dt
            bubble.update_body(dt)

        self.bubbles = list(filter(lambda b: b.y > -HF(13), self.bubbles))

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        self.update_bubbles(dt)

        if animation_state != WAIT:
            self.caption.update_alpha(animation_state, time_elapsed)
            if self.state == State.RESOLUTIONS:
                self.resolution_warning.set_alpha(self.caption.alpha)

        if self.state == State.MAIN_MENU:
            self.play_button.update(dt, animation_state, time_elapsed)
            self.settings_button.update(dt, animation_state, time_elapsed)

        elif self.state == State.SETTINGS:
            self.lang_window_button.update(dt, animation_state, time_elapsed)
            self.res_window_button.update(dt, animation_state, time_elapsed)
            self.back_button.update(dt, animation_state, time_elapsed)
            self.exit_button.update(dt, animation_state, time_elapsed)
            self.slider.update(dt, animation_state, time_elapsed)
            if animation_state == WAIT and self.slider.pressed:
                self.game.sound_player.set_music_volume(self.slider.value)
                self.game.sound_player.set_sound_volume(self.slider.value)

        elif self.state == State.EXIT_CONFIRMATION:
            self.yes_button.update(dt, animation_state, time_elapsed)
            self.no_button.update(dt, animation_state, time_elapsed)

        elif self.state == State.LANGUAGES:
            for button in self.lang_buttons:
                button.update(dt, animation_state, time_elapsed)

        elif self.state == State.RESOLUTIONS:
            for button in self.res_buttons:
                button.update(dt, animation_state, time_elapsed)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        for bubble in self.bubbles:
            bubble.draw(screen, 0, 0)
        self.caption.draw(screen)

        if self.state == State.MAIN_MENU:
            self.play_button.draw(screen)
            self.settings_button.draw(screen)

        elif self.state == State.SETTINGS:
            self.slider.draw(screen)
            self.lang_window_button.draw(screen)
            self.res_window_button.draw(screen)
            self.back_button.draw(screen)
            self.exit_button.draw(screen)

        elif self.state == State.EXIT_CONFIRMATION:
            self.yes_button.draw(screen)
            self.no_button.draw(screen)

        elif self.state == State.LANGUAGES:
            for button in self.lang_buttons:
                button.draw(screen)

        elif self.state == State.RESOLUTIONS:
            for button in self.res_buttons:
                button.draw(screen)
            self.resolution_warning.draw(screen)

        pg.display.update()

    def awake(self):
        dt = time = 0
        mask = pg.Surface(SCR_SIZE)
        alpha = 255
        duration = 600
        self.game.clock.tick()

        while time <= duration:
            alpha = max(0, alpha - 255 * dt / duration)
            mask.set_alpha(alpha)

            self.game.screen.blit(self.bg, (0, 0))
            self.game.screen.blit(mask, (0, 0))
            pg.display.update()

            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
            time += dt

    def run_animation(self, animation_state, duration=400):
        self.game.clock.tick()
        dt = time = 0
        while time <= duration:
            self.handle_events(animation_state)
            self.update(dt, animation_state, time / duration)
            self.draw(self.game.screen)
            self.game.fps_manager.update(dt)
            dt = self.game.clock.tick()
            time += dt
        self.game.clock.tick()

    def run(self):
        self.game.sound_player.play_music(START_MUSIC)

        self.running = True
        self.bubbles = []
        self.bubbles_time = 0

        self.awake()
        self.run_animation(OPEN, 1000)

        self.game.clock.tick()
        dt = 0
        while self.running:
            self.handle_events()
            self.update(dt)
            self.draw(self.game.screen)
            self.game.fps_manager.update(dt)
            dt = self.game.clock.tick()


__all__ = ["MainMenu"]

import pygame as pg
import sys

from gui.text import Text
from gui.slider import Slider
from gui.text_button import *
from data.config import *
from data.paths import *
from data.resolution import *
from data.colors import *
from data.gui_texts import *
from utils import H


class SettingsWindow:
    def __init__(self, menu, game):
        self.menu = menu
        self.game = game

        self.bg_image = pg.image.load(START_MENU_CAPTION_BG).convert_alpha()
        self.caption_bg = None

        self.caption = Text(SCR_W2, H(100), FONT_1, H(80), WHITE, 1)

        self.resolution_warning = Text(SCR_W2, H(890), FONT_2, H(28), WHITE, 1, True)
        self.slider = Slider(SCR_W2, H(526), MASTER_VOLUME_TEXT, H(44), self.game.sound_player)

        resolutions = get_available_resolutions()
        self.res_buttons = [
            TextButton(SCR_W2, H(240 + 61*i), resolutions[i], FONT_1,
                       H(44), 200, self.game.sound_player, H(300), True)
            for i in range(len(resolutions))
        ]
        for button in self.res_buttons:
            button.set_text(button.texts)

        self.lang_buttons = [
            TextButton(SCR_W2, H(440 + 150*i), LANGUAGES[i], FONT_1,
                       H(50), 200, self.game.sound_player, H(300), True)
            for i in range(len(LANGUAGES))
        ]
        for button in self.lang_buttons:
            button.set_text(button.texts)

        self.lang_window_button = DoubleTextButton(SCR_W2, H(325), LANGUAGE_LABEL, LANGUAGES[0],
                                                   FONT_1, H(44), 200, self.game.sound_player)
        self.res_window_button = DoubleTextButton(SCR_W2, H(425), RESOLUTION_LABEL, resolutions[cur_res_index()],
                                                  FONT_1, H(44), 200, self.game.sound_player)

        self.exit_button = TextButton(SCR_W2, H(640), EXIT_TO_DESKTOP_TEXT, FONT_1, H(44), 200, self.game.sound_player, H(400))
        self.back_button = TextButton(SCR_W2, H(740), BACK_BUTTON_TEXT, FONT_1, H(44), 200, self.game.sound_player, H(200))
        self.yes_button = TextButton(SCR_W2 - H(160), SCR_H2, YES_BUTTON_TEXT, FONT_1, H(60), 200, self.game.sound_player, H(300), True)
        self.no_button = TextButton(SCR_W2 + H(160), SCR_H2, NO_BUTTON_TEXT, FONT_1, H(60), 200, self.game.sound_player, H(300), True)

        self.running = False

    def close_settings(self):
        self.run_animation(CLOSE)
        self.lang_window_button.hidden = True
        self.res_window_button.hidden = True
        self.slider.hidden = True
        self.exit_button.hidden = True
        self.back_button.hidden = True

    def go_to_settings(self):
        self.run_animation(CLOSE)
        self.lang_window_button.hidden = False
        self.res_window_button.hidden = False
        self.slider.hidden = False
        self.exit_button.hidden = False
        self.back_button.hidden = False
        self.set_caption(SETTINGS_WINDOW_CAPTIONS[self.menu.language][0])
        self.yes_button.hidden = True
        self.no_button.hidden = True
        for button in self.lang_buttons:
            button.hidden = True
        for button in self.res_buttons:
            button.hidden = True
        self.resolution_warning.hidden = True
        self.run_animation(OPEN)

    def go_to_exit(self):
        self.close_settings()
        self.set_caption(SETTINGS_WINDOW_CAPTIONS[self.menu.language][1])
        self.yes_button.hidden = False
        self.no_button.hidden = False
        self.run_animation(OPEN)

    def go_to_resolutions(self):
        self.close_settings()
        self.set_caption(SETTINGS_WINDOW_CAPTIONS[self.menu.language][2])
        for button in self.res_buttons:
            button.hidden = False
        self.resolution_warning.hidden = False
        self.run_animation(OPEN)

    def go_to_languages(self):
        self.close_settings()
        self.set_caption(SETTINGS_WINDOW_CAPTIONS[self.menu.language][3])
        for button in self.lang_buttons:
            button.hidden = False
        self.run_animation(OPEN)

    def set_caption(self, text):
        self.caption.set_text(text)
        self.caption_bg = pg.transform.scale(self.bg_image, (self.caption.w + H(60), H(120)))

    def set_language(self, language):
        self.lang_window_button.set_language(language)
        self.res_window_button.set_language(language)
        self.slider.set_language(language)
        self.back_button.set_language(language)
        self.exit_button.set_language(language)
        self.yes_button.set_language(language)
        self.no_button.set_language(language)
        self.resolution_warning.set_text(RESOLUTION_WARNING[language])
        caption = 3 if self.lang_window_button.hidden else 0
        self.set_caption(SETTINGS_WINDOW_CAPTIONS[language][caption])

    def handle_mouse_click(self):
        if self.lang_window_button.clicked:
            self.go_to_languages()

        elif self.res_window_button.clicked:
            self.go_to_resolutions()

        elif self.back_button.clicked:
            self.running = False

        elif self.exit_button.clicked:
            self.go_to_exit()

        elif self.yes_button.clicked:
            self.run_animation(CLOSE)
            pg.quit()
            sys.exit()

        elif self.no_button.clicked:
            self.go_to_settings()

        else:
            for button in self.lang_buttons:
                if button.clicked:
                    new_language = button.texts[0]
                    self.menu.set_language(new_language)
                    self.lang_window_button.set_value([new_language])
                    self.go_to_settings()
                    break

            for button in self.res_buttons:
                if button.clicked:
                    self.res_window_button.set_value(button.texts)
                    new_resolution = raw_resolution(button.texts[0])
                    if list(SCR_SIZE) != new_resolution:
                        save_resolution(new_resolution)
                    self.go_to_settings()
                    break

    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                self.game.sound_player.reset()
                self.game.sound_player.play_sound(UI_CLICK)
                if not self.back_button.hidden:
                    self.running = False
                else:
                    self.go_to_settings()

            elif e.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP) and e.button == pg.BUTTON_LEFT:
                self.slider.handle(e.type)
                if e.type == pg.MOUSEBUTTONDOWN:
                    self.handle_mouse_click()


    def update_alpha(self, state, time_elapsed):
        if state == OPEN:
            alpha = round(255 * time_elapsed)
        else:
            alpha = round(255 - 255 * time_elapsed)
        self.caption.set_alpha(alpha)
        self.caption_bg.set_alpha(alpha)
        self.resolution_warning.set_alpha(alpha)

    def update(self, dt, time_elapsed=0, state=WAIT):
        self.menu.update_bubbles(dt)

        self.lang_window_button.update(dt, state, time_elapsed)
        self.res_window_button.update(dt, state, time_elapsed)
        self.back_button.update(dt, state, time_elapsed)
        self.exit_button.update(dt, state, time_elapsed)
        self.slider.update(dt, state, time_elapsed)
        self.yes_button.update(dt, state, time_elapsed)
        self.no_button.update(dt, state, time_elapsed)
        for button in self.lang_buttons:
            button.update(dt, state, time_elapsed)
        for button in self.res_buttons:
            button.update(dt, state, time_elapsed)

        if state != WAIT:
            self.update_alpha(state, time_elapsed)

        if self.slider.pressed:
            self.game.sound_player.set_music_volume(self.slider.value)
            self.game.sound_player.set_sound_volume(self.slider.value)

    def draw(self, screen):
        screen.blit(self.menu.bg, (0, 0))

        for bubble in self.menu.bubbles:
            bubble.draw(screen, 0, 0)

        screen.blit(self.caption_bg, (SCR_W2 - self.caption_bg.get_width()//2, H(74)))
        self.caption.draw(screen)

        self.slider.draw(screen)
        self.lang_window_button.draw(screen)
        self.res_window_button.draw(screen)
        self.back_button.draw(screen)
        self.exit_button.draw(screen)
        self.yes_button.draw(screen)
        self.no_button.draw(screen)
        for button in self.lang_buttons:
            button.draw(screen)
        for button in self.res_buttons:
            button.draw(screen)

        self.resolution_warning.draw(screen)

        pg.display.update()

    def run_animation(self, state):
        self.game.clock.tick()
        dt = time = 0
        while time <= TEXTS_ANIMATION_TIME:
            self.update(dt, time/TEXTS_ANIMATION_TIME, state)
            self.draw(self.game.screen)
            self.game.fps_manager.update(dt)
            dt = self.game.clock.tick()
            time += dt
        self.game.clock.tick()

    def run(self):
        self.caption.set_alpha(0)
        self.slider.reset(self.game.sound_player.master_volume)
        self.lang_window_button.reset()
        self.res_window_button.reset()
        self.back_button.reset()
        self.exit_button.reset()

        self.run_animation(OPEN)

        dt = 0
        self.running = True
        while self.running:
            self.handle_events()
            self.update(dt)
            self.draw(self.game.screen)
            dt = self.game.clock.tick()

        self.run_animation(CLOSE)

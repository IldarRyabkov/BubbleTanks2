import pygame as pg
import sys
from random import uniform

from bubble import Bubble
from gui.text_widget import TextWidget
from gui.text_button import *
from gui.slider import Slider
from gui.main_menu_caption import *
from gui.main_menu_button import MainMenuButton
from constants import *
from data.scripts import *
from languages.texts import TEXTS
from data.paths import *
from utils import H, HF


class MainMenu:
    """Main menu of the game, where player can change
    game settings and start a new game.
    """
    def __init__(self, game):
        self.game = game
        self.running = True
        self.state = State.MAIN_PAGE

        sp = self.game.sound_player
        resolutions = list(map(self.pretty_res, SUPPORTED_RESOLUTIONS))

        self.res_buttons = []
        for i, res_text in enumerate(resolutions):
            button = TextButton(SCR_W2, H(240 + i * 671/len(resolutions)), res_text, CALIBRI_BOLD, H(56), 200, sp, H(300))
            button.set_text(button.texts)
            self.res_buttons.append(button)

        self.lang_buttons = []
        for i, lang_text in enumerate(TEXTS["language"]):
            button = TextButton(SCR_W2, H(440 + i * 120*i), lang_text, CALIBRI_BOLD, H(66), 200, sp, H(300))
            button.set_text(button.texts)
            self.lang_buttons.append(button)

        self.resolution_warning = TextWidget(SCR_W2, H(890), CALIBRI_BOLD, H(34), WHITE, 1)

        self.lang_window_button = DoubleTextButton(SCR_W2, H(325), TEXTS["language label"],
                                                   TEXTS["language"][self.game.language], CALIBRI_BOLD, H(56), 200, sp)

        self.res_window_button = DoubleTextButton(SCR_W2, H(415), TEXTS["resolution label"],
                                                  self.pretty_res([SCR_W, SCR_H]), CALIBRI_BOLD, H(56), 200, sp)

        self.slider = Slider(SCR_W2, H(516), TEXTS["master volume text"], CALIBRI_BOLD, H(56), sp)
        self.slider.set_value(sp.master_volume)

        self.exit_button = TextButton(SCR_W2, H(610), TEXTS["exit to desktop text"], CALIBRI_BOLD, H(56), 200, sp, H(400))
        self.back_button = TextButton(SCR_W2, H(700), TEXTS["back button text"], CALIBRI_BOLD, H(56), 200, sp, H(200))
        self.yes_button = TextButton(SCR_W2 - H(120), SCR_H2 + H(100), TEXTS["yes button text"], CALIBRI_BOLD, H(70), 200, sp, H(200))
        self.no_button = TextButton(SCR_W2 + H(120), SCR_H2 + H(100), TEXTS["no button text"], CALIBRI_BOLD, H(70), 200, sp, H(200))

        self.play_button = MainMenuButton(SCR_W2, TEXTS["play button label"], H(80), PLAY_BUTTON_BG, sp, 1.3, H(800))
        self.settings_button = MainMenuButton(SCR_W2 - H(180), TEXTS["settings button label"], H(80), SETTINGS_BUTTON_BG, sp, 1.3, H(840))
        self.credits_button = MainMenuButton(SCR_W2 + H(180), TEXTS["credits button label"], H(80), CREDITS_BUTTON_BG, sp, 1.3, H(840))

        self.credits_labels = (
            TextWidget(SCR_W2, H(200), FONT_1, H(42), WHITE, 1),
            TextWidget(SCR_W2, H(605), FONT_1, H(42), WHITE, 1),
            TextWidget(SCR_W2, H(810), FONT_1, H(42), WHITE, 1)
        )
        for i, label in enumerate(self.credits_labels):
            label.set_text(TEXTS["credits labels"][self.game.language][i])
        self.credits_bg_images = (
            pg.transform.smoothscale(pg.image.load(CREDITS_BG_1).convert_alpha(), (int(8/9*SCR_H), H(380))),
            pg.transform.smoothscale(pg.image.load(CREDITS_BG_2).convert_alpha(), (int(8/9*SCR_H), H(180))),
            pg.transform.smoothscale(pg.image.load(CREDITS_BG_3).convert_alpha(), (int(8/9*SCR_H), H(140)))
        )
        self.credits_widgets = (
            TextWidget(SCR_W2, H(250), CALIBRI_BOLD, H(61), WHITE, 1),
            TextWidget(SCR_W2, H(326), CALIBRI_BOLD, H(37), WHITE, 1),
            TextWidget(SCR_W2, H(360), CALIBRI_BOLD, H(56), WHITE, 1),
            TextWidget(SCR_W2, H(430), CALIBRI_BOLD, H(48), WHITE, 1),
            TextWidget(SCR_W2 - H(180), H(480), CALIBRI_BOLD, H(38), WHITE, 1, H(400)),
            TextWidget(SCR_W2 + H(180), H(480), CALIBRI_BOLD, H(38), WHITE, 1, H(400)),
            TextWidget(SCR_W2, H(650), CALIBRI_BOLD, H(46), WHITE, 1),
            TextWidget(SCR_W2, H(695), CALIBRI_BOLD, H(42), WHITE, 1),
            TextWidget(SCR_W2, H(730), CALIBRI_BOLD, H(34), WHITE, 1),
            TextWidget(SCR_W2, H(850), CALIBRI_BOLD, H(46), WHITE, 1),
            TextWidget(SCR_W2, H(894), CALIBRI_BOLD, H(34), WHITE, 1),
        )
        for i, widget in enumerate(self.credits_widgets):
            widget.set_text(TEXTS["credits widgets"][self.game.language][i])

        self.caption = MainMenuCaption(self, game)

        self.bg = pg.image.load(BG).convert()
        self.bg = pg.transform.scale(self.bg, SCR_SIZE)

        self.bubbles = []
        self.bubbles_time = 0
        self.set_language(self.game.language)

    @staticmethod
    def pretty_res(resolution) -> str:
        """Returns text representation of game resolution."""
        return '%d x %d' % tuple(resolution)

    def set_language(self, language):
        self.caption.set_format()
        self.resolution_warning.set_text(TEXTS["resolution warning"][language])
        self.lang_window_button.set_language(language)
        self.res_window_button.set_language(language)
        self.slider.set_language(language)
        self.back_button.set_language(language)
        self.exit_button.set_language(language)
        self.yes_button.set_language(language)
        self.no_button.set_language(language)
        self.play_button.set_language(language)
        self.settings_button.set_language(language)
        self.credits_button.set_language(language)

    def set_state(self, state, clicked_button=None):
        if clicked_button is not None:
            self.run_button_press_animation(clicked_button)

        duration = 1000 if self.state == State.MAIN_PAGE else 300
        self.run_animation(CLOSE, duration)

        self.state = state
        self.caption.set_format()

        if state == State.MAIN_PAGE:
            self.play_button.reset()
            self.settings_button.reset()
            self.credits_button.reset()
        elif state == State.CREDITS:
            pass
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

        duration = 1000 if self.state == State.MAIN_PAGE else 300
        self.run_animation(OPEN, duration)

    def handle_mouse_down(self, e_type):
        if self.state == State.MAIN_PAGE:
            if self.play_button.clicked:
                self.running = False
                self.game.sound_player.fade_out(1250)
                self.run_button_press_animation(self.play_button)
                self.run_animation(CLOSE, 1000)
                self.play_button.reset()
                self.settings_button.reset()
                self.credits_button.reset()
            elif self.settings_button.clicked:
                self.set_state(State.SETTINGS, self.settings_button)
            elif self.credits_button.clicked:
                self.set_state(State.CREDITS, self.credits_button)

        elif self.state == State.SETTINGS:
            self.slider.handle(e_type)
            if self.lang_window_button.clicked:
                self.set_state(State.LANGUAGES, self.lang_window_button)
            elif self.res_window_button.clicked:
                self.set_state(State.RESOLUTIONS, self.res_window_button)
            elif self.back_button.clicked:
                self.set_state(State.MAIN_PAGE, self.back_button)
            elif self.exit_button.clicked:
                self.set_state(State.EXIT_CONFIRMATION, self.exit_button)

        elif self.state == State.EXIT_CONFIRMATION:
            if self.yes_button.clicked:
                self.run_button_press_animation(self.yes_button)
                self.run_animation(CLOSE)
                self.run_awake_animation(CLOSE)
                sys.exit()
            elif self.no_button.clicked:
                self.set_state(State.MAIN_PAGE, self.no_button)

        elif self.state == State.LANGUAGES:
            for button in self.lang_buttons:
                if button.clicked:
                    save_language(button.texts)
                    new_language = TEXTS["language"].index(button.texts)
                    self.game.language = new_language
                    self.set_language(new_language)
                    self.lang_window_button.set_value(button.texts)
                    self.set_state(State.SETTINGS, button)
                    break

        elif self.state == State.RESOLUTIONS:
            for button in self.res_buttons:
                if button.clicked:
                    save_resolution(button.texts)
                    self.res_window_button.set_value(button.texts)
                    self.set_state(State.SETTINGS, button)
                    break

    def handle_mouse_up(self, e_type):
        if self.state == State.SETTINGS:
            self.slider.handle(e_type)

    def handle_events(self, animation_state=WAIT):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()

            if animation_state == WAIT:
                if self.state == State.CREDITS and e.type in (pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
                    self.set_state(State.MAIN_PAGE)

                elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    self.game.sound_player.play_sound(UI_CLICK)
                    if self.state in (State.SETTINGS, State.EXIT_CONFIRMATION, State.CREDITS):
                        self.set_state(State.MAIN_PAGE)
                    elif self.state == State.MAIN_PAGE:
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
            alpha = self.caption.alpha
            if self.state == State.RESOLUTIONS:
                self.resolution_warning.set_alpha(alpha)

            elif self.state == State.CREDITS:
                for label in self.credits_labels:
                    label.set_alpha(alpha)
                for bg_image in self.credits_bg_images:
                    bg_image.set_alpha(alpha)
                for widget in self.credits_widgets:
                    widget.set_alpha(alpha)

        if self.state == State.MAIN_PAGE:
            self.play_button.update(dt, animation_state, time_elapsed)
            self.settings_button.update(dt, animation_state, time_elapsed)
            self.credits_button.update(dt, animation_state, time_elapsed)

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

        if self.state == State.MAIN_PAGE:
            self.play_button.draw(screen)
            self.settings_button.draw(screen)
            self.credits_button.draw(screen)

        elif self.state == State.CREDITS:
            for i, label in enumerate(self.credits_labels):
                x = SCR_W2 - self.credits_bg_images[i].get_width() // 2
                y = label.y - H(15)
                screen.blit(self.credits_bg_images[i], (x, y))
                label.draw(screen)
            for widget in self.credits_widgets:
                widget.draw(screen)

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

    def run_awake_animation(self, state):
        time = 0
        duration = 600
        mask = pg.Surface(SCR_SIZE)
        self.game.clock.tick()

        while time <= duration:
            if state == OPEN:
                alpha = 255 - 255 * time/duration
            else:
                alpha = 255 * time/duration
            mask.set_alpha(alpha)

            self.game.screen.blit(self.bg, (0, 0))
            self.game.screen.blit(mask, (0, 0))
            pg.display.update()

            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
            time += dt

    def run_button_press_animation(self, button):
        dt = time = 0
        duration = 250
        self.game.clock.tick()
        while time <= duration:
            self.handle_events(CLOSE)
            self.update_bubbles(dt)
            increasing = time/duration >= 0.5
            button.update_size(dt, increasing, default_alpha=255)
            self.draw(self.game.screen)
            self.game.fps_manager.update(dt)
            dt = self.game.clock.tick()
            time += dt
        self.game.clock.tick()

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

        self.run_awake_animation(OPEN)
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

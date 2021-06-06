import pygame as pg
import sys

from menus.menu import Menu

from gui.widgets.text_widget import TextWidget
from gui.widgets.credits_label import CreditsLabel
from gui.widgets.main_menu_caption import *
from gui.widgets.background_bubbles import BackgroundBubbles

from gui.buttons.text_button import *
from gui.buttons.slider_button import SliderButton
from gui.buttons.main_menu_button import MainMenuButton
from gui.buttons.language_button import LanguageButton
from gui.buttons.resolution_button import ResolutionButton

from constants import *
from states import MainMenuStates as St
from languages.texts import TEXTS
from data.scripts import *
from data.paths import *
from utils import *


class MainMenu(Menu):
    """Main menu of the game, where player can change
    game settings and start a new game.
    """
    def __init__(self, game):
        super().__init__(game)
        sp = self.game.sound_player

        # background
        self.bg_surface = pg.image.load(BG).convert()
        self.bg_surface = pg.transform.scale(self.bg_surface, SCR_SIZE)

        # widgets
        self.resolution_warning = TextWidget(SCR_W2, H(890), CALIBRI_BOLD, H(34), WHITE, 1)
        self.credits_widgets = (
            CreditsLabel(H(200), CREDITS_BG_1, H(380)),
            CreditsLabel(H(605), CREDITS_BG_2, H(180)),
            CreditsLabel(H(810), CREDITS_BG_3, H(140)),
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
            TextWidget(SCR_W2, H(894), CALIBRI_BOLD, H(34), WHITE, 1)
        )
        self.bubbles = BackgroundBubbles()
        self.caption = MainMenuCaption(self)

        # widgets dictionary
        base_widgets = self.bubbles, self.caption
        self.widgets = {
            St.MAIN_PAGE: base_widgets,
            St.SETTINGS: base_widgets,
            St.CREDITS: (*base_widgets, *self.credits_widgets),
            St.LANGUAGES: base_widgets,
            St.RESOLUTIONS: (*base_widgets, self.resolution_warning),
            St.DIALOG_EXIT: base_widgets
        }

        # buttons
        self.resolution_buttons = self.create_resolution_buttons()
        self.language_buttons = self.create_language_buttons()

        self.to_languages_button = DoubleTextButton(SCR_W2, H(325),
                                                    TEXTS["language label"],
                                                    TEXTS["language"][self.game.language],
                                                    CALIBRI_BOLD, H(56), sp,
                                                    action=self.languages)

        self.to_resolutions_button = DoubleTextButton(SCR_W2, H(400),
                                                      TEXTS["resolution label"],
                                                      pretty_resolution([SCR_W, SCR_H]),
                                                      CALIBRI_BOLD, H(56), sp,
                                                      action=self.resolutions)

        self.music_slider = SliderButton(SCR_W2, H(475),
                                         TEXTS["music volume text"],
                                         CALIBRI_BOLD, H(52), sp, "music")

        self.sound_slider = SliderButton(SCR_W2, H(550),
                                         TEXTS["sound volume text"],
                                         CALIBRI_BOLD, H(52), sp, "sound")

        self.exit_button = TextButton(SCR_W2, H(625),
                                      TEXTS["exit to desktop text"],
                                      CALIBRI_BOLD, H(56), 200, sp,
                                      action=self.exit, w=H(400))

        self.back_button = TextButton(SCR_W2, H(700),
                                      TEXTS["back button text"],
                                      CALIBRI_BOLD, H(56), 200, sp,
                                      action=self.back, w=H(200))

        self.yes_button = TextButton(SCR_W2 - H(120), SCR_H2 + H(100),
                                     TEXTS["yes button text"],
                                     CALIBRI_BOLD, H(70), 200, sp,
                                     action=self.yes, w=H(200))

        self.no_button = TextButton(SCR_W2 + H(120), SCR_H2 + H(100),
                                    TEXTS["no button text"],
                                    CALIBRI_BOLD, H(70), 200, sp,
                                    action=self.no, w=H(200))

        self.play_button = MainMenuButton(SCR_W2, TEXTS["play button label"],
                                          H(80), PLAY_BUTTON_BG, sp, 1.3, H(800),
                                          action=self.start_game,
                                          click_sound=MOB_DEATH)

        self.settings_button = MainMenuButton(SCR_W2 - H(180), TEXTS["settings button label"],
                                              H(80), SETTINGS_BUTTON_BG, sp, 1.3, H(840),
                                              action=self.settings)

        self.credits_button = MainMenuButton(SCR_W2 + H(180), TEXTS["credits button label"],
                                             H(80), CREDITS_BUTTON_BG, sp, 1.3, H(840),
                                             action=self.credits)

        # buttons dictionary
        self.buttons = {
            St.MAIN_PAGE: (self.settings_button, self.play_button, self.credits_button),
            St.SETTINGS: (self.to_languages_button, self.to_resolutions_button,
                          self.music_slider, self.sound_slider,
                          self.back_button, self.exit_button),
            St.CREDITS: (),
            St.LANGUAGES: self.language_buttons,
            St.RESOLUTIONS: self.resolution_buttons,
            St.DIALOG_EXIT: (self.yes_button, self.no_button)
        }
        self.set_language(self.game.language)

    def create_resolution_buttons(self) -> list:
        resolutions = list(map(pretty_resolution, SUPPORTED_RESOLUTIONS))
        buttons = []
        for i, text in enumerate(resolutions):
            buttons.append(ResolutionButton(self, H(240 + i * 671/len(resolutions)), text))
        return buttons

    def create_language_buttons(self) -> list:
        languages = TEXTS["language"]
        buttons = []
        for i, text in enumerate(languages):
            buttons.append(LanguageButton(self, H(440 + i * 120*i), text))
        return buttons

    def start_game(self):
        """Action of the 'play' button. """
        self.game.sound_player.fade_out(1250)
        self.click_animation(self.play_button)
        self.close()

    def settings(self):
        """Action of the 'settings' button. """
        self.set_state(St.SETTINGS, self.settings_button)

    def credits(self):
        """Action of the 'credits' button. """
        self.set_state(St.CREDITS, self.credits_button)

    def languages(self):
        """Action of the 'to languages' button. """
        self.set_state(St.LANGUAGES, self.to_languages_button)

    def resolutions(self):
        """Action of the 'to resolutions' button. """
        self.set_state(St.RESOLUTIONS, self.to_resolutions_button)

    def back(self):
        """Action of the 'back' button. """
        self.set_state(St.MAIN_PAGE, self.back_button)

    def exit(self):
        """Action of the 'exit' button. """
        self.set_state(St.DIALOG_EXIT, self.exit_button)

    def yes(self):
        """Action of the 'yes' button. """
        self.click_animation(self.yes_button)
        self.animation(CLOSE)
        self.run_awake_animation(CLOSE)
        pg.quit()
        sys.exit()

    def no(self):
        """Action of the 'no' button. """
        self.set_state(St.MAIN_PAGE, self.no_button)

    def set_language(self, language):
        self.caption.set_state(self.state)
        self.resolution_warning.set_text(TEXTS["resolution warning"][language])
        self.to_languages_button.set_language(language)
        self.to_resolutions_button.set_language(language)
        self.music_slider.set_language(language)
        self.sound_slider.set_language(language)
        self.back_button.set_language(language)
        self.exit_button.set_language(language)
        self.yes_button.set_language(language)
        self.no_button.set_language(language)
        self.play_button.set_language(language)
        self.settings_button.set_language(language)
        self.credits_button.set_language(language)
        for i, widget in enumerate(self.credits_widgets):
            widget.set_text(TEXTS["credits widgets"][language][i])

    @property
    def animation_time(self):
        if self.state == St.MAIN_PAGE:
            return 1000
        return 300

    def set_widgets_state(self, state):
        self.caption.set_state(state)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type in (pg.KEYDOWN, pg.MOUSEBUTTONDOWN) and self.state == St.CREDITS:
            self.set_state(St.MAIN_PAGE)
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            if self.state in (St.SETTINGS, St.DIALOG_EXIT, St.CREDITS):
                self.set_state(St.MAIN_PAGE)
            elif self.state == St.MAIN_PAGE:
                self.set_state(St.DIALOG_EXIT)
            else:
                self.set_state(St.SETTINGS)

    def draw_background(self, screen):
        screen.blit(self.bg_surface, (0, 0))

    def run_awake_animation(self, state):
        time = 0
        duration = 600
        mask = pg.Surface(SCR_SIZE)
        self.game.clock.tick()
        while time <= duration:
            if state == OPEN:
                mask.set_alpha(int(255 - 255 * time/duration))
            else:
                mask.set_alpha(int(255 * time/duration))
            self.game.screen.blit(self.bg_surface, (0, 0))
            self.game.screen.blit(mask, (0, 0))
            pg.display.update()

            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
            time += dt

    def update_press_animation(self, button, dt):
        self.bubbles.update(dt)
        super().update_press_animation(button, dt)

    def open(self):
        self.bubbles.reset()
        self.game.sound_player.play_music(START_MUSIC)
        self.run_awake_animation(OPEN)
        super().open()

    @set_cursor_grab(False)
    def run(self):
        super().run()


__all__ = ["MainMenu"]

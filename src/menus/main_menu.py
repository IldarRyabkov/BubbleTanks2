import pygame as pg
import sys

from menus.menu import Menu

from gui.widgets.text_widget import TextWidget
from gui.widgets.credits_label import CreditsLabel
from gui.widgets.main_menu_caption import *
from gui.widgets.background_bubbles import BackgroundBubbles
from gui.widgets.key_hint import KeyHint

from gui.buttons.text_button import *
from gui.buttons.slider_button import SliderButton
from gui.buttons.language_button import LanguageButton
from gui.buttons.resolution_button import ResolutionButton
from gui.buttons.screen_mode_button import ScreenModeButton
from gui.buttons.save_button import SaveButton
from gui.buttons.back_button import BackButton
from gui.buttons.delete_button import DeleteButton
from gui.buttons.start_button import StartButton

from data.constants import *
from data.states import MainMenuStates as St
from data.languages import TEXTS
from data.scripts import *

from assets.paths import *
from components.utils import *


class MainMenu(Menu):
    """Main menu of the game, where player can change
    game settings and start a new game.
    """
    def __init__(self, game):
        super().__init__(game)
        sp = self.game.sound_player
        self.game_music_played = False
        self.splash_screen_shown = False
        self.clicked_save_button = None
        self.clicked_delete_button = None

        # background
        self.bg_surface = pg.image.load(BG).convert()
        self.bg_surface = pg.transform.scale(self.bg_surface, SCR_SIZE)

        # widgets
        self.resolution_warning = TextWidget(SCR_W2, H(860), CALIBRI, H(36), WHITE, 1, H(500))
        self.credits_widgets = (
            CreditsLabel(H(210), CREDITS_BG_1, H(240)),
            CreditsLabel(H(475), CREDITS_BG_2, H(180)),
            CreditsLabel(H(680), CREDITS_BG_3, H(150)),
            TextWidget(SCR_W2, H(260), CALIBRI_BOLD, H(61), WHITE, 1),
            TextWidget(SCR_W2, H(336), CALIBRI_BOLD, H(37), WHITE, 1),
            TextWidget(SCR_W2, H(370), CALIBRI_BOLD, H(56), WHITE, 1),
            TextWidget(SCR_W2, H(520), CALIBRI_BOLD, H(46), WHITE, 1),
            TextWidget(SCR_W2, H(565), CALIBRI_BOLD, H(42), WHITE, 1),
            TextWidget(SCR_W2, H(600), CALIBRI_BOLD, H(34), WHITE, 1),
            TextWidget(SCR_W2, H(720), CALIBRI_BOLD, H(46), WHITE, 1),
            TextWidget(SCR_W2, H(764), CALIBRI_BOLD, H(34), WHITE, 1)
        )
        self.bubbles = BackgroundBubbles(game.rect)
        self.caption = MainMenuCaption(self)
        self.esc_hint = KeyHint(SCR_W - H(190), H(890), CALIBRI, H(35), WHITE)

        # widgets dictionary
        base_widgets = self.bubbles, self.caption
        self.widgets = {
            St.SPLASH_SCREEN: (self.bubbles, self.caption),
            St.MAIN_PAGE: (self.bubbles, self.caption),
            St.SETTINGS: base_widgets,
            St.CREDITS: (*base_widgets, *self.credits_widgets, self.esc_hint),
            St.LANGUAGES: (*base_widgets, self.esc_hint),
            St.RESOLUTIONS: (*base_widgets, self.resolution_warning, self.esc_hint),
            St.SCREEN_MODES: (*base_widgets, self.esc_hint),
            St.EXIT: base_widgets,
            St.NEW_GAME: base_widgets,
            St.LOAD_GAME: base_widgets,
            St.OVERRIDE_SAVE: base_widgets,
            St.DELETE_SAVE: base_widgets
        }

        # buttons
        self.resolution_buttons = self.create_resolution_buttons()
        self.language_buttons = self.create_language_buttons()
        self.screen_mode_buttons = self.create_screen_mode_buttons()

        self.start_button = StartButton(SCR_W2, H(770), sp, action=self.start)

        self.to_languages_button = DoubleTextButton(self.game,
                                                    SCR_W2, H(325),
                                                    TEXTS["language label"],
                                                    TEXTS["language"][self.game.language],
                                                    CALIBRI_BOLD, H(56), sp,
                                                    action=self.languages,
                                                    min_alpha=200)

        self.to_resolutions_button = DoubleTextButton(self.game,
                                                      SCR_W2, H(405),
                                                      TEXTS["resolution label"],
                                                      pretty_resolution([SCR_W, SCR_H]),
                                                      CALIBRI_BOLD, H(56), sp,
                                                      action=self.resolutions,
                                                      min_alpha=200)

        self.music_slider = SliderButton(SCR_W2, H(485), H(996),
                                         TEXTS["music volume text"],
                                         CALIBRI_BOLD, H(56), sp, "music",
                                         min_alpha=200)

        self.sound_slider = SliderButton(SCR_W2, H(565), H(946),
                                         TEXTS["sound volume text"],
                                         CALIBRI_BOLD, H(56), sp, "sound",
                                         min_alpha=200)

        self.to_screen_modes_button = DoubleTextButton(self.game,
                                                       SCR_W2, H(645),
                                                       TEXTS["screen mode label"],
                                                       screen_mode_texts(game.screen_mode),
                                                       CALIBRI_BOLD, H(56), sp,
                                                       action=self.screen_modes,
                                                       min_alpha=200, w=H(780))

        self.back_button = BackButton(TEXTS["back button text"], sp, self.back)

        self.yes_button = TextButton(SCR_W2 - H(120), SCR_H2 + H(100),
                                     TEXTS["yes button text"],
                                     CALIBRI_BOLD, H(70), 220, sp,
                                     action=self.yes, w=H(200))

        self.no_button = TextButton(SCR_W2 + H(120), SCR_H2 + H(100),
                                    TEXTS["no button text"],
                                    CALIBRI_BOLD, H(70), 220, sp,
                                    action=self.no, w=H(200))

        self.resume_button = TextButton(SCR_W2, H(400),
                                        TEXTS["resume game button text"],
                                        CALIBRI_BOLD, H(56), 200, sp,
                                        action=self.resume_game, w=H(400),
                                        click_sound=ENEMY_DEATH)

        self.new_game_button = TextButton(SCR_W2, H(400),
                                          TEXTS["new game button text"],
                                          CALIBRI_BOLD, H(56), 200, sp,
                                          action=self.new_game,
                                          w=H(300))

        self.load_game_button = TextButton(SCR_W2, H(475),
                                           TEXTS["load game button text"],
                                           CALIBRI_BOLD, H(56), 200, sp,
                                           action=self.load_game,
                                           w=H(300))

        self.settings_button = TextButton(SCR_W2, H(550),
                                          TEXTS["settings button text"],
                                          CALIBRI_BOLD, H(56), 200, sp,
                                          action=self.settings, w=H(300))

        self.credits_button = TextButton(SCR_W2, H(625),
                                         TEXTS["credits button text"],
                                         CALIBRI_BOLD, H(56), 200, sp,
                                         action=self.credits, w=H(300))

        self.exit_button = TextButton(SCR_W2, H(700),
                                      TEXTS["exit to desktop button text"],
                                      CALIBRI_BOLD, H(56), 200, sp,
                                      action=self.exit, w=H(400))

        self.save_buttons = (
            SaveButton(game.rect, SCR_W2 - H(340), "save_1", sp, self.save_button_action),
            SaveButton(game.rect, SCR_W2, "save_2", sp, self.save_button_action),
            SaveButton(game.rect, SCR_W2 + H(340), "save_3", sp, self.save_button_action)
        )

        self.delete_buttons = (
            DeleteButton(SCR_W2 - H(340), sp, self.save_buttons[0], self.delete_button_action),
            DeleteButton(SCR_W2, sp, self.save_buttons[1], self.delete_button_action),
            DeleteButton(SCR_W2 + H(340), sp, self.save_buttons[2], self.delete_button_action)
        )

        # buttons dictionary
        self.buttons = {
            St.SPLASH_SCREEN: [self.start_button],
            St.MAIN_PAGE: [self.new_game_button, self.load_game_button,
                           self.settings_button, self.credits_button, self.exit_button],
            St.SETTINGS: [self.to_languages_button, self.to_resolutions_button,
                          self.to_screen_modes_button, self.music_slider,
                          self.sound_slider, self.back_button],
            St.CREDITS: [],
            St.NEW_GAME: [*self.save_buttons, self.back_button],
            St.LOAD_GAME: [*self.save_buttons, self.back_button],
            St.LANGUAGES: self.language_buttons,
            St.RESOLUTIONS: self.resolution_buttons,
            St.SCREEN_MODES: self.screen_mode_buttons,
            St.EXIT: [self.yes_button, self.no_button],
            St.OVERRIDE_SAVE: [self.yes_button, self.no_button],
            St.DELETE_SAVE: [self.yes_button, self.no_button],
        }
        self.set_language(self.game.language)

        self.current_save = None

    def add_resume_button(self):
        for button in self.buttons[St.MAIN_PAGE]:
            button.move(dy=HF(75))
        self.buttons[St.MAIN_PAGE].append(self.resume_button)

    def remove_resume_button(self):
        self.buttons[St.MAIN_PAGE].remove(self.resume_button)
        for button in self.buttons[St.MAIN_PAGE]:
            button.move(dy=-HF(75))

    def create_resolution_buttons(self) -> list:
        resolutions = list(map(pretty_resolution, SUPPORTED_RESOLUTIONS))
        buttons = []
        for i, text in enumerate(resolutions):
            buttons.append(ResolutionButton(self, H(200 + i * 671/len(resolutions)), text))
        return buttons

    def create_language_buttons(self) -> list:
        languages = TEXTS["language"]
        buttons = []
        for i, text in enumerate(languages):
            buttons.append(LanguageButton(self, H(440 + i * 120*i), text))
        return buttons

    def create_screen_mode_buttons(self) -> list:
        buttons = [
            ScreenModeButton(self, H(400), TEXTS["windowed mode"], H(56), WINDOWED_MODE, St.SETTINGS),
            ScreenModeButton(self, H(500), TEXTS["borderless mode"], H(56), BORDERLESS_MODE, St.SETTINGS),
            ScreenModeButton(self, H(600), TEXTS["fullscreen mode"], H(56), FULLSCREEN_MODE, St.SETTINGS)
        ]
        return buttons

    def set_delete_buttons(self):
        for db, sb in zip(self.delete_buttons, self.save_buttons):
            if sb.save_data is not None and db not in self.buttons[St.NEW_GAME]:
                self.buttons[St.NEW_GAME].append(db)
                self.buttons[St.LOAD_GAME].append(db)
            elif sb.save_data is None and db in self.buttons[St.NEW_GAME]:
                self.buttons[St.NEW_GAME].remove(db)
                self.buttons[St.LOAD_GAME].remove(db)

    def resume_game(self):
        """Action of the 'play' button. """
        save_data = load_save_file(self.current_save)
        self.init_save(self.resume_button, save_data)

    def init_save(self, button, save_data):
        if isinstance(button, SaveButton):
            update_config_file(save=button.save_name)
            self.current_save = button.save_name
        self.game.set_save_data(save_data)
        self.game.sound_player.fade_out(500)
        self.click_animation(button)
        self.close()

    def delete_button_action(self, button):
        self.clicked_delete_button = button
        self.set_state(St.DELETE_SAVE, button)

    def save_button_action(self, button):
        self.clicked_save_button = button

        if self.state == St.LOAD_GAME and button.save_data is not None:
            self.game.sound_player.play_sound(ENEMY_DEATH)
            self.click_animation(button)
            self.init_save(button, button.save_data)

        elif self.state == St.NEW_GAME:
            self.game.sound_player.play_sound(ENEMY_DEATH)
            if button.save_data is None:
                create_save_file(button.save_name)
                save_data = load_save_file(button.save_name)
                self.click_animation(button)
                self.init_save(button, save_data)
            else:
                self.set_state(St.OVERRIDE_SAVE, button)

    def start(self):
        self.set_state(St.MAIN_PAGE, self.start_button)

    def load_game(self):
        """Action of the 'load game' button. """
        self.set_state(St.LOAD_GAME, self.load_game_button)

    def new_game(self):
        """Action of the 'new game' button. """
        self.set_state(St.NEW_GAME, self.new_game_button)

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

    def screen_modes(self):
        """Action of the 'to screen modes' button. """
        self.set_state(St.SCREEN_MODES, self.to_screen_modes_button)

    def back(self):
        """Action of the 'back' button. """
        self.set_state(St.MAIN_PAGE, self.back_button)

    def exit(self):
        """Action of the 'exit' button. """
        self.set_state(St.EXIT, self.exit_button)

    def yes(self):
        """Action of the 'yes' button. """
        if self.state == St.EXIT:
            self.click_animation(self.yes_button)
            self.animation(CLOSE)
            self.run_awake_animation(CLOSE)
            pg.quit()
            sys.exit()

        elif self.state == St.OVERRIDE_SAVE:
            create_save_file(self.clicked_save_button.save_name)
            save_data = load_save_file(self.clicked_save_button.save_name)
            self.init_save(self.yes_button, save_data)

        elif self.state == St.DELETE_SAVE:
            self.delete_save_slot()
            self.set_state(self.previous_state, self.yes_button)

    def no(self):
        """Action of the 'no' button. """
        if self.state == St.EXIT:
            self.set_state(St.MAIN_PAGE, self.no_button)
        elif self.state == St.OVERRIDE_SAVE:
            self.set_state(St.NEW_GAME, self.no_button)
        elif self.state == St.DELETE_SAVE:
            self.set_state(self.previous_state, self.no_button)

    def delete_save_slot(self):
        save_button = self.clicked_delete_button.save_button
        file_name = save_button.save_name
        delete_save_file(file_name)
        if self.current_save == file_name:
            update_config_file(save="empty")
            self.set_current_save()
        save_button.load_save_data()
        self.set_delete_buttons()

    def set_language(self, language):
        self.game.language = language
        for button in (self.to_languages_button, self.to_resolutions_button,
                       self.to_screen_modes_button, self.start_button, self.music_slider,
                       self.sound_slider, self.back_button, self.yes_button,
                       self.no_button, self.resume_button, *self.screen_mode_buttons,
                       self.new_game_button, self.load_game_button, self.exit_button,
                       self.settings_button, self.credits_button, *self.save_buttons):
            button.set_language(language)

        self.caption.set_state(self.state)
        self.resolution_warning.set_text(TEXTS["resolution warning"][language])
        self.esc_hint.set_text(TEXTS["escape hint"][language])
        for i, widget in enumerate(self.credits_widgets):
            widget.set_text(TEXTS["credits widgets"][language][i])

    @property
    def animation_time(self):
        if self.is_closing:
            return 1000
        if self.is_opening:
            if self.state == St.SPLASH_SCREEN:
                return 1300
            return 800
        if self.state == St.SPLASH_SCREEN:
            return 500
        return 260

    def set_widgets_state(self, state):
        self.caption.set_state(state)

    def handle_escape_button_press(self):
        self.pressed_button = None
        if self.state in (St.SETTINGS, St.EXIT, St.CREDITS, St.NEW_GAME, St.LOAD_GAME):
            self.set_state(St.MAIN_PAGE)
        elif self.state == St.MAIN_PAGE:
            self.set_state(St.EXIT)
        elif self.state == St.OVERRIDE_SAVE:
            self.set_state(St.NEW_GAME)
        else:
            self.set_state(St.SETTINGS)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type in (pg.KEYDOWN, pg.MOUSEBUTTONDOWN) and self.state == St.CREDITS:
            self.set_state(St.MAIN_PAGE)
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.handle_escape_button_press()

    def draw_background(self, screen):
        screen.blit(self.bg_surface, (0, 0))

    def run_awake_animation(self, animation_state):
        if animation_state == OPEN:
            self.game.sound_player.play_music(TITLE_MUSIC)
        time = 0
        duration = 600
        mask = pg.Surface(SCR_SIZE)
        self.game.clock.tick()
        while time <= duration:
            if animation_state == OPEN:
                mask.set_alpha(int(255 - 255 * time/duration))
            else:
                mask.set_alpha(int(255 * time/duration))
            self.game.screen.blit(self.bg_surface, (0, 0))
            self.game.screen.blit(mask, (0, 0))
            pg.display.update()

            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
            time += dt

    def update_click_animation(self, button, dt):
        self.bubbles.update(dt)
        super().update_click_animation(button, dt)

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if self.is_closing and time_elapsed >= 0.5 and not self.game_music_played:
            self.game.sound_player.play_music(GAME_MUSIC)
            self.game_music_played = True
        super().update(dt, animation_state, time_elapsed)

    def set_current_save(self):
        self.current_save = load_current_save()
        if self.current_save != "empty" and load_save_file(self.current_save) is not None:
            if self.resume_button not in self.buttons[St.MAIN_PAGE]:
                self.add_resume_button()
        elif self.resume_button in self.buttons[St.MAIN_PAGE]:
            self.remove_resume_button()

    def open(self):
        if self.splash_screen_shown:
            self.state = St.MAIN_PAGE
        else:
            self.state = St.SPLASH_SCREEN
            self.splash_screen_shown = True
        self.caption.set_state(self.state)
        self.bubbles.reset()
        for button in self.save_buttons:
            button.load_save_data()
        self.set_current_save()
        self.set_delete_buttons()
        self.game_music_played = False
        self.run_awake_animation(OPEN)
        super().open()

    @set_cursor_grab(False)
    def run(self):
        super().run()


__all__ = ["MainMenu"]

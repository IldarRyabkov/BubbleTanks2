import sys
import pygame as pg

from gui.map import Map
from menus.menu import Menu
from gui.side_button import SideButton
from gui.slider_button import SliderButton
from gui.text_button import TextButton
from gui.text_widget import TextWidget
from gui.exit_button import ExitButton
from gui.tank_body import TankBody
from data.paths import *
from constants import *
from states import PauseMenuStates as St
from languages.texts import TEXTS
from utils import *


class PauseMenu(Menu):
    """ Pause menu, which the player can go to during the game.
    It has statistics window, map window and options window.

        -In stats window player can see all information about his tank.
        -In map window player can see his current position on map.
        -In options window player can change game options, exit so main menu or to desktop.
    """
    def __init__(self, game):
        super().__init__(game)

        # background
        self.screen_mask = pg.Surface(SCR_SIZE)
        self.screen_mask.set_alpha(175)
        self.menu_mask = pg.Surface((H(1072), H(760)))
        self.menu_mask.set_alpha(125)
        self.bg_surface = pg.Surface(SCR_SIZE)

        xo = SCR_W2 - H(584)  # x-coord of left side of pause menu
        sp = game.sound_player

        # widgets
        self.tank_body = TankBody(xo, self.game.player)

        self.stats_widgets = (
            TextWidget(xo + H(150), H(268), CALIBRI_BOLD, H(48), WHITE, 0, H(600)),
            TextWidget(xo + H(150), H(565), CALIBRI, H(42), WHITE, 0, H(480)),
            TextWidget(xo + H(656), H(565), CALIBRI, H(42), WHITE, 0, H(480)),
            TextWidget(xo + H(150), H(334), CALIBRI, H(32), WHITE, 0, H(630)),
            TextWidget(xo + H(150), H(628), CALIBRI, H(32), WHITE, 0, H(470)),
            TextWidget(xo + H(656), H(628), CALIBRI, H(32), WHITE, 0, H(470)),
        )
        self.stats_labels = (
            TextWidget(xo + H(150), H(508), CALIBRI_BOLD, H(48), WHITE),
            TextWidget(xo + H(656), H(508), CALIBRI_BOLD, H(48), WHITE),
            TextWidget(xo + H(150), H(812), CALIBRI, H(42), WHITE),
            TextWidget(xo + H(150), H(856), CALIBRI, H(42), WHITE),
        )
        self.stats_counters = (
            TextWidget(xo + H(530), H(812), CALIBRI, H(42), WHITE),
            TextWidget(xo + H(530), H(856), CALIBRI, H(42), WHITE)
        )
        self.caption = TextWidget(SCR_W2, H(50), FONT_1, H(56), WHITE, 1)

        self.window_caption = TextWidget(SCR_W2, H(176), CALIBRI_BOLD, H(58), WHITE, 1)

        # widgets dictionary
        base_widgets = self.window_caption,
        self.widgets = {
            St.STATS: (*base_widgets, *self.stats_labels,
                       *self.stats_widgets, *self.stats_counters,
                       self.tank_body),
            St.MAP: base_widgets,
            St.OPTIONS: base_widgets,
            St.DIALOG_MENU: base_widgets,
            St.DIALOG_DESKTOP: base_widgets
        }

        # buttons
        self.map_button = Map(xo)

        self.music_slider = SliderButton(SCR_W2, H(400),
                                         TEXTS["music volume text"],
                                         CALIBRI_BOLD, H(48), sp, "music")

        self.sound_slider = SliderButton(SCR_W2, H(470),
                                         TEXTS["sound volume text"],
                                         CALIBRI_BOLD, H(48), sp, "sound")

        self.to_menu_button = TextButton(SCR_W2, H(540),
                                         TEXTS["exit to menu text"],
                                         CALIBRI_BOLD, H(48), 210, sp,
                                         self.dialog_menu, H(500))

        self.to_desktop_button = TextButton(SCR_W2, H(610),
                                            TEXTS["exit to desktop text"],
                                            CALIBRI_BOLD, H(48), 210, sp,
                                            self.dialog_desktop, H(500))

        self.yes_button = TextButton(SCR_W2 - H(140), H(600),
                                     TEXTS["yes button text"],
                                     CALIBRI_BOLD, H(54), 210, sp,
                                     self.yes, H(200))

        self.no_button = TextButton(SCR_W2 + H(140), H(600),
                                    TEXTS["no button text"],
                                    CALIBRI_BOLD, H(54), 210, sp,
                                    self.no, H(200))

        self.exit_button = ExitButton(xo, sp, self.close)

        self.side_buttons = (
            SideButton(self, xo, H(160), TEXTS["stats side button caption"], sp, self.stats, True),
            SideButton(self, xo, H(352), TEXTS["map side button caption"], sp, self.map),
            SideButton(self, xo, H(544), TEXTS["options side button caption"], sp, self.options)
        )

        # buttons dictionary
        base_buttons = *self.side_buttons, self.exit_button
        self.buttons = {
            St.STATS: base_buttons,
            St.MAP: (*base_buttons, self.map_button),
            St.OPTIONS: (*base_buttons, self.music_slider,
                         self.sound_slider,  self.to_menu_button,
                         self.to_desktop_button),
            St.DIALOG_DESKTOP: (*base_buttons, self.yes_button, self.no_button),
            St.DIALOG_MENU: (*base_buttons, self.yes_button, self.no_button)
        }

    def set_widgets_state(self, state):
        text = TEXTS["pause menu window captions"][self.game.language][state]
        self.window_caption.set_text(text)
        if self.state in (St.DIALOG_MENU, St.DIALOG_DESKTOP):
            self.window_caption.y = H(400)
        else:
            self.window_caption.y = H(176)

    def select_side_button(self, state):
        """Sets which side button is selected, to draw it properly. """
        for i, button in enumerate(self.side_buttons):
            button.selected = (i == state)

    def options(self):
        """Action of 'options' side button. """
        self.set_state(St.OPTIONS, animation=False)
        self.select_side_button(St.OPTIONS)

    def map(self):
        """Action of 'map' side button. """
        self.set_state(St.MAP, animation=False)
        self.select_side_button(St.MAP)

    def stats(self):
        """Action of 'stats' side button. """
        self.set_state(St.STATS, animation=False)
        self.select_side_button(St.STATS)

    def close(self):
        """Action of exit button. """
        self.running = False
        if self.state in (St.DIALOG_MENU, St.DIALOG_DESKTOP):
            self.set_state(St.OPTIONS, animation=False)

    def dialog_menu(self):
        """Action of 'to menu' button. """
        self.set_state(St.DIALOG_MENU, self.to_menu_button)

    def dialog_desktop(self):
        """Action of 'to desktop' button. """
        self.set_state(St.DIALOG_DESKTOP, self.to_desktop_button)

    def yes(self):
        """Action of 'yes' button. """
        self.game.sound_player.fade_out(400)
        self.click_animation(self.yes_button)
        self.animation(CLOSE)
        if self.state == St.DIALOG_MENU:
            self.running = self.game.running = False
        elif self.state == St.DIALOG_DESKTOP:
            pg.quit()
            sys.exit()

    def no(self):
        """Action of 'no' button. """
        self.set_state(St.OPTIONS, self.no_button)

    @property
    def button_is_pressed(self):
        return self.pressed_button is not None and self.state != St.MAP

    def set_stats_texts(self):
        tank = self.game.player.tank
        """Sets texts of stats widgets and labels according to the given tank. """
        for i, widget in enumerate(self.stats_widgets):
            widget.set_text(TEXTS["tank descriptions"][self.game.language][tank][i])
        for i, label in enumerate(self.stats_labels):
            label.set_text(TEXTS["stats window labels"][self.game.language][i])

    def update_tank_description(self):
        self.set_stats_texts()
        self.tank_body.set_body()

    def update_counter(self, index, delta_value):
        new_value = int(self.stats_counters[index].text) + delta_value
        self.stats_counters[index].set_text(str(new_value))

    def set_language(self, language):
        self.caption.set_text(TEXTS["pause menu caption"][language])
        self.window_caption.set_text(TEXTS["pause menu window captions"][language][St.STATS])
        self.set_stats_texts()
        self.to_menu_button.set_language(language)
        self.to_desktop_button.set_language(language)
        self.sound_slider.set_language(language)
        self.music_slider.set_language(language)
        self.yes_button.set_language(language)
        self.no_button.set_language(language)
        for button in self.side_buttons:
            button.set_language(language)

    def reset_data(self):
        """Method is called when a new game is started. Resets all pause menu data. """
        self.state = St.STATS
        self.update_tank_description()
        self.map_button.reset_all_data()
        self.select_side_button(St.STATS)
        self.set_widgets_state(St.STATS)
        self.music_slider.reset()
        self.sound_slider.reset()
        for counter in self.stats_counters:
            counter.set_text("0")

    @property
    def animation_time(self):
        return 200

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pg.KEYDOWN and event.key in [pg.K_ESCAPE, pg.K_p]:
            if self.state in (St.DIALOG_DESKTOP, St.DIALOG_MENU):
                self.set_state(St.OPTIONS, animation=False)
            self.running = False
            self.pressed_button = None
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        self.game.update_scaling_objects(dt)
        super().update(dt, animation_state, time_elapsed)

    def draw_background(self, screen):
        screen.blit(self.bg_surface, (0, 0))
        self.game.draw_foreground()
        screen.blit(self.screen_mask, (0, 0))
        screen.blit(self.menu_mask, (SCR_W2 - H(488), H(160)))
        self.caption.draw(screen)

    @set_cursor_grab(False)
    def run(self):
        super().run()


__all__ = ["PauseMenu"]

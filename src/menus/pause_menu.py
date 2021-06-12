import pygame as pg

from menus.menu import Menu

from gui.buttons.map import Map
from gui.buttons.side_button import SideButton
from gui.buttons.slider_button import SliderButton
from gui.buttons.text_button import TextButton
from gui.buttons.exit_button import ExitButton

from gui.widgets.text_widget import TextWidget
from gui.widgets.tank_body_smooth import TankBodySmooth
from gui.widgets.mask import Mask
from gui.widgets.menu_caption import MenuCaption

from assets.paths import *
from data.constants import *
from data.states import PauseMenuStates as St
from data.languages.texts import TEXTS
from components.utils import *


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
        self.bg_surface = pg.Surface(SCR_SIZE)

        xo = SCR_W2 - H(584)  # x-coord of left side of pause menu
        sp = game.sound_player

        # buttons
        self.map_button = Map(self, xo, self.game.mob_generator.mobs_dict)

        self.music_slider = SliderButton(SCR_W2, H(400),
                                         TEXTS["music volume text"],
                                         CALIBRI_BOLD, H(48), sp, "music",
                                         alpha=210)

        self.sound_slider = SliderButton(SCR_W2, H(470),
                                         TEXTS["sound volume text"],
                                         CALIBRI_BOLD, H(48), sp, "sound",
                                         alpha=210)

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
                                     CALIBRI_BOLD, H(57), 220, sp,
                                     self.yes, H(200))

        self.no_button = TextButton(SCR_W2 + H(140), H(600),
                                    TEXTS["no button text"],
                                    CALIBRI_BOLD, H(57), 220, sp,
                                    self.no, H(200))

        self.exit_button = ExitButton(self, xo, sp, self.close)

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

        # widgets
        self.tank_body = TankBodySmooth(xo + H(940), H(370))
        self.mask = Mask(self, self.create_mask_surface())

        self.stats_widgets = (
            TextWidget(xo + H(150), H(268), CALIBRI_BOLD, H(47), WHITE, 0),
            TextWidget(xo + H(150), H(565), CALIBRI, H(40), WHITE, 0),
            TextWidget(xo + H(656), H(565), CALIBRI, H(40), WHITE, 0),
            TextWidget(xo + H(150), H(334), CALIBRI, H(35), WHITE, 0, H(630)),
            TextWidget(xo + H(150), H(628), CALIBRI, H(32), WHITE, 0, H(470)),
            TextWidget(xo + H(656), H(628), CALIBRI, H(32), WHITE, 0, H(470)),
        )
        self.stats_labels = (
            TextWidget(xo + H(150), H(508), CALIBRI_BOLD, H(47), WHITE),
            TextWidget(xo + H(656), H(508), CALIBRI_BOLD, H(47), WHITE),
            TextWidget(xo + H(150), H(812), CALIBRI, H(42), WHITE),
            TextWidget(xo + H(150), H(856), CALIBRI, H(42), WHITE),
        )
        self.stats_counters = (
            TextWidget(xo + H(530), H(812), CALIBRI, H(42), WHITE),
            TextWidget(xo + H(530), H(856), CALIBRI, H(42), WHITE)
        )
        self.caption = MenuCaption(self, SCR_W2, H(50), FONT_1, H(56), WHITE, 1)
        self.window_caption = TextWidget(SCR_W2, H(176), CALIBRI_BOLD, H(58), WHITE, 1)

        # widgets dictionary
        base_widgets = self.mask, self.window_caption, self.caption
        self.widgets = {
            St.STATS: (*base_widgets, *self.stats_labels,
                       *self.stats_widgets, *self.stats_counters,
                       self.tank_body),
            St.MAP: base_widgets,
            St.OPTIONS: base_widgets,
            St.DIALOG_MENU: base_widgets,
            St.DIALOG_DESKTOP: base_widgets
        }

    def create_mask_surface(self):
        surface = pg.Surface(SCR_SIZE, pg.SRCALPHA)
        surface.fill((0, 0, 0, 175))
        small_mask = pg.Surface((H(1072), H(760)), pg.SRCALPHA)
        small_mask.fill((0, 0, 0, 125))
        surface.blit(small_mask, (SCR_W2 - H(488), H(160)))
        for button in self.side_buttons:
            surface.blit(button.bg_surface, (button.x, button.y))
        return surface

    def set_widgets_state(self, state):
        text = TEXTS["pause menu window captions"][self.game.language][state]
        self.window_caption.set_text(text)
        if self.state in (St.DIALOG_MENU, St.DIALOG_DESKTOP):
            self.window_caption.y = H(360)
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
        super().close()
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
            self.game.update_save_data()
            self.running = self.game.running = False
        elif self.state == St.DIALOG_DESKTOP:
            self.game.quit()

    def no(self):
        """Action of 'no' button. """
        self.set_state(St.OPTIONS, self.no_button)

    def set_stats_texts(self):
        tank = self.game.player.tank
        """Sets texts of stats widgets and labels according to the given tank. """
        for i, widget in enumerate(self.stats_widgets):
            widget.set_text(TEXTS["tank descriptions"][self.game.language][tank][i])
        for i, label in enumerate(self.stats_labels):
            label.set_text(TEXTS["stats window labels"][self.game.language][i])

    def update_tank_description(self):
        self.set_stats_texts()
        self.tank_body.set_body(self.game.player.tank)

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

    def set_data(self, data):
        self.state = St.STATS
        self.update_tank_description()
        self.map_button.set_data(data)
        self.select_side_button(St.STATS)
        self.set_widgets_state(St.STATS)
        self.stats_counters[0].set_text(data["enemies killed"])
        self.stats_counters[1].set_text(data["bubbles collected"])

    @property
    def animation_time(self):
        return 200

    def handle_events_animation(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            elif event.type in [pg.KEYDOWN, pg.KEYUP]:
                self.game.player.handle(event.type, event.key)
            elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
                self.game.player.handle(event.type, event.button)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pg.KEYDOWN and event.key in [pg.K_ESCAPE, pg.K_p]:
            self.close()
        elif event.type in [pg.KEYDOWN, pg.KEYUP]:
            self.game.player.handle(event.type, event.key)
        elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
            self.game.player.handle(event.type, event.button)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        self.game.update_scaling_objects(dt)
        super().update(dt, animation_state, time_elapsed)

    def draw_background(self, screen):
        screen.blit(self.bg_surface, (0, 0))
        self.game.draw_foreground()

    @set_cursor_grab(False)
    def run(self):
        super().run()


__all__ = ["PauseMenu"]

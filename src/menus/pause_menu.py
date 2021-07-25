import pygame as pg

from menus.menu import Menu

from gui.buttons.map import Map
from gui.buttons.side_button import SideButton
from gui.buttons.slider_button import SliderButton
from gui.buttons.text_button import *
from gui.buttons.exit_button import ExitButton
from gui.buttons.screen_mode_button import ScreenModeButton
from gui.buttons.control_button import ControlButton

from gui.widgets.text_widget import TextWidget
from gui.widgets.tank_preview_smooth import TankPreviewSmooth
from gui.widgets.mask import Mask
from gui.widgets.menu_caption import MenuCaption
from gui.widgets.key_hint import KeyHint

from assets.paths import *
from data.constants import *
from data.states import PauseMenuStates as St
from data.languages import TEXTS
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
        self.clicked_control_button = None

        # background
        self.bg_surface = pg.Surface(SCR_SIZE)

        xo = SCR_W2 - H(584)  # x-coord of left side of pause menu
        sp = game.sound_player

        # buttons
        self.screen_mode_buttons = self.create_screen_mode_buttons()

        self.map_button = Map(self, xo, self.game.world.visited_rooms)

        self.music_slider = SliderButton(SCR_W2, H(360),  H(856),
                                         TEXTS["music volume text"],
                                         CALIBRI_BOLD, H(48), sp, "music",
                                         min_alpha=210)

        self.sound_slider = SliderButton(SCR_W2, H(430), H(826),
                                         TEXTS["sound volume text"],
                                         CALIBRI_BOLD, H(48), sp, "sound",
                                         min_alpha=210)

        self.to_screen_modes_button = DoubleTextButton(self.game,
                                                       SCR_W2, H(500),
                                                       TEXTS["screen mode label"],
                                                       screen_mode_texts(game.screen_mode),
                                                       CALIBRI_BOLD, H(48), sp,
                                                       action=self.screen_modes,
                                                       min_alpha=210, w=H(760))

        self.to_controls_button = TextButton(SCR_W2, H(570),
                                             TEXTS["controls button text"],
                                             CALIBRI_BOLD, H(48), 210, sp,
                                             action=self.controls, w=H(400))

        self.to_menu_button = TextButton(SCR_W2, H(640),
                                         TEXTS["exit to menu text"],
                                         CALIBRI_BOLD, H(48), 210, sp,
                                         self.dialog_menu, H(500))

        self.to_desktop_button = TextButton(SCR_W2, H(710),
                                            TEXTS["exit to desktop text"],
                                            CALIBRI_BOLD, H(48), 210, sp,
                                            self.dialog_desktop, H(500))

        self.back_button = TextButton(SCR_W2, H(800), TEXTS["back button text"],
                                      CALIBRI_BOLD, H(52), 210, sp,
                                      action=self.back, w=H(300))

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
        self.control_buttons = (
            ControlButton(xo + H(184), H(295), TEXTS["moving up label"],
                          self.game.controls, "up", sp, self.control_button_action, k=0.8),

            ControlButton(xo + H(184), H(380), TEXTS["moving down label"],
                          self.game.controls, "down", sp, self.control_button_action, k=0.8),

            ControlButton(xo + H(184), H(465), TEXTS["moving left label"],
                          self.game.controls, "left", sp, self.control_button_action, k=0.8),

            ControlButton(xo + H(184), H(550), TEXTS["moving right label"],
                          self.game.controls, "right", sp, self.control_button_action, k=0.8),

            ControlButton(xo + H(594), H(380), TEXTS["superpower label"],
                          self.game.controls, "superpower", sp, self.control_button_action, k=0.8),

            ControlButton(xo + H(594), H(465), TEXTS["pause label"],
                          self.game.controls, "pause", sp, self.control_button_action, k=0.8),
        )
        self.reset_key_mapping_button = TextButton(SCR_W2, H(720),
                                                   TEXTS["reset key mapping text"],
                                                   CALIBRI_BOLD, H(52), 210, sp,
                                                   action=self.reset_key_mapping, w=H(580))

        # buttons dictionary
        base_buttons = *self.side_buttons, self.exit_button
        self.buttons = {
            St.STATS: base_buttons,
            St.MAP: (*base_buttons, self.map_button),
            St.OPTIONS: (*base_buttons, self.music_slider, self.sound_slider,
                         self.to_menu_button, self.to_desktop_button,
                         self.to_screen_modes_button, self.to_controls_button),
            St.DIALOG_DESKTOP: (*base_buttons, self.yes_button, self.no_button),
            St.DIALOG_MENU: (*base_buttons, self.yes_button, self.no_button),
            St.SCREEN_MODES: (*base_buttons, *self.screen_mode_buttons,
                              self.back_button),
            St.CONTROLS: (*base_buttons, *self.control_buttons,
                          self.reset_key_mapping_button, self.back_button)
        }

        # widgets
        self.tank_body = TankPreviewSmooth(game.rect, xo + H(940), H(370))
        self.mask = Mask(self, self.create_mask_surface())
        self.esc_hint = KeyHint(xo + H(982), H(856), CALIBRI, H(33), WHITE)

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
            St.DIALOG_MENU: (*base_widgets, self.esc_hint),
            St.DIALOG_DESKTOP: (*base_widgets, self.esc_hint),
            St.SCREEN_MODES: (*base_widgets, self.esc_hint),
            St.CONTROLS: (*base_widgets, self.esc_hint)
        }

    def create_screen_mode_buttons(self) -> list:
        buttons = [
            ScreenModeButton(self, H(440), TEXTS["windowed mode"], H(52), WINDOWED_MODE, St.OPTIONS),
            ScreenModeButton(self, H(520), TEXTS["borderless mode"], H(52), BORDERLESS_MODE, St.OPTIONS),
            ScreenModeButton(self, H(600), TEXTS["fullscreen mode"], H(52), FULLSCREEN_MODE, St.OPTIONS)
        ]
        return buttons

    def create_mask_surface(self):
        surface = pg.Surface(SCR_SIZE, pg.SRCALPHA)
        surface.fill((0, 0, 0, 150))
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
        elif self.state == St.SCREEN_MODES:
            self.window_caption.y = H(226)
        else:
            self.window_caption.y = H(176)

    def control_button_action(self, button):
        if self.clicked_control_button is not None:
            self.clicked_control_button.deactivate()
        button.activate()
        self.clicked_control_button = button

    def controls(self):
        """Action of the 'to controls' button. """
        if self.clicked_control_button is not None:
            self.clicked_control_button.deactivate()
            self.clicked_control_button = None
        self.set_state(St.CONTROLS, self.to_controls_button)

    def reset_key_mapping(self):
        self.control_buttons[0].set_control(pg.K_w)
        self.control_buttons[1].set_control(pg.K_s)
        self.control_buttons[2].set_control(pg.K_a)
        self.control_buttons[3].set_control(pg.K_d)
        self.control_buttons[4].set_control(pg.K_SPACE)
        self.control_buttons[5].set_control(pg.K_p)
        if self.clicked_control_button is not None:
            self.clicked_control_button.deactivate()
            self.clicked_control_button = None

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
        if self.state in (St.DIALOG_MENU, St.DIALOG_DESKTOP, St.SCREEN_MODES, St.CONTROLS):
            self.set_state(St.OPTIONS, animation=False)

    def dialog_menu(self):
        """Action of 'to menu' button. """
        self.set_state(St.DIALOG_MENU, self.to_menu_button)

    def dialog_desktop(self):
        """Action of 'to desktop' button. """
        self.set_state(St.DIALOG_DESKTOP, self.to_desktop_button)

    def screen_modes(self):
        """Action of 'to screen modes' button. """
        self.set_state(St.SCREEN_MODES, self.to_screen_modes_button)

    def back(self):
        """Action of 'back' button. """
        self.set_state(St.OPTIONS, self.back_button)

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
        self.tank_body.set(self.game.player.tank)

    def update_counter(self, index, delta_value):
        new_value = int(self.stats_counters[index].text) + delta_value
        self.stats_counters[index].set_text(str(new_value))

    def set_language(self, language):
        self.caption.set_text(TEXTS["pause menu caption"][language])
        self.window_caption.set_text(TEXTS["pause menu window captions"][language][St.STATS])
        self.esc_hint.set_text(TEXTS["escape hint"][language])
        self.set_stats_texts()
        for button in (self.to_menu_button, self.to_screen_modes_button, self.to_desktop_button,
                       self.sound_slider, self.music_slider, self.yes_button, self.no_button,
                       *self.side_buttons, *self.screen_mode_buttons, self.back_button,
                       self.to_controls_button, *self.control_buttons, self.reset_key_mapping_button):
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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if self.state in (St.DIALOG_MENU, St.DIALOG_DESKTOP, St.SCREEN_MODES, St.CONTROLS):
                    self.set_state(St.OPTIONS)
                else:
                    self.close()
            elif event.key == self.game.controls["pause"] and self.state != St.CONTROLS:
                self.close()
        if event.type in [pg.KEYDOWN, pg.KEYUP]:
            self.game.player.handle(event.type, event.key)
        elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
            self.game.player.handle(event.type, event.button)
        if event.type == pg.KEYDOWN and event.key != pg.K_ESCAPE and self.state == St.CONTROLS:
            if self.clicked_control_button is not None:
                self.clicked_control_button.change_control(event.key)

    def update_click_animation(self, pressed_button, dt):
        self.game.update_scaling_objects(dt)
        super().update_click_animation(pressed_button, dt)

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

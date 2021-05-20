import sys
import pygame as pg

from body import Body
from map import Map
from gui.side_button import SideButton
from gui.slider import Slider
from gui.text_button import TextButton
from gui.text import Text
from data.paths import *
from constants import *
from data.gui_texts import *
from data.tank_bodies import TANK_BODIES
from utils import H


class State:
    STATS_WINDOW = 0
    MAP_WINDOW = 1
    OPTIONS_WINDOW = 2
    EXIT_TO_MENU_CONFIRMATION = 3
    EXIT_TO_DESKTOP_CONFIRMATION = 4



class PauseMenu:
    """ Pause menu, which the player can go to during the game.
    It has statistics window, map window and options window.

        -In stats window player can see all information about his tank.
        -In map window player can see his current position on map.
        -In options window player can change game options.
    """
    def __init__(self, game):
        self.game = game
        self.running = True
        self.state = State.STATS_WINDOW

        xo = SCR_W2 - H(584)  # x-coord of  top-left corner of pause menu

        # gui elements of Stats window
        self.tank_body = None
        self.tank_body_pos = (xo + H(940), H(370))

        self.stats_widgets = (
            Text(xo + H(150), H(268), FONT_3, H(48), WHITE, 0, H(470)),
            Text(xo + H(150), H(575), CALIBRI_BOLD, H(42), WHITE, 0, H(480)),
            Text(xo + H(656), H(575), CALIBRI_BOLD, H(42), WHITE, 0, H(480)),
            Text(xo + H(150), H(344), CALIBRI, H(34), WHITE, 0, H(630)),
            Text(xo + H(150), H(668), CALIBRI, H(34), WHITE, 0, H(470)),
            Text(xo + H(656), H(668), CALIBRI, H(34), WHITE, 0, H(470)),
        )
        self.stats_labels = (
            Text(xo + H(150), H(508), FONT_3, H(48), WHITE),
            Text(xo + H(656), H(508), FONT_3, H(48), WHITE),
            Text(xo + H(150), H(842), FONT_3, H(39), WHITE),
            Text(xo + H(656), H(842), FONT_3, H(39), WHITE),
        )
        self.counters = (
            Text(xo + H(440), H(840), FONT_3, H(43), WHITE),
            Text(xo + H(990), H(840), FONT_3, H(43), WHITE)
        )

        # gui elements of Map window
        self.map = Map(xo)

        # gui elements of Options window
        sp = game.sound_player
        self.music_slider = Slider(SCR_W2, H(400), MUSIC_VOLUME_TEXT, FONT_3, H(48), sp)
        self.sound_slider = Slider(SCR_W2, H(485), SOUND_VOLUME_TEXT, FONT_3, H(48), sp)
        self.to_menu_button = TextButton(SCR_W2, H(580), EXIT_TO_MENU_TEXT, FONT_3, H(48), 210, sp)
        self.to_desktop_button = TextButton(SCR_W2, H(665), EXIT_TO_DESKTOP_TEXT, FONT_3, H(48), 210, sp)
        self.yes_button = TextButton(SCR_W2 - H(140), H(600), YES_BUTTON_TEXT, FONT_3, H(54), 210, sp, H(200))
        self.no_button = TextButton(SCR_W2 + H(140), H(600), NO_BUTTON_TEXT, FONT_3, H(54), 210, sp, H(200))

        # Base gui elements of Pause menu
        self.side_buttons = (
            SideButton(xo, H(160), STATS_SIDE_BUTTON_CAPTION, sp, True),
            SideButton(xo, H(352), MAP_SIDE_BUTTON_CAPTION, sp),
            SideButton(xo, H(544), OPTIONS_SIDE_BUTTON_CAPTION, sp)
        )
        self.screen_mask = pg.Surface(SCR_SIZE)
        self.screen_mask.set_alpha(175)
        self.menu_mask = pg.Surface((H(1072), H(760)))
        self.menu_mask.set_alpha(125)

        self.bg_surface = pg.Surface(SCR_SIZE)
        self.caption = Text(SCR_W2, H(50), FONT_1, H(56), WHITE, 1)
        self.window_caption = Text(SCR_W2, H(176), FONT_3, H(58), WHITE, 1)

    def set_stats_widgets(self, tank=(0, 0)):
        for i, widget in enumerate(self.stats_widgets):
            widget.set_text(TANK_DESCRIPTIONS[self.game.language][tank][i])
        for i, label in enumerate(self.stats_labels):
            label.set_text(STATS_WINDOW_LABELS[self.game.language][i])

    def set_tank_stats(self, tank=(0, 0)):
        self.set_stats_widgets(tank)
        self.tank_body = Body(TANK_BODIES[tank])

    def update_counter(self, counter_index, value):
        new_value = int(self.counters[counter_index].text) + value
        self.counters[counter_index].set_text(str(new_value))

    def set_language(self, language):
        self.caption.set_text(PAUSE_MENU_CAPTION[language])
        self.window_caption.set_text(PAUSE_MENU_WINDOW_CAPTIONS[language][State.STATS_WINDOW])
        self.set_stats_widgets()
        self.to_menu_button.set_language(language)
        self.to_desktop_button.set_language(language)
        self.sound_slider.set_language(language)
        self.music_slider.set_language(language)
        self.yes_button.set_language(language)
        self.no_button.set_language(language)
        for button in self.side_buttons:
            button.set_language(language)

    def reset(self):
        """Method is called when a new game is started. Resets map
        in the map window and player statistics in the stats window.
        Also sets stats window as a current window.
        """
        self.set_tank_stats()
        self.map.reset()
        self.sound_slider.reset(self.game.sound_player.master_volume)
        self.music_slider.reset(self.game.sound_player.master_volume)
        self.to_menu_button.reset()
        self.to_desktop_button.reset()
        self.set_state(State.STATS_WINDOW)
        self.set_side_button_pressed(State.STATS_WINDOW)
        for counter in self.counters:
            counter.set_text("0")

    def set_side_button_pressed(self, index):
        for button in self.side_buttons:
            button.pressed = False
        self.side_buttons[index].pressed = True

    def set_state(self, state, animation=False, clicked_button=None):
        if clicked_button is not None:
            self.run_button_press_animation(clicked_button)
        if animation:
            self.run_animation(CLOSE)

        self.state = state
        self.window_caption.set_text(PAUSE_MENU_WINDOW_CAPTIONS[self.game.language][self.state])
        if state in (State.EXIT_TO_MENU_CONFIRMATION, State.EXIT_TO_DESKTOP_CONFIRMATION):
            self.window_caption.y = H(400)
            self.yes_button.reset()
            self.no_button.reset()
        else:
            self.window_caption.y = H(176)
        if state == State.MAP_WINDOW:
            self.map.reset_offset()
        elif state == State.OPTIONS_WINDOW:
            self.sound_slider.reset()
            self.music_slider.reset()
            self.to_desktop_button.reset()
            self.to_menu_button.reset()

        if animation:
            self.run_animation(OPEN)

    def update_map_data(self, room_pos, boss_state):
        """Adds information about visited room and boss location to the map. """
        self.map.add_visited_room(room_pos)
        if boss_state == BOSS_IN_CURRENT_ROOM:
            self.map.boss_aim.pos = room_pos

    def handle_mouse_up(self, e_type):
        if self.state == State.OPTIONS_WINDOW:
            self.music_slider.handle(e_type)
            self.sound_slider.handle(e_type)
        elif self.state == State.MAP_WINDOW:
            self.map.handle_mouse_click(e_type)

    def handle_mouse_down(self, e_type):
        for state, button in enumerate(self.side_buttons):
            if button.clicked:
                self.set_side_button_pressed(state)
                self.set_state(state)
                return

        if self.state == State.OPTIONS_WINDOW:
            self.music_slider.handle(e_type)
            self.sound_slider.handle(e_type)
            if self.to_desktop_button.clicked:
                self.set_state(State.EXIT_TO_DESKTOP_CONFIRMATION, True, self.to_desktop_button)
            elif self.to_menu_button.clicked:
                self.set_state(State.EXIT_TO_MENU_CONFIRMATION, True, self.to_menu_button)

        elif self.state == State.MAP_WINDOW:
            self.map.handle_mouse_click(e_type)

        elif self.state == State.EXIT_TO_DESKTOP_CONFIRMATION:
            if self.yes_button.clicked:
                self.run_button_press_animation(self.yes_button)
                self.run_animation(CLOSE)
                sys.exit()
            elif self.no_button.clicked:
                self.set_state(State.OPTIONS_WINDOW, True, self.no_button)

        elif self.state == State.EXIT_TO_MENU_CONFIRMATION:
            if self.yes_button.clicked:
                self.run_button_press_animation(self.yes_button)
                self.running = self.game.running = False
            elif self.no_button.clicked:
                self.set_state(State.OPTIONS_WINDOW, True, self.no_button)

    def handle_events(self, animation_state=WAIT):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()

            if animation_state == WAIT:
                if e.type == pg.KEYDOWN and e.key in [pg.K_ESCAPE, pg.K_p]:
                    if self.state in (State.EXIT_TO_DESKTOP_CONFIRMATION,
                                      State.EXIT_TO_MENU_CONFIRMATION):
                        self.set_state(State.OPTIONS_WINDOW, True)
                    else:
                        self.running = False
                        if self.state == State.MAP_WINDOW:
                            self.map.reset_offset()

                elif e.type == pg.MOUSEBUTTONUP and e.button == pg.BUTTON_LEFT:
                    self.handle_mouse_up(e.type)

                elif e.type == pg.MOUSEBUTTONDOWN and e.button == pg.BUTTON_LEFT:
                    self.handle_mouse_down(e.type)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        self.game.update_scaling_objects(dt)
        if animation_state != WAIT:
            self.window_caption.update_alpha(animation_state, time_elapsed)

        if self.state == State.STATS_WINDOW:
            x, y = self.tank_body_pos
            self.tank_body.update(x, y, dt, (9000, y))

        elif self.state == State.MAP_WINDOW:
            self.map.update(dt)

        elif self.state == State.OPTIONS_WINDOW:
            self.sound_slider.update(dt, animation_state, time_elapsed)
            self.music_slider.update(dt, animation_state, time_elapsed)
            self.to_menu_button.update(dt, animation_state, time_elapsed)
            self.to_desktop_button.update(dt, animation_state, time_elapsed)
            if self.sound_slider.pressed:
                self.game.sound_player.set_sound_volume(self.sound_slider.value)
            elif self.music_slider.pressed:
                self.game.sound_player.set_music_volume(self.music_slider.value)

        else:
            self.yes_button.update(dt, animation_state, time_elapsed)
            self.no_button.update(dt, animation_state, time_elapsed)

    def draw(self, screen):
        """Draws all objects in the background and pause menu items. """
        screen.blit(self.bg_surface, (0, 0))
        self.game.draw_foreground()
        screen.blit(self.screen_mask, (0, 0))
        screen.blit(self.menu_mask, (SCR_W2 - H(488), H(160)))
        self.caption.draw(screen)
        self.window_caption.draw(screen)
        for button in self.side_buttons:
            button.draw(screen)

        if self.state == State.STATS_WINDOW:
            for widget in self.stats_widgets:
                widget.draw(screen)
            for label in self.stats_labels:
                label.draw(screen)
            for counter in self.counters:
                counter.draw(screen)
            pg.draw.circle(screen, WHITE, self.tank_body_pos, H(129))
            pg.draw.circle(screen, TANK_BG_COLOR, self.tank_body_pos, H(123))
            self.tank_body.draw(screen)

        elif self.state == State.MAP_WINDOW:
            self.map.draw(screen)

        elif self.state == State.OPTIONS_WINDOW:
            self.to_menu_button.draw(screen)
            self.to_desktop_button.draw(screen)
            self.sound_slider.draw(screen)
            self.music_slider.draw(screen)

        else:
            self.yes_button.draw(screen)
            self.no_button.draw(screen)

        pg.display.update()

    def run_button_press_animation(self, button):
        dt = time = 0
        duration = 250
        self.game.clock.tick()
        while time <= duration:
            self.handle_events(CLOSE)
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
        """Pause menu loop which starts when player pressed pause key. """
        self.game.draw_background(self.bg_surface)
        self.game.player.stop_moving()

        self.running = True
        dt = 0

        while self.running:
            self.update(dt)
            self.draw(self.game.screen)
            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
            self.handle_events()


__all__ = ["PauseMenu"]

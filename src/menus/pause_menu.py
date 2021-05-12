import sys
import pygame as pg

from gui.stats_window import StatsWindow
from gui.map_window import MapWindow
from gui.options_window import OptionsWindow
from gui.side_button import SideButton
from gui.text import Text
from data.paths import FONT_1
from data.colors import WHITE
from data.config import *
from data.gui_texts import (PAUSE_MENU_CAPTION, OPTIONS_WINDOW_CAPTION,
                            STATS_WINDOW_CAPTION, MAP_WINDOW_CAPTION)
from utils import H, W



class PauseMenu:
    """ Pause menu, which the player can go to during the game.
    Includes statistics window, map window, options window and exit button.
    """
    def __init__(self, game):
        self.game = game

        xo = SCR_W2 - H(584)  # x-coord of  top-left corner of pause menu

        self.windows = (
            StatsWindow(xo),
            MapWindow(xo),
            OptionsWindow(xo, game.sound_player)
        )
        self.current_window = STATS_WINDOW

        self.side_buttons = (
            SideButton(xo, H(160), STATS_WINDOW_CAPTION, True),
            SideButton(xo, H(352), MAP_WINDOW_CAPTION, False),
            SideButton(xo, H(544), OPTIONS_WINDOW_CAPTION, False)
        )
        self.masks = (
            (pg.Surface(SCR_SIZE), (0, 0)),
            (pg.Surface((H(1072), H(760))), (xo + H(96), H(160)))
        )
        self.masks[0][0].set_alpha(175)
        self.masks[1][0].set_alpha(125)

        self.bg_surface = pg.Surface(SCR_SIZE)
        self.caption = Text(W(528), H(40), FONT_1, H(56), WHITE)

        self.running = True

    def set_language(self, language):
        for window in self.windows:
            window.set_language(language)
        for button in self.side_buttons:
            button.set_language(language)
        self.caption.set_text(PAUSE_MENU_CAPTION[language])

    def reset(self):
        """Method is called when a new game is started. Resets map
        in the map window and player statistics in the stats window.
        Also sets stats window as a current window.
        """
        self.windows[MAP_WINDOW].reset()
        self.windows[OPTIONS_WINDOW].reset()
        self.windows[STATS_WINDOW].set_player_stats((0, 0))
        self.set_current_window(STATS_WINDOW)

    def set_current_window(self, window):
        self.side_buttons[self.current_window].pressed = False
        self.current_window = window
        self.side_buttons[self.current_window].pressed = True
        if window == MAP_WINDOW:
            self.windows[MAP_WINDOW].map.reset_offset()

    def set_stats_window(self, player_state):
        self.windows[STATS_WINDOW].set_player_stats(player_state)

    def update_map_data(self, room_pos, boss_state):
        """Adds information about visited room and boss location to the map. """
        self.windows[MAP_WINDOW].map.add_visited_room(room_pos)
        if boss_state == BOSS_IN_CURRENT_ROOM:
            self.windows[MAP_WINDOW].map.boss_aim.pos = room_pos

    def handle_mouse_click(self, e_type):
        """Handles situations when mouse left button was pressed or unpressed. """
        if self.current_window == OPTIONS_WINDOW:
            self.running = self.game.running = not self.windows[OPTIONS_WINDOW].handle(e_type)

        elif self.current_window == MAP_WINDOW:
            self.windows[MAP_WINDOW].map.handle_mouse_click(e_type)

        if e_type == pg.MOUSEBUTTONDOWN:
            for window, button in enumerate(self.side_buttons):
                if button.clicked:
                    self.set_current_window(window)
                    break

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key in [pg.K_ESCAPE, pg.K_p]:
                self.running = False
            elif (event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP] and
                    event.button == pg.BUTTON_LEFT):
                self.handle_mouse_click(event.type)

    def draw(self, screen):
        """Draws all objects in the background and pause menu items. """
        screen.blit(self.bg_surface, (0, 0))

        self.game.draw_foreground()

        for mask, pos in self.masks:
            screen.blit(mask, pos)
        self.caption.draw(screen)
        self.windows[self.current_window].draw(screen)
        for button in self.side_buttons:
            button.draw(screen)
        pg.display.update()

    def run(self):
        """Pause menu loop which starts when player pressed pause key. """
        self.game.draw_background(self.bg_surface)
        self.game.player.stop_moving()

        self.running = True
        self.game.dt = 0

        self.windows[MAP_WINDOW].map.reset_offset()
        self.windows[OPTIONS_WINDOW].reset()

        while self.running:
            self.handle_events()

            self.game.update_scaling_objects()
            self.windows[self.current_window].update(self.game.dt)

            self.draw(self.game.screen)

            self.game.dt = self.game.clock.tick()
            self.game.fps_manager.update(self.game.dt)


__all__ = ["PauseMenu"]

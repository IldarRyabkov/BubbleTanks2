import sys
import pygame as pg

from gui.stats_window import StatsWindow
from gui.map_window import MapWindow
from gui.options_window import OptionsWindow
from gui.exit_button import ExitButton
from gui.side_button import SideButton
from gui.text import Text
from data.paths import FONT_1
from data.colors import WHITE
from data.config import *
from data.gui_texts import PAUSE_MENU_CAPTIONS as CAPTIONS
from utils import H, W



class PauseMenu:
    """ Pause menu, which the player can go to during the game.
    Includes statistics window, map window, options window and exit button.
    """
    def __init__(self, sounds):
        xo = SCR_W2 - H(584)  # x-coord of  top-left corner of pause menu

        self.windows = (
            StatsWindow(xo),
            MapWindow(xo),
            OptionsWindow(xo, sounds)
        )
        self.current_window = STATS_WINDOW

        self.side_buttons = (
            SideButton(xo, H(160), "stats_button", True),
            SideButton(xo, H(352), "map_button", False),
            SideButton(xo, H(544), "options_button", False)
        )
        self.masks = (
            (pg.Surface(SCR_SIZE), (0, 0)),
            (pg.Surface((H(1072), H(760))), (xo + H(96), H(160)))
        )
        self.masks[0][0].set_alpha(150)
        self.masks[1][0].set_alpha(125)

        self.bg_surface = pg.Surface(SCR_SIZE)
        self.caption = Text(W(528), H(40), FONT_1, H(56), WHITE)

        self.exit_button = ExitButton(xo)

        self.running = True
        self.game_running = True
        self.set_language("English")

    def set_language(self, language):
        for window in self.windows:
            window.set_language(language)
        for button in self.side_buttons:
            button.set_language(language)
        self.caption.set_text(CAPTIONS[language])

    def reset(self):
        """Method is called when a new game is started. Resets map
        in the map window and player statistics in the stats window.
        Also sets stats window as a current window.
        """
        self.windows[MAP_WINDOW].reset()
        self.windows[STATS_WINDOW].set_player_stats((0, 0))
        self.set_current_window(STATS_WINDOW)

    def set_current_window(self, window):
        self.side_buttons[self.current_window].clicked = False
        self.current_window = window
        self.side_buttons[self.current_window].clicked = True
        if window == MAP_WINDOW:
            self.windows[MAP_WINDOW].map.reset_offset()

    def set_stats_window(self, player_state):
        self.windows[STATS_WINDOW].set_player_stats(player_state)

    def set(self):
        self.running = True
        self.game_running = True
        self.windows[MAP_WINDOW].map.reset_offset()

    def update_map_data(self, room_pos, boss_state):
        """Adds information about visited room and boss location to the map. """
        self.windows[MAP_WINDOW].map.add_visited_room(room_pos)
        if boss_state == BOSS_IN_CURRENT_ROOM:
            self.windows[MAP_WINDOW].map.boss_aim.pos = room_pos

    def handle_mouse_click(self, e_type):
        if self.current_window == OPTIONS_WINDOW:
            self.running = self.game_running = self.windows[OPTIONS_WINDOW].handle(e_type)

        elif self.current_window == MAP_WINDOW:
            self.windows[MAP_WINDOW].map.handle_mouse_click(e_type)

        if e_type == pg.MOUSEBUTTONDOWN:
            if self.exit_button.cursor_on_button:
                self.running = False
            for window, button in enumerate(self.side_buttons):
                if button.cursor_on_button:
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

    def update(self, dt):
        self.windows[self.current_window].update(dt)

    def draw(self, screen):
        for mask, pos in self.masks:
            screen.blit(mask, pos)
        self.caption.draw(screen)
        self.windows[self.current_window].draw(screen)
        for button in self.side_buttons:
            button.draw(screen)
        self.exit_button.draw(screen)
        pg.display.update()


__all__ = ["PauseMenu"]

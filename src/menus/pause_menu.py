import sys
import pygame as pg

from gui.stats_window import StatsWindow
from gui.map_window import MapWindow
from gui.options_window import OptionsWindow
from gui.exit_button import ExitButton
from gui.side_button import SideButton
from data.paths import FONT_1, PAUSE_MENU_MASK
from data.colors import WHITE
from data.config import SCR_SIZE, SCR_W2, BOSS_IN_CURRENT_ROOM
import data.languages.english as eng
import data.languages.russian as rus


STATS_WINDOW = 0
MAP_WINDOW = 1
OPTIONS_WINDOW = 2


class PauseMenu:
    def __init__(self, sounds):
        self.windows = [StatsWindow(), MapWindow(), OptionsWindow(sounds)]
        self.mask = pg.image.load(PAUSE_MENU_MASK).convert_alpha()
        self.bg_surface = pg.Surface(SCR_SIZE)
        self.caption = None
        self.current_window = STATS_WINDOW
        self.side_buttons = [SideButton(65, 160, "stats_button", True),
                             SideButton(65, 352, "map_button", False),
                             SideButton(65, 544, "options_button", False)]
        self.exit_button = ExitButton()
        self.running = True
        self.game_running = True
        self.set_language("English")

    def set_language(self, language):
        for window in self.windows:
            window.set_language(language)
        for button in self.side_buttons:
            button.set_language(language)
        self.set_caption_language(language)

    def set_caption_language(self, language):
        pg.font.init()
        text = eng.PAUSEMENU_CAPTION if language == "English" else rus.PAUSEMENU_CAPTION
        font = pg.font.Font(FONT_1, 56)
        self.caption = font.render(text, True, WHITE)

    def reset(self):
        self.windows[MAP_WINDOW].reset()
        self.windows[STATS_WINDOW].set_player_stats((0, 0))

    def set_stats_window(self, player_state):
        self.windows[STATS_WINDOW].set_player_stats(player_state)

    def set_params_before_running(self):
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
            self.windows[MAP_WINDOW].map.handle(e_type)

        if e_type == pg.MOUSEBUTTONDOWN:
            self.running = not self.exit_button.cursor_on_button
            for i, button in enumerate(self.side_buttons):
                if button.cursor_on_button():
                    for b in self.side_buttons:
                        b.clicked = False
                    button.clicked = True
                    self.current_window = i
                    if self.current_window == MAP_WINDOW:
                        self.windows[MAP_WINDOW].map.reset_offset()
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
        self.exit_button.update()

    def draw(self, screen):
        screen.blit(self.mask, (0, 0))
        screen.blit(self.caption, (SCR_W2 - 112, 40))
        self.windows[self.current_window].draw(screen)
        for button in self.side_buttons:
            button.draw(screen)
        self.exit_button.draw(screen)

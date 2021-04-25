import sys
import pygame as pg

from gui.stats_window import StatsWindow
from gui.map_window import MapWindow
from gui.options_window import OptionsWindow
from gui.exit_button import ExitButton
from gui.side_button import SideButton
from data.paths import FONT_1, PAUSE_MENU_MASK
from data.colors import WHITE
from data.config import SCR_SIZE, SCR_W2
import data.languages.english as eng
import data.languages.russian as rus


STATS_WINDOW = 0
MAP_WINDOW = 1
OPTIONS_WINDOW = 2


class PauseMenu:
    def __init__(self):
        self.mask = pg.image.load(PAUSE_MENU_MASK).convert_alpha()
        self.bg_surface = pg.Surface(SCR_SIZE)
        self.caption = None
        self.windows = [StatsWindow(), MapWindow(), OptionsWindow()]
        self.current_window = STATS_WINDOW
        self.side_buttons = [SideButton(65, 160, "stats_button", True),
                             SideButton(65, 352, "map_button", False),
                             SideButton(65, 544, "options_button", False)]
        self.exit_button = ExitButton()
        self.running = True
        self.game_running = True
        self.clock = pg.time.Clock()
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

    def set_boss_location(self):
        self.windows[MAP_WINDOW].game_map.set_boss_location()

    def update_game_map(self, room_coords):
        self.windows[MAP_WINDOW].game_map.update_data(room_coords)

    def show_fps(self):
        pg.display.set_caption('FPS: ' + str(int(self.clock.get_fps()/2)))

    def handle_mouse_click(self, e_type, sounds):
        if e_type == pg.MOUSEBUTTONDOWN and self.exit_button.cursor_on_button():
            self.running = False
            self.exit_button.color = self.exit_button.colors[0]

        elif self.current_window == OPTIONS_WINDOW:
            running = self.windows[OPTIONS_WINDOW].handle(e_type, sounds)
            self.running = self.game_running = running

        if e_type == pg.MOUSEBUTTONDOWN:
            for i in range(len(self.side_buttons)):
                if self.side_buttons[i].cursor_on_button():
                    for button in self.side_buttons:
                        button.clicked = False
                    self.side_buttons[i].clicked = True
                    self.current_window = i
                    break

    def handle_events(self, sounds):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key in [pg.K_ESCAPE, pg.K_p]:
                self.running = False
            elif (event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP] and
                          event.button == pg.BUTTON_LEFT):
                self.handle_mouse_click(event.type, sounds)

    def update(self, dt, player, bubbles, mobs, bullets, sounds):
        if player.superpower.name == "Ghost":
            player.superpower.update_body(player.body)
        player.update_body(dt)
        for mob in mobs:
            mob.update_body(dt, (player.x, player.y))
        for bubble in bubbles:
            bubble.update_body(dt)
        for bullet in player.bullets:
            bullet.update_body(dt)
        for shuriken in player.shurikens:
            if shuriken.is_orbiting:
                shuriken.update_polar_coords(*player.pos, dt)
        for bullet in bullets:
            bullet.update_body(dt)
        if self.current_window == OPTIONS_WINDOW:
            self.windows[self.current_window].update(sounds)
        else:
            self.windows[self.current_window].update(dt)
        self.exit_button.update()

    def draw(self, screen, draw_foreground):
        screen.blit(self.bg_surface, (0, 0))
        draw_foreground()
        screen.blit(self.mask, (0, 0))
        screen.blit(self.caption, (SCR_W2 - 112, 40))
        self.windows[self.current_window].draw(screen)
        for button in self.side_buttons:
            button.draw(screen)
        self.exit_button.draw(screen)
        pg.display.update()

    def run(self, screen, player, bubbles, mobs, bullets, draw_foreground, sounds):
        self.running = True
        self.game_running = True
        dt = 0
        while self.running:
            self.handle_events(sounds)
            self.clock.tick()
            self.update(dt, player, bubbles, mobs, bullets, sounds)
            self.draw(screen, draw_foreground)
            dt = self.clock.tick()
            self.show_fps()
import pygame as pg

from .text_button import TextButton

from data.constants import *
from data.scripts import load_save_data
from data.player import PLAYER_PARAMS
from data.languages.texts import TEXTS
from assets.paths import *
from gui.widgets.tank_body_smooth import TankBodySmooth
from components.utils import *


class SaveButton(TextButton):
    def __init__(self, x, save_name, sound_player, save_button_action):
        y = H(470)
        super().__init__(x, y + H(146), None, CALIBRI_BOLD, H(40), 210, sound_player,
                         w=H(310), action=lambda: save_button_action(self))

        self.save_name = save_name
        self.save_data = None
        self.tank_body = None
        self.bg = None
        self.language = None

        self.rect.w = H(310)
        self.rect.h = H(400)
        self.rect.center = x, y

    def draw_status_bars(self):
        rect = pg.Rect(0, 0, H(230), H(17))
        rect.centerx = self.rect.w // 2
        rect.y = H(280)

        health_rect = pg.Rect(0, 0, H(230), H(17))
        max_health = PLAYER_PARAMS[tuple(self.save_data["tank"])]["max_health"]
        if self.save_data["health"] < max_health and self.save_data["tank"][0] != 5:
            health_rect.w = self.save_data["health"] / max_health * rect.w
        health_rect.topleft = rect.topleft

        for key in self.bg:
            pg.draw.rect(self.bg[key], PLAYER_BG_COLOR, rect, width=H(2))
            pg.draw.rect(self.bg[key], PLAYER_BG_COLOR, health_rect)

    def create_bg_images(self):
        self.bg = {
            False: pg.image.load(SAVE_BUTTON_BG).convert_alpha(),
            True: pg.image.load(SAVE_BUTTON_PRESSED_BG).convert_alpha()
        }
        for key, image in self.bg.items():
            self.bg[key] = pg.transform.smoothscale(image, self.rect.size)

    def load_save_data(self):
        self.create_bg_images()
        self.save_data = load_save_data(self.save_name)
        if self.save_data is not None:
            tank = tuple(self.save_data["tank"])
            self.set_text(self.save_data["time"])
            self.draw_status_bars()
        else:
            tank = None
            self.set_text(TEXTS["save button text"][self.language])

        x, y = self.rect.center
        self.tank_body = TankBodySmooth(x, y - H(60), no_background=True)
        self.tank_body.set_body(tank)

    def set_language(self, language):
        self.language = language

    def set_bg_alpha(self, alpha):
        for image in self.bg.values():
            image.set_alpha(alpha)

    def update_look(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if self.tank_body is not None:
            self.tank_body.update(dt, animation_state=animation_state,
                                  time_elapsed=time_elapsed)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        super().update(dt, animation_state, time_elapsed)
        if animation_state == WAIT:
            self.set_bg_alpha(255)
        if animation_state == OPEN:
            self.set_bg_alpha(round(255 * time_elapsed))
        elif animation_state == CLOSE:
            self.set_bg_alpha(round(255 - 255 * time_elapsed))

    def draw(self, screen, animation_state=WAIT):
        screen.blit(self.bg[self.cursor_on_button], self.rect.topleft)
        super().draw(screen, animation_state)
        if self.tank_body is not None:
            self.tank_body.draw(screen, animation_state=animation_state)


__all__ = ["SaveButton"]

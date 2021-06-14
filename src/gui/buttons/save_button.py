import pygame as pg

from .scaling_button import ScalingButton

from data.constants import *
from data.scripts import load_save_file
from data.player import PLAYER_PARAMS
from data.languages.texts import TEXTS

from assets.paths import *
from components.utils import *

from gui.widgets.tank_body_smooth import TankBodySmooth
from gui.widgets.text_widget import TextWidget


class SaveButton(ScalingButton):
    def __init__(self, x, save_name, sound_player, save_button_action):
        y = H(470)
        super().__init__(x, H(490), H(330), H(420), 0.9, 180, None,
                         sound_player, click_sound=None,
                         action=lambda: save_button_action(self))

        self.save_name = save_name
        self.save_data = None
        self.tank_body = TankBodySmooth(self.x, self.y - H(60), no_background=True)
        self.bg = None
        self.language = None

        self.label = TextWidget(self.w//2, H(360), CALIBRI_BOLD, H(40), WHITE, 1)

        self.image = pg.image.load(SAVE_BUTTON_BG).convert_alpha()
        self.surface = pg.transform.smoothscale(self.image, (round(self.w), round(self.h)))

    @property
    def clicked(self):
        clicked = self.is_pressed and self.cursor_on_button
        self.is_pressed = False
        return clicked

    def set_label_text(self):
        if self.save_data is None:
            text = TEXTS["save button text"][self.language]
        else:
            text = self.save_data["time"]
        self.label.set_text(text)

    def set_tank_body(self):
        if self.save_data is not None:
            tank = tuple(self.save_data["tank"])
        else:
            tank = None
        self.tank_body.set_body(tank)

    def draw_status_bar(self):
        rect = pg.Rect(0, 0, H(270), H(17))
        rect.centerx = self.w // 2
        rect.y = H(290)

        health_rect = rect.copy()
        max_health = PLAYER_PARAMS[tuple(self.save_data["tank"])]["max_health"]
        health = self.save_data["health"]
        tank_level = self.save_data["tank"][0]
        if health < max_health and tank_level != 5:
            health_rect.w = 0.2 * (tank_level + health/max_health) * rect.w

        pg.draw.rect(self.surface, WHITE, rect, width=H(2))
        pg.draw.rect(self.surface, WHITE, health_rect)

    def load_save_data(self):
        self.save_data = load_save_file(self.save_name)
        self.set_label_text()
        self.set_tank_body()

    def set_language(self, language):
        self.language = language
        self.set_label_text()
        self.render_surface()

    def set_bg_alpha(self, alpha):
        for image in self.bg.values():
            image.set_alpha(alpha)

    def update_look(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if self.tank_body is not None:
            self.tank_body.update(dt, animation_state=animation_state,
                                  time_elapsed=time_elapsed)

    def set_surface(self):
        self.surface = pg.transform.smoothscale(self.image, (round(self.w), round(self.h)))
        self.label.draw(self.surface)
        if self.save_data is not None:
            self.draw_status_bar()

    def draw(self, screen, animation_state=WAIT):
        super().draw(screen, animation_state)
        self.tank_body.draw(screen, animation_state)


__all__ = ["SaveButton"]

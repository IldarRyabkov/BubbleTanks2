import pygame as pg

from gui.buttons.button import Button
from gui.widgets.text_widget import TextWidget
from assets.paths import *
from data.constants import *
from data.scripts import update_config_file
from components.utils import H


class ControlButton(Button):
    def __init__(self, x, y, texts, controls, control_name, sound_player, control_button_action, k=1):
        super().__init__(pg.SYSTEM_CURSOR_HAND, sound_player, BUTTON_CLICK,
                         action=lambda: control_button_action(self))
        self.active = False
        self.k = k  # scale factor
        self.rect.size = H(550 * k), H(86 * k)
        self.rect.topleft = x, y
        self.surface = pg.Surface(self.rect.size, pg.SRCALPHA)
        self.controls = controls
        self.control_name = control_name
        self.label = TextWidget(H(224 * k), H(21 * k),  CALIBRI_BOLD, H(44 * k), LIGHT_GREY, align=2)
        self.label_texts = texts
        self.value_rect = pg.Rect(0, 0, 0, H(82 * k))
        self.click_area = pg.Rect(0, y, 0, H(82 * k))
        self.value = TextWidget(H(375 * k), H(20 * k), CALIBRI_BOLD, H(46 * k), LIGHT_GREY, align=1)
        self.set_value()

    @property
    def cursor_on_button(self):
        return self.click_area.collidepoint(pg.mouse.get_pos())

    def set_language(self, language):
        self.label.set_text(self.label_texts[language])
        self.render_surface()

    def set_value(self):
        text = pg.key.name(self.controls[self.control_name]).upper()
        self.value.set_text(text)
        self.value_rect.w = max(H(82 * self.k), self.value.w + H(42 * self.k))
        self.value_rect.x = self.value.x - self.value_rect.w//2
        self.click_area.x = self.rect.x + self.value_rect.x
        self.click_area.w = self.value_rect.w
        self.render_surface()

    def reset(self, state):
        super().reset(state)
        self.set_value()

    def activate(self):
        self.active = True
        self.render_surface()

    def deactivate(self):
        self.active = False
        self.render_surface()

    def set_control(self, key_code):
        self.controls[self.control_name] = key_code
        self.set_value()
        update_config_file(controls=self.controls)

    def change_control(self, key_code):
        if key_code in self.controls.values():
            return
        try:
            key_code = pg.key.key_code(pg.key.name(key_code))
        except ValueError:
            return
        else:
            self.set_control(key_code)

    def render_surface(self):
        width = H(5) if self.active else H(2.5)
        color = WHITE if self.active else LIGHT_GREY
        self.surface.fill((0, 0, 0, 0))
        self.label.draw(self.surface)
        self.value.set_color(color)
        self.value.draw(self.surface)
        pg.draw.rect(self.surface, color, self.value_rect, width=width, border_radius=H(24))

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if animation_state == WAIT:
            if self.surface.get_alpha() != 255:
                self.surface.set_alpha(255)
        elif animation_state == OPEN:
            self.surface.set_alpha(round(255 * time_elapsed))
        elif animation_state == CLOSE:
            self.surface.set_alpha(round(255 * (1 - time_elapsed)))

    def draw(self, screen, animation_state=WAIT):
        screen.blit(self.surface, self.rect)


__all__ = ["ControlButton"]

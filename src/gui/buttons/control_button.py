import pygame as pg

from gui.buttons.button import Button
from gui.widgets.text_widget import TextWidget
from assets.paths import *
from data.constants import *
from data.scripts import update_config_file
from components.utils import H


class ControlButton(Button):
    def __init__(self, x, y, texts, controls, control_name, sound_player, control_button_action):
        super().__init__(pg.SYSTEM_CURSOR_HAND, sound_player, BUTTON_CLICK,
                         action=lambda: control_button_action(self))
        self.active = False
        self.rect.size = H(550), H(86)
        self.rect.topleft = x, y
        self.surface = pg.Surface(self.rect.size, pg.SRCALPHA)
        self.controls = controls
        self.control_name = control_name
        self.label = TextWidget(H(224), H(21), CALIBRI_BOLD, H(44), WHITE, align=2)
        self.label_texts = texts
        self.value_rect = pg.Rect(0, 0, 0, H(82))
        self.click_area = pg.Rect(0, y, 0, H(82))
        self.value = TextWidget(H(375), H(20), CALIBRI_BOLD, H(46), LIGHT_GREY, align=1)
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
        self.value_rect.w = max(H(82), self.value.w + H(42))
        self.value_rect.x = self.value.x - self.value_rect.w//2
        self.click_area.x = self.rect.x + self.value_rect.x
        self.click_area.w = self.value_rect.w
        self.render_surface()

    def activate(self):
        self.active = True
        self.value.set_color(WHITE)
        self.render_surface()

    def deactivate(self):
        self.active = False
        self.value.set_color(LIGHT_GREY)
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
        self.surface.fill((0, 0, 0, 0))
        self.label.draw(self.surface)
        self.value.draw(self.surface)
        width = H(5) if self.active else H(3)
        color = WHITE if self.active else LIGHT_GREY
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

import pygame as pg

from data.paths import *
from constants import *
from languages.texts import TEXTS
from gui.text_widget import TextWidget
from utils import H, HF


class ButtonType:
    LEFT = 0
    CENTER = 1
    RIGHT = 2
    WIDE_LEFT = 3
    WIDE_RIGHT = 4


class UpgradeButton:
    """Button that is used in upgrade menu.
    It contains description of new tank, its weapon and superpower.
    It appears when the upgrade menu opens and hides when it closes.
    """
    def __init__(self, button_type, tank, language, sound_player, animation_duration):
        self.sound_player = sound_player
        self.sound_lock = False
        self.tank = tank
        self.w = HF(480) if button_type in (ButtonType.WIDE_LEFT, ButtonType.WIDE_RIGHT) else HF(352)
        self.h = HF(736)

        if button_type == ButtonType.LEFT:
            self.X0, self.Y0 = -self.w, HF(160)
            self.X1, self.Y1 = SCR_W2 - HF(592), HF(160)

        elif button_type == ButtonType.CENTER:
            self.X0, self.Y0 = SCR_W2 - HF(176), SCR_H
            self.X1, self.Y1 = SCR_W2 - HF(176), HF(160)

        elif button_type == ButtonType.RIGHT:
            self.X0, self.Y0 = SCR_W, HF(160)
            self.X1, self.Y1 = SCR_W2 + HF(240), HF(160)

        elif button_type == ButtonType.WIDE_LEFT:
            self.X0, self.Y0 = -self.w, HF(160)
            self.X1, self.Y1 = SCR_W2 - HF(512), HF(160)

        elif button_type == ButtonType.WIDE_RIGHT:
            self.X0, self.Y0 = SCR_W, HF(160)
            self.X1, self.Y1 = SCR_W2 + HF(32), HF(160)

        self.x, self.y = self.X0, self.Y0
        self.vel_x = (self.X1 - self.X0) / animation_duration
        self.vel_y = (self.Y1 - self.Y0) / animation_duration

        # Now we set button background surfaces.
        # First we load background images of button.
        if button_type in (ButtonType.WIDE_LEFT, ButtonType.WIDE_RIGHT):
            image = pg.image.load(UPGRADE_BUTTON_WIDE_BG).convert_alpha()
            image_pressed = pg.image.load(UPGRADE_BUTTON_WIDE_PRESSED_BG).convert_alpha()
        else:
            image = pg.image.load(UPGRADE_BUTTON_BG).convert_alpha()
            image_pressed = pg.image.load(UPGRADE_BUTTON_PRESSED_BG).convert_alpha()
        size = (round(self.w), round(self.h))
        self.bg = (
            pg.transform.scale(image, size),
            pg.transform.scale(image_pressed, size),
        )
        # Then we create text widget to be blitted on background surfaces of button
        width = self.w - HF(30)
        text_widgets = (
            TextWidget(self.w / 2, HF(6), FONT_1, H(48), UPG_LABEL_COLOR, 1, width),  # button caption
            TextWidget(self.w / 2, HF(264), CALIBRI_BOLD, H(35), BLACK, 1, width),  # main weapon caption
            TextWidget(self.w / 2, HF(384), CALIBRI_BOLD, H(35), BLACK, 1, width),  # second weapon caption
            TextWidget(self.w / 2, HF(166), CALIBRI_BOLD, H(35), BLACK, 1, width),  # tank name
            TextWidget(self.w / 2, HF(312), CALIBRI, H(31), BLACK, 1, width),  # main weapon name
            TextWidget(self.w / 2, HF(432), CALIBRI, H(31), BLACK, 1, width),  # second weapon name
            TextWidget(HF(15), HF(536), CALIBRI, H(31), BLACK, 0, width),  # tank description
        )
        texts = (TEXTS["upgrade button labels"][language] +
                 TEXTS["tank descriptions"][language][tank][:4])
        for widget, text in zip(text_widgets, texts):
            widget.set_text(text)

        # And finally we blit text widgets on background surfaces of button
        for bg in self.bg:
            for widget in text_widgets:
                widget.draw(bg)

    @property
    def cursor_on_button(self):
        x, y = pg.mouse.get_pos()
        return 0 <= x - self.x <= self.w and 0 <= y - self.y <= self.h

    @property
    def clicked(self):
        if self.cursor_on_button:
            self.sound_player.play_sound(UI_CLICK)
            return True
        return False

    def update(self, dt, animation_state=WAIT):
        if animation_state == OPEN:
            dx = self.vel_x * dt
            dy = self.vel_y * dt
            self.x = min(self.x + dx, self.X1) if self.vel_x > 0 else max(self.x + dx, self.X1)
            self.y = min(self.y + dy, self.Y1) if self.vel_y > 0 else max(self.y + dy, self.Y1)

        elif animation_state == CLOSE:
            dx = -self.vel_x * dt
            dy = -self.vel_y * dt
            self.x = max(self.x + dx, self.X0) if self.vel_x > 0 else min(self.x + dx, self.X0)
            self.y = max(self.y + dy, self.Y0) if self.vel_y > 0 else min(self.y + dy, self.Y0)

        elif animation_state == WAIT:
            if not self.cursor_on_button:
                self.sound_lock = False
            elif not self.sound_lock:
                self.sound_player.play_sound(UI_CHOOSE)
                self.sound_lock = True


    def draw(self, screen):
        screen.blit(self.bg[self.cursor_on_button], (round(self.x), round(self.y)))


__all__ = [

    "ButtonType",
    "UpgradeButton"

]

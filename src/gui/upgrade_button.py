import pygame as pg

from data.colors import BLACK, UPG_LABEL_COLOR
from data.paths import *
from data.config import *
from data.gui_texts import UPGRADE_BUTTON_TEXTS as TEXTS
from gui.text import Text
from utils import H, HF


class UpgradeButton:
    """Button that is used in upgrade menu.
    It contains description of new tank, its weapon and superpower.
    It appears when the upgrade menu opens and hides when it closes.
    """
    def __init__(self, button_type, tank, language):
        self.tank = tank
        self.w = HF(480) if button_type in (UPG_BUTTON_WIDE_LEFT, UPG_BUTTON_WIDE_RIGHT) else HF(352)
        self.h = HF(736)

        if button_type == UPG_BUTTON_LEFT:
            self.X0, self.Y0 = -self.w, HF(160)
            self.X1, self.Y1 = SCR_W2 - HF(592), HF(160)

        elif button_type == UPG_BUTTON_CENTER:
            self.X0, self.Y0 = SCR_W2 - HF(176), SCR_H
            self.X1, self.Y1 = SCR_W2 - HF(176), HF(160)

        elif button_type == UPG_BUTTON_RIGHT:
            self.X0, self.Y0 = SCR_W, HF(160)
            self.X1, self.Y1 = SCR_W2 + HF(240), HF(160)

        elif button_type == UPG_BUTTON_WIDE_LEFT:
            self.X0, self.Y0 = -self.w, HF(160)
            self.X1, self.Y1 = SCR_W2 - HF(512), HF(160)

        elif button_type == UPG_BUTTON_WIDE_RIGHT:
            self.X0, self.Y0 = SCR_W, HF(160)
            self.X1, self.Y1 = SCR_W2 + HF(32), HF(160)

        self.x, self.y = self.X0, self.Y0
        self.vel_x = (self.X1 - self.X0) / UPGRADE_MENU_ANIMATION_TIME
        self.vel_y = (self.Y1 - self.Y0) / UPGRADE_MENU_ANIMATION_TIME

        # Now we set button background surfaces.
        # First we load background images of button.
        if button_type in (UPG_BUTTON_WIDE_LEFT, UPG_BUTTON_WIDE_RIGHT):
            image = pg.image.load(UPGRADE_BUTTON_WIDE).convert_alpha()
            image_pressed = pg.image.load(UPGRADE_BUTTON_WIDE_PRESSED).convert_alpha()
        else:
            image = pg.image.load(UPGRADE_BUTTON).convert_alpha()
            image_pressed = pg.image.load(UPGRADE_BUTTON_PRESSED).convert_alpha()
        size = (round(self.w), round(self.h))
        self.bg = (
            pg.transform.scale(image, size),
            pg.transform.scale(image_pressed, size),
        )
        # Then we create text widget to be blitted on background surfaces of button
        text_widgets = (
            Text(self.w / 2, HF(6),   FONT_1,  H(48), UPG_LABEL_COLOR, True),  # button caption
            Text(self.w / 2, HF(264), CALIBRI_BOLD, H(35), BLACK, True),  # main weapon caption
            Text(self.w / 2, HF(384), CALIBRI_BOLD, H(35), BLACK, True),  # second weapon caption
            Text(self.w / 2, HF(166), CALIBRI_BOLD,  H(35), BLACK, True),  # tank name
            Text(self.w / 2, HF(312), CALIBRI,  H(31), BLACK, True),  # main weapon name
            Text(self.w / 2, HF(432), CALIBRI,  H(31), BLACK, True),  # second weapon name
            Text(HF(8), HF(536), CALIBRI, H(31), BLACK, False),  # tank description
        )
        texts = TEXTS[language]["labels"] + list(TEXTS[language]["texts"][tank][:4])
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

    def update_pos(self, dt, action):
        if action == OPEN:
            dx = self.vel_x * dt
            dy = self.vel_y * dt
            self.x = min(self.x + dx, self.X1) if self.vel_x > 0 else max(self.x + dx, self.X1)
            self.y = min(self.y + dy, self.Y1) if self.vel_y > 0 else max(self.y + dy, self.Y1)
        else:
            dx = -self.vel_x * dt
            dy = -self.vel_y * dt
            self.x = max(self.x + dx, self.X0) if self.vel_x > 0 else min(self.x + dx, self.X0)
            self.y = max(self.y + dy, self.Y0) if self.vel_y > 0 else min(self.y + dy, self.Y0)

    def draw(self, screen):
        screen.blit(self.bg[self.cursor_on_button], (round(self.x), round(self.y)))

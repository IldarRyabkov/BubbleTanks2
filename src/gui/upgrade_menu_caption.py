import pygame as pg

from constants import *
from gui.text_widget import TextWidget
from data.paths import *
from utils import H, HF
from languages.texts import TEXTS


class UpgradeMenuCaption:
    """Caption of the upgrade menu. It appears when
    upgrade menu opens and hides when it closes.
    """
    def __init__(self):
        self.w = H(1184)
        self.h = H(112)

        self.x = SCR_W2 - HF(592)
        self.y = -HF(112)
        self.Y0 = -HF(112)
        self.Y1 = HF(16)

        self.image = pg.image.load(UPGRADE_CAPTION).convert_alpha()
        self.bg_surface = None
        self.text_widget = TextWidget(self.w/2, H(18), FONT_1, H(76), UPG_LABEL_COLOR, 1)

    def reset(self):
        self.y = self.Y0

    def set_language(self, language):
        self.text_widget.set_text(TEXTS["upgrade menu caption"][language])
        self.bg_surface = pg.transform.scale(self.image, (self.w, self.h))
        self.text_widget.draw(self.bg_surface)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        if animation_state == OPEN:
            self.y = self.Y0 + (self.Y1 - self.Y0) * time_elapsed
        elif animation_state == CLOSE:
            self.y = self.Y1 + (self.Y0 - self.Y1) * time_elapsed
        else:
            self.y = self.Y1

    def draw(self, surface):
        surface.blit(self.bg_surface, (round(self.x), round(self.y)))


__all__ = ["UpgradeMenuCaption"]

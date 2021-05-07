import pygame as pg

from data.config import UPGRADE_MENU_ANIMATION_TIME, SCR_W2, OPEN
from data.paths import UPGRADE_CAPTION_RUS, UPGRADE_CAPTION_ENG
from utils import H, HF


class UpgradeMenuCaption:
    """Caption of the upgrade menu. It appears when
    upgrade menu opens and hides when it closes.
    """
    def __init__(self):
        self.x = SCR_W2 - HF(592)
        self.y = -HF(112)
        self.Y0 = -HF(112)
        self.Y1 = HF(16)
        self.vel = (self.Y1 - self.Y0) / UPGRADE_MENU_ANIMATION_TIME
        self.surface = None

    def set_language(self, language):
        filename = UPGRADE_CAPTION_ENG if language == "English" else UPGRADE_CAPTION_RUS
        image = pg.image.load(filename).convert_alpha()
        self.surface = pg.transform.scale(image, (H(1184), H(112)))

    def update_pos(self, dt, action):
        if action == OPEN:
            dy = self.vel * dt
            self.y = min(self.y + dy, self.Y1) if self.vel > 0 else max(self.y + dy, self.Y1)
        else:
            dy = -self.vel * dt
            self.y = max(self.y + dy, self.Y0) if self.vel > 0 else min(self.y + dy, self.Y0)

    def draw(self, surface):
        surface.blit(self.surface, (round(self.x), round(self.y)))


__all__ = ["UpgradeMenuCaption"]

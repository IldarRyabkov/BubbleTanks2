from .popup_window import PopupWindow
from .status_bar import StatusBar
from .text_widget import TextWidget

from assets.paths import *
from data.languages import TEXTS
from data.constants import *
from components.utils import *


class HealthWindow(PopupWindow):
    """Window that shows status bar representing how many
    more bubbles the player needs to collect to upgrade his tank.
    """
    def __init__(self, game):
        super().__init__(game,
                         SCR_W2 - HF(456),
                         SCR_H,
                         HF(912),
                         HF(106),
                         -HF(1.12),
                         1250,
                         HEALTH_WINDOW_BG)
        self.status_bar = StatusBar(self.x + HF(16), self.y + HF(56), self.w - HF(32), H(32), 75)
        self.tank_label = TextWidget(self.x + HF(23), self.y + HF(18), CALIBRI_BOLD, H(32), WHITE)
        self.bubbles_label = TextWidget(0, self.y + HF(18), CALIBRI_BOLD, H(32), WHITE)
        self.widgets.append(self.status_bar)
        self.widgets.append(self.tank_label)
        self.widgets.append(self.bubbles_label)

    def reset(self):
        super().reset()
        self.status_bar.move_to(self.x + HF(16), self.y + HF(56))
        self.tank_label.move_to(self.tank_label.x, self.y + HF(9))
        self.bubbles_label.move_to(0, self.y + HF(9))

    def set_bubbles_label(self):
        labels = TEXTS["health window labels"][self.game.language]
        if self.player.level != 5:
            text = '%d %s' % (self.player.max_health - self.player.health, labels[0])
        else:
            text = labels[1]
        self.bubbles_label.set_text(text)
        self.bubbles_label.move_to(self.x + self.w - HF(23) - self.bubbles_label.w,
                                   self.bubbles_label.y)

    def activate(self):
        super().activate()
        if self.player.level != 5:
            self.status_bar.set_value(self.player.health)
            self.set_bubbles_label()

    def set(self):
        self.status_bar.set_max_value(self.player.max_health)
        value = self.player.health if self.player.level != 5 else self.player.max_health
        self.status_bar.set_value(value)
        self.tank_label.set_text(TEXTS["tank names"][self.game.language][self.player.tank])
        self.set_bubbles_label()


__all__ = ["HealthWindow"]

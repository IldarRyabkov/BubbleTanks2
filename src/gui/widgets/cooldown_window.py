from .status_bar import StatusBar
from .popup_window import PopupWindow
from .text_widget import TextWidget
from data.constants import SCR_W, WHITE
from data.languages.texts import TEXTS
from assets.paths import COOLDOWN_WINDOW_BG, CALIBRI_BOLD
from components.superpowers import *
from components.utils import H, HF


class CooldownWindow(PopupWindow):
    """Window that shows status bars for player's
    shooting cooldown and player's superpower cooldown.
    """
    def __init__(self, game):
        super().__init__(game,
                         SCR_W - HF(264),
                         -HF(96),
                         HF(248),
                         HF(96),
                         HF(1.12),
                         1000,
                         COOLDOWN_WINDOW_BG)
        self.player = self.game.player
        self.status_bar_1 = StatusBar(self.x + HF(56), self.y + HF(11), self.w - HF(72), H(32), 300)
        self.status_bar_2 = StatusBar(self.x + HF(56), self.y + HF(53), self.w - HF(72), H(32), 0)
        self.label_1 = TextWidget(self.x + HF(16), self.y + HF(14), CALIBRI_BOLD, H(27), WHITE)
        self.label_2 = TextWidget(self.x + HF(16), self.y + HF(56), CALIBRI_BOLD, H(27), WHITE)
        self.widgets.append(self.status_bar_1)
        self.widgets.append(self.status_bar_2)
        self.widgets.append(self.label_1)
        self.widgets.append(self.label_2)

    @property
    def shooting_active(self) -> bool:
        return self.player.shooting and not self.player.disassembled

    @property
    def superpower_active(self) -> bool:
        return (self.player.superpower.on and
                not isinstance(self.player.superpower,
                               (NoneSuperPower, Ghost, OrbitalSeekers)))

    def set_language(self, language):
        label_1, label_2 = TEXTS["cooldown window labels"][language]
        self.label_1.set_text(label_1)
        self.label_2.set_text(label_2)

    def reset(self):
        super().reset()
        self.status_bar_1.move_to(self.x + H(56), self.y + H(11))
        self.status_bar_2.move_to(self.x + H(56), self.y + H(53))
        self.label_1.move_to(self.x + H(16), int(self.y) + H(14))
        self.label_2.move_to(self.x + H(16), int(self.y) + H(56))

    def set(self,):
        self.status_bar_1.set_max_value(self.player.gun.cooldown_time)
        self.status_bar_1.set_value(0)
        self.status_bar_2.set_max_value(self.player.superpower.cooldown_time)
        self.status_bar_2.set_value(0)

    def update(self, dt):
        super().update(dt)
        if (self.shooting_active or self.superpower_active) and not self.game.transportation:
            self.activate()
        self.status_bar_1.set_value(self.player.gun.time, reset=True)
        self.status_bar_2.set_value(self.player.superpower.time, reset=True)


__all__ = ["CooldownWindow"]

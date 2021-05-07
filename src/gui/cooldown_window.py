from gui.status_bar import StatusBar
from gui.popup_window import PopupWindow
from gui.text import Text
from data.config import SCR_W
from data.colors import WHITE
from data.gui_texts import COOLDOWN_WINDOW_LABELS as LABELS
from data.paths import COOLDOWN_WINDOW_BG, CALIBRI_BOLD
from entities.superpowers import *
from utils import H, HF


class CooldownWindow(PopupWindow):
    """Window that shows status bars for player's
    shooting cooldown and player's superpower cooldown.
    """
    def __init__(self):
        super().__init__(SCR_W - HF(264),
                         -HF(96),
                         HF(248),
                         HF(96),
                         HF(1.12),
                         1000,
                         COOLDOWN_WINDOW_BG)
        self.status_bar_1 = StatusBar(self.x + HF(56), self.y + HF(11), self.w - HF(72), H(32), 300)
        self.status_bar_2 = StatusBar(self.x + HF(56), self.y + HF(53), self.w - HF(72), H(32), 0)
        self.label_1 = Text(self.x + HF(16), self.y + HF(14), CALIBRI_BOLD, H(27), WHITE)
        self.label_2 = Text(self.x + HF(16), self.y + HF(56), CALIBRI_BOLD, H(27), WHITE)
        self.set_language("English")

    def set_language(self, language):
        self.label_1.set_text(LABELS[language][0])
        self.label_2.set_text(LABELS[language][1])

    def reset(self):
        super().reset()
        self.status_bar_1.move_to(self.x + H(56), self.y + H(11))
        self.status_bar_2.move_to(self.x + H(56), self.y + H(53))
        self.label_1.move_to(self.x + H(16), int(self.y) + H(14))
        self.label_2.move_to(self.x + H(16), int(self.y) + H(56))

    def set(self, cooldown_time_1, cooldown_time_2):
        self.status_bar_1.set_max_value(cooldown_time_1)
        self.status_bar_1.set_value(0)
        self.status_bar_2.set_max_value(cooldown_time_2)
        self.status_bar_2.set_value(0)

    def update(self, dt, player, transportation):
        yo = self.y
        self.update_state(dt)
        dy = self.y - yo
        self.status_bar_1.move(0, dy)
        self.status_bar_2.move(0, dy)
        self.label_1.move(0, dy)
        self.label_2.move(0, dy)

        shooting_active = player.shooting and not player.invisible
        superpower_active = (player.superpower.on and
                             not isinstance(player.superpower, (NoneSuperPower, Ghost, Shurikens)))
        if (shooting_active or superpower_active) and not transportation:
            self.activate()

        self.status_bar_1.set_value(player.gun.time, reset=True)
        self.status_bar_2.set_value(player.superpower.time, reset=True)

    def draw(self, screen):
        if self.on_screen:
            screen.blit(self.background, (round(self.x), round(self.y)))
            self.label_1.draw(screen)
            self.label_2.draw(screen)
            self.status_bar_1.draw(screen)
            self.status_bar_2.draw(screen)


__all__ = ["CooldownWindow"]

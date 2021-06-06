from gui.buttons.text_button import TextButton
from constants import *
from data.paths import CALIBRI_BOLD
from data.scripts import save_resolution
from utils import *
from states import MainMenuStates as St


class ResolutionButton(TextButton):
    def __init__(self, menu, y, texts):
        super().__init__(SCR_W2, y, texts, CALIBRI_BOLD, H(56),
                         200, menu.game.sound_player,
                         action=self.set_new_resolution, w=H(300))
        self.menu = menu
        self.set_text(texts)

    def set_new_resolution(self):
        save_resolution(self.texts)
        self.menu.to_resolutions_button.set_value(self.texts)
        self.menu.set_state(St.SETTINGS, self)


__all__ = ["ResolutionButton"]

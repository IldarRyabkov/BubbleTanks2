from gui.buttons.text_button import TextButton
from data.constants import *
from data.scripts import update_config_file
from data.states import MainMenuStates as St
from assets.paths import CALIBRI_BOLD
from components.utils import *


class ResolutionButton(TextButton):
    def __init__(self, menu, y, texts):
        super().__init__(SCR_W2, y, texts, CALIBRI_BOLD, H(56),
                         200, menu.game.sound_player,
                         action=self.set_new_resolution, w=H(320))
        self.menu = menu
        self.set_text(texts)

    def set_new_resolution(self):
        resolution = list(map(int, self.texts.split(' x ')))
        update_config_file(resolution=resolution)
        self.menu.to_resolutions_button.set_value(self.texts)
        self.menu.set_state(St.SETTINGS, self)


__all__ = ["ResolutionButton"]

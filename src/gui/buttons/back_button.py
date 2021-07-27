from .text_button import TextButton
from data.constants import *
from assets.paths import *
from components.utils import H
from data.states import MainMenuStates as St


class BackButton(TextButton):
    def __init__(self, texts, sound_player, action):
        super().__init__(SCR_W2, H(675),
                         texts, CALIBRI_BOLD, H(56),
                         220, sound_player,
                         action=action, w=H(200))

    def reset(self, state):
        super().reset(state)
        if state == St.SETTINGS:
            self.move_to(y=H(785))
        else:
            self.move_to(y=H(850))


__all__ = ["BackButton"]

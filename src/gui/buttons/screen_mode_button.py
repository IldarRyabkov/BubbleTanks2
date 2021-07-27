from gui.buttons.text_button import TextButton
from data.constants import *
from data.scripts import update_config_file
from data.states import MainMenuStates as St
from assets.paths import CALIBRI_BOLD
from components.utils import *


class ScreenModeButton(TextButton):
    def __init__(self, menu, x, y, texts, font_size, screen_mode, next_state):
        super().__init__(x, y, texts, CALIBRI_BOLD, font_size,
                         200, menu.game.sound_player,
                         action=self.set_new_screen_mode, w=H(400))
        self.menu = menu
        self.game = menu.game
        self.screen_mode = screen_mode
        self.set_text(texts[self.game.language])
        self.next_state = next_state

    def set_new_screen_mode(self):
        update_config_file(screen_mode=self.screen_mode)
        self.game.set_screen_mode(self.screen_mode)
        self.game.main_menu.to_screen_modes_button.set_value(self.texts)
        self.game.pause_menu.to_screen_modes_button.set_value(self.texts)
        self.menu.set_state(self.next_state, self)


__all__ = ["ScreenModeButton"]
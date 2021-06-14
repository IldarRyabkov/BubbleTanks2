from gui.buttons.text_button import TextButton
from data.constants import *
from data.states import MainMenuStates as St
from data.languages.texts import TEXTS
from data.scripts import update_config_file
from assets.paths import CALIBRI_BOLD
from components.utils import *


class LanguageButton(TextButton):
    def __init__(self, menu, y, texts):
        super().__init__(SCR_W2, y, texts, CALIBRI_BOLD, H(66),
                         200, menu.game.sound_player,
                         action=self.set_new_language, w=H(300))
        self.menu = menu
        self.set_text(texts)

    def set_new_language(self):
        update_config_file(language=self.texts)
        new_language = TEXTS["language"].index(self.texts)
        self.menu.game.language = new_language
        self.menu.set_language(new_language)
        self.menu.to_languages_button.set_value(self.texts)
        self.menu.set_state(St.SETTINGS, self)


__all__ = ["LanguageButton"]

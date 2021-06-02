from gui.text_button import TextButton
from constants import *
from data.paths import CALIBRI_BOLD
from data.scripts import save_language
from utils import *
from states import MainMenuStates as St
from languages.texts import TEXTS


class LanguageButton(TextButton):
    def __init__(self, menu, y, texts):
        super().__init__(SCR_W2, y, texts, CALIBRI_BOLD, H(66),
                         200, menu.game.sound_player,
                         action=self.set_new_language, w=H(300))
        self.menu = menu
        self.set_text(texts)

    def set_new_language(self):
        save_language(self.texts)
        new_language = TEXTS["language"].index(self.texts)
        self.menu.game.language = new_language
        self.menu.set_language(new_language)
        self.menu.to_languages_button.set_value(self.texts)
        self.menu.set_state(St.SETTINGS, self)


__all__ = ["LanguageButton"]

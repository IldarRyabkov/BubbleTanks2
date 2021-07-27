from gui.buttons.text_button import TextButton
from data.constants import *
from data.languages import TEXTS
from data.scripts import update_config_file
from components.utils import *


class LanguageButton(TextButton):
    def __init__(self, menu, x, y, font, font_size, min_alpha, texts, set_new_language):
        super().__init__(x, y, texts, font, font_size,
                         min_alpha, menu.game.sound_player,
                         action=lambda: set_new_language(self), w=H(300))
        self.menu = menu
        self.game = menu.game
        self.set_text(texts)

    def set_new_language(self):
        update_config_file(language=self.texts)
        new_language = TEXTS["language"].index(self.texts)
        self.game.language = new_language
        self.game.set_language(new_language)
        self.game.pause_menu.to_languages_button.set_value(self.texts)
        self.game.main_menu.to_languages_button.set_value(self.texts)


__all__ = ["LanguageButton"]

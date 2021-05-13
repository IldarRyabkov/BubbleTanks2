from pygame.constants import MOUSEBUTTONDOWN
import pygame as pg
import sys

from data.colors import WHITE
from data.gui_texts import *
from data.paths import FONT_1, CALIBRI_BOLD
from gui.text_button import TextButton
from gui.slider import Slider
from gui.text import Text
from utils import H, HF


class OptionsWindow:
    """Pause menu window, in which the player can change the volume
    of music and sound, as well as end the game and return to the start menu.
    """
    def __init__(self, xo, sound_player):
        self.sound_player = sound_player
        self.music_slider = Slider(xo + H(587), H(400), MUSIC_VOLUME_TEXT, CALIBRI_BOLD, H(44), sound_player)
        self.sound_slider = Slider(xo + H(587), H(500), SOUND_VOLUME_TEXT, CALIBRI_BOLD, H(44), sound_player)
        self.caption = Text(xo + HF(587), HF(200), CALIBRI_BOLD, H(56), WHITE, 1)
        self.to_menu_button = TextButton(xo + H(584), H(610), EXIT_TO_MENU_TEXT, CALIBRI_BOLD, H(44), 210, sound_player)
        self.to_desktop_button = TextButton(xo + H(584), H(710), EXIT_TO_DESKTOP_TEXT, CALIBRI_BOLD, H(44), 210, sound_player)

    def set_language(self, language):
        """Sets the language for quit-button and labels. """
        self.caption.set_text(OPTIONS_WINDOW_CAPTION[language])
        self.to_menu_button.set_language(language)
        self.to_desktop_button.set_language(language)
        self.sound_slider.set_language(language)
        self.music_slider.set_language(language)

    def reset(self):
        self.sound_slider.reset(self.sound_player.master_volume)
        self.music_slider.reset(self.sound_player.master_volume)
        self.to_menu_button.reset()
        self.to_desktop_button.reset()

    def handle_mouse_click(self):
        if self.to_menu_button.clicked:
            return True
        if self.to_desktop_button.clicked:
            pg.quit()
            sys.exit()

    def handle(self, e_type) -> bool:
        """Handles mouse click. Returns True if one of exit buttons was pressed. """
        self.sound_slider.handle(e_type)
        self.music_slider.handle(e_type)
        if e_type == MOUSEBUTTONDOWN:
            if self.to_menu_button.clicked:
                return True
            if self.to_desktop_button.clicked:
                pg.quit()
                sys.exit()
        return False

    def update(self, dt):
        self.sound_slider.update(dt)
        self.music_slider.update(dt)
        self.to_menu_button.update(dt)
        self.to_desktop_button.update(dt)

        if self.sound_slider.pressed:
            self.sound_player.set_sound_volume(self.sound_slider.value)
        elif self.music_slider.pressed:
            self.sound_player.set_music_volume(self.music_slider.value)

    def draw(self, screen):
        self.caption.draw(screen)
        self.to_menu_button.draw(screen)
        self.to_desktop_button.draw(screen)
        self.sound_slider.draw(screen)
        self.music_slider.draw(screen)


__all__ = ["OptionsWindow"]

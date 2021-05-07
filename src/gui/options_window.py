import pygame as pg

from data.colors import WHITE
from data.gui_texts import OPTIONS_WINDOW_TEXTS as TEXTS
from data.paths import CALIBRI_BOLD
from gui.long_button import LongButton
from gui.slider import Slider
from gui.text import Text
from utils import WF, H, HF


class OptionsWindow:
    """Pause menu window, in which the player can change the volume
    of music and sound, as well as end the game and return to the start menu.
    """
    def __init__(self, xo, sounds):
        self.sound_slider = Slider(xo + H(400), H(600))
        self.music_slider = Slider(xo + H(400), H(400))
        self.sounds = sounds
        self.labels = (
            Text(WF(560), HF(176), CALIBRI_BOLD, H(56), WHITE),
            Text(xo + HF(180), HF(375), CALIBRI_BOLD, H(56), WHITE),
            Text(xo + HF(180), HF(575), CALIBRI_BOLD, H(56), WHITE),
        )
        self.quit_button = LongButton(xo + H(880), H(832))

    def set_language(self, language):
        """Sets the language for quit-button and labels. """
        self.quit_button.set_text(TEXTS['quit_button'][language])
        for i, label in enumerate(self.labels):
            label.set_text(TEXTS['labels'][language][i])

    def handle(self, e_type) -> bool:
        """Handles mouse click. Returns whether a quit button
         has not been pressed. """
        self.sound_slider.handle(e_type)
        self.music_slider.handle(e_type)
        return not (e_type == pg.MOUSEBUTTONDOWN and self.quit_button.cursor_on_button)

    def update_mixer(self):
        """Updates the volume of sounds and music. """
        if self.sound_slider.clicked:
            for sound in self.sounds.values():
                sound.set_volume(self.sound_slider.value)
        if self.music_slider.clicked:
            pg.mixer.music.set_volume(self.music_slider.value)

    def update(self, dt):
        self.sound_slider.update()
        self.music_slider.update()
        self.update_mixer()

    def draw(self, screen):
        for label in self.labels:
            label.draw(screen)
        self.quit_button.draw(screen)
        self.sound_slider.draw(screen)
        self.music_slider.draw(screen)


__all__ = ["OptionsWindow"]

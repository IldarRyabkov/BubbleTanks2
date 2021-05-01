import pygame as pg

from data.colors import WHITE
from gui.long_button import LongButton
from gui.slider import Slider
import data.languages.english as eng
import data.languages.russian as rus


TEXTS = {
    'quit_button':
        {
            'English': eng.OPTIONSWINDOW_QUIT_BUTTON,
            'Russian': rus.OPTIONSWINDOW_QUIT_BUTTON
        },
    'labels':
        {
            'Russian': (
                rus.OPTIONSWINDOW_CAPTION,
                rus.OPTIONSWINDOW_LABEL_MUSIC,
                rus.OPTIONSWINDOW_LABEL_SOUND
            ),
            'English': (
                eng.OPTIONSWINDOW_CAPTION,
                eng.OPTIONSWINDOW_LABEL_MUSIC,
                eng.OPTIONSWINDOW_LABEL_SOUND
            )
        }
}


class OptionsWindow:
    def __init__(self, sounds):
        self.sound_slider = Slider(500, 600)
        self.music_slider = Slider(500, 400)
        self.sounds = sounds
        self.caption = None
        self.label_music = None
        self.label_sound = None
        self.quit_button = None
        self.set_language("English")

    def set_language(self, language):
        self.set_labels(*TEXTS['labels'][language])
        self.quit_button = LongButton(944, 832, False, TEXTS['quit_button'][language])

    def set_labels(self, caption, label_1, label_2):
        pg.font.init()
        font = pg.font.SysFont('Calibri', 56, True)
        self.caption = font.render(caption, True, WHITE)
        self.label_music = font.render(label_1, True, WHITE)
        self.label_sound = font.render(label_2, True, WHITE)

    def handle(self, e_type) -> bool:
        game_running = True
        self.sound_slider.handle(e_type)
        self.music_slider.handle(e_type)
        self.update_mixer()
        if self.quit_button.cursor_on_button():
            game_running = False
        return game_running

    def update_mixer(self):
        if self.sound_slider.clicked:
            for sound in self.sounds.values():
                sound.set_volume(self.sound_slider.value)
        if self.music_slider.clicked:
            pg.mixer.music.set_volume(self.music_slider.value)

    def update(self, dt):
        self.quit_button.update_color()
        self.sound_slider.update()
        self.music_slider.update()
        self.update_mixer()

    def draw(self, screen):
        screen.blit(self.caption, (560, 176))
        screen.blit(self.label_music, (240, 375))
        screen.blit(self.label_sound, (240, 575))

        self.quit_button.draw(screen)
        self.sound_slider.draw(screen)
        self.music_slider.draw(screen)
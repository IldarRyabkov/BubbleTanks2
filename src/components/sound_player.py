import pygame as pg
from assets.paths import *


sounds = (COLLECT_BUBBLE, ENEMY_DEATH, ENEMY_HIT, SHOOT,
          PLAYER_HIT, BUTTON_CLICK, WATER_SPLASH)


class SoundPlayer:
    """Manages game sounds and music. """
    def __init__(self):
        self.sounds = {sound: pg.mixer.Sound(sound) for sound in sounds}
        self.locked = {sound: False for sound in sounds}
        self.music_volume = 0.9
        self.sound_volume = 0.58
        self.set_music_volume(self.music_volume)
        self.set_sound_volume(self.sound_volume)

    def reset(self):
        for sound in self.locked:
            self.locked[sound] = False

    def play_sound(self, sound):
        if not self.locked[sound] and self.sounds[sound].get_num_channels() < 5:
            self.sounds[sound].play()
            self.locked[sound] = True

    def set_sound_volume(self, volume):
        for sound in self.sounds:
            self.sounds[sound].set_volume(volume)
        self.sound_volume = volume

    def set_music_volume(self, volume):
        pg.mixer.music.set_volume(volume)
        self.music_volume = volume

    @staticmethod
    def play_music(music):
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1, 0.0, fade_ms=2000)

    @staticmethod
    def fade_out(time):
        pg.mixer.music.fadeout(time)


__all__ = ["SoundPlayer"]

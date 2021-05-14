from pygame import mixer
from data.paths import *


sounds = (BUBBLE_DEATH, MOB_DEATH, PLAYER_BULLET_HIT, PLAYER_BULLET_SHOT,
          PLAYER_INJURE, THUNDER, UI_CHOOSE, UI_CLICK, WATER_SPLASH)


class SoundPlayer:
    """Manages game sounds and music. """
    def __init__(self):
        mixer.pre_init(44100, -32, 8, 4096)
        self.sounds = {sound: mixer.Sound(sound) for sound in sounds}
        self.sound_on = True
        self.music_on = True
        self.sound_lock = False
        self.master_volume = 0.3
        self.set_music_volume(self.master_volume)
        self.set_sound_volume(self.master_volume)

    def reset(self):
        self.sound_lock = False

    def play_sound(self, sound):
        if self.sound_on and not self.sound_lock:
            self.sounds[sound].play()
            self.sound_lock = True

    def set_sound_volume(self, value):
        for sound in self.sounds:
            self.sounds[sound].set_volume(value)

    def set_music_volume(self, volume):
        mixer.music.set_volume(volume)
        self.master_volume = volume

    @staticmethod
    def play_music(music):
        mixer.music.load(music)
        mixer.music.play(-1, 0.0)

    def update_data(self, music_on, sound_on):
        if self.music_on and not music_on:
            self.music_on = False
            mixer.music.pause()
        elif not self.music_on and music_on:
            self.music_on = True
            mixer.music.unpause()
        self.sound_on = sound_on


__all__ = ["SoundPlayer"]

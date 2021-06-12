from pygame import mixer
from assets.paths import *


sounds = (COLLECT_BUBBLE, ENEMY_DEATH, HIT, SHOOT,
          AVATAR_HIT, BUTTON_CLICK, WATER_SPLASH)


class SoundPlayer:
    """Manages game sounds and music. """
    def __init__(self):
        mixer.pre_init(44100, -32, 8, 4096)
        self.sounds = {sound: mixer.Sound(sound) for sound in sounds}
        self._sound_lock = False
        self.music_volume = 0.8
        self.sound_volume = 0.8
        self.set_music_volume(self.music_volume)
        self.set_sound_volume(self.sound_volume)

    def unlock(self):
        self._sound_lock = False

    def play_sound(self, sound, ignore_lock=True):
        if ignore_lock or not self._sound_lock:
            self.sounds[sound].play()
            self._sound_lock = True

    def set_sound_volume(self, volume):
        for sound in self.sounds:
            self.sounds[sound].set_volume(volume)
        self.sound_volume = volume

    def set_music_volume(self, volume):
        mixer.music.set_volume(volume)
        self.music_volume = volume

    @staticmethod
    def play_music(music):
        mixer.music.load(music)
        mixer.music.play(-1, 0.0, fade_ms=2000)

    @staticmethod
    def fade_out(time):
        mixer.music.fadeout(time)


__all__ = ["SoundPlayer"]

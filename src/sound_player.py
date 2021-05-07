from pygame import mixer
from data.paths import *


sounds = (BUBBLE_DEATH, MOB_DEATH, PLAYER_BULLET_HIT,
          PLAYER_BULLET_SHOT, PLAYER_INJURE, THUNDER)


class SoundPlayer:
    """Manages game sounds and music. """
    def __init__(self):
        mixer.pre_init(44100, -32, 8, 4096)
        self.sounds = {sound: mixer.Sound(sound) for sound in sounds}
        self.sound_on = True
        self.music_on = True
        self.sound_was_played = False

    def reset(self):
        self.sound_was_played = False

    def play_sound(self, sound):
        if self.sound_on and not self.sound_was_played:
            self.sounds[sound].play()
            self.sound_was_played = True

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

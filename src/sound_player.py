import pygame as pg
from data.paths import *


sounds = (BUBBLE_DEATH, MOB_DEATH, PLAYER_BULLET_HIT,
          PLAYER_BULLET_SHOT, PLAYER_INJURE)


class SoundPlayer:
    def __init__(self):
        pg.mixer.pre_init(44100, 16, 2, 1024)
        self.sounds = {sound: pg.mixer.Sound(sound) for sound in sounds}
        self.sound_on = True
        self.music_on = True
        self.sound_was_played = False

    def reset(self):
        self.sound_was_played = False

    def play_sound(self, sound):
        if self.sound_on and not self.sound_was_played:
            self.sounds[sound].play()
            self.sound_was_played = True

    def play_music(self, music):
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1, 0.0)
        if not self.music_on:
            pg.mixer.music.pause()

    def update_data(self, music_on, sound_on):
        if self.music_on and not music_on:
            self.music_on = False
            pg.mixer.music.pause()
        elif not self.music_on and music_on:
            self.music_on = True
            pg.mixer.music.unpause()

        self.sound_on = sound_on

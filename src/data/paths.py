"""
Module contains paths to all files used in the game.

"""


import os
import sys


def path(directory: str, filename: str):
    return os.path.abspath(os.path.join(ROOT_DIR, "%s/%s" % (directory, filename)))


def img_path(filename: str): return path("images", filename)
def font_path(filename: str): return path("fonts", filename)
def music_path(filename: str): return path("music", filename)
def sound_path(filename: str): return path("sounds", filename)


ROOT_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


# images
BG = img_path("bg.png")
ROOM_BG = img_path("room_bg.png")
START_MENU_CAPTION_BG = img_path("start_menu_caption.png")
UPGRADE_CAPTION_RUS = img_path("upgrade_caption_rus.png")
UPGRADE_CAPTION_ENG = img_path("upgrade_caption_eng.png")
UPGRADE_BUTTON_PRESSED = img_path("upgrade_button_pressed.png")
UPGRADE_BUTTON_WIDE_PRESSED = img_path("upgrade_button_wide_pressed.png")
UPGRADE_BUTTON = img_path("upgrade_button.png")
UPGRADE_BUTTON_WIDE = img_path("upgrade_button_wide.png")
SIDE_BUTTON = img_path("side_button.png")
SIDE_BUTTON_PRESSED = img_path("side_button_pressed.png")
EXIT_BUTTON = img_path("exit_button.png")
EXIT_BUTTON_PRESSED = img_path("exit_button_pressed.png")
ROOM_GLARE = img_path("room_glare.png")
ROOM_AIM = img_path("room_aim.png")
BOSS_AIM = img_path("boss_aim.png")
PARALYZING_EXPLOSION = img_path("paralyzing_explosion.png")
POWERFUL_EXPLOSION = img_path("powerful_explosion.png")
TELEPORTATION = img_path("teleportation.png")
HEALTH_WINDOW_BG = img_path("health_window_bg.png")
COOLDOWN_WINDOW_BG = img_path("cooldown_window_bg.png")
BUBBLE_HALO = img_path("bubble_halo.png")
RUS_FLAG = img_path("russian_flag.png")
ENG_FLAG = img_path("english_flag.png")
PLAY_BUTTON = img_path("play_button.png")

# fonts
FONT_1 = font_path('font_1.otf')
FONT_2 = font_path('font_2.ttf')
CALIBRI = font_path('calibri.ttf')
CALIBRI_BOLD = font_path('calibri_bold.ttf')

# music
GAME_MUSIC = music_path('game_music.wav')
START_MUSIC = music_path('start_music.wav')


# sounds
BUBBLE_DEATH = sound_path('bubble_death.wav')
MOB_DEATH = sound_path('mob_death.wav')
PLAYER_BULLET_HIT = sound_path('player_bullet_hit.wav')
PLAYER_BULLET_SHOT = sound_path('player_bullet_shot.wav')
PLAYER_INJURE = sound_path('player_injure.wav')
THUNDER = sound_path('thunder.wav')


__all__ = [

    "ROOT_DIR",
    "BG",
    "ROOM_BG",
    "START_MENU_CAPTION_BG",
    "UPGRADE_CAPTION_RUS",
    "UPGRADE_CAPTION_ENG",
    "UPGRADE_BUTTON_PRESSED",
    "UPGRADE_BUTTON_WIDE_PRESSED",
    "UPGRADE_BUTTON",
    "UPGRADE_BUTTON_WIDE",
    "SIDE_BUTTON",
    "SIDE_BUTTON_PRESSED",
    "EXIT_BUTTON",
    "EXIT_BUTTON_PRESSED",
    "ROOM_GLARE",
    "ROOM_AIM",
    "BOSS_AIM",
    "PARALYZING_EXPLOSION",
    "POWERFUL_EXPLOSION",
    "TELEPORTATION",
    "HEALTH_WINDOW_BG",
    "COOLDOWN_WINDOW_BG",
    "BUBBLE_HALO",
    "RUS_FLAG",
    "ENG_FLAG",
    "FONT_1",
    "FONT_2",
    "CALIBRI",
    "CALIBRI_BOLD",
    "GAME_MUSIC",
    "START_MUSIC",
    "BUBBLE_DEATH",
    "MOB_DEATH",
    "PLAYER_INJURE",
    "PLAYER_BULLET_HIT",
    "PLAYER_BULLET_SHOT",
    "THUNDER"

]

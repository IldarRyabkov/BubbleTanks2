"""
Module contains paths to all files used in the game.

"""


import os
import sys


def path(directory: str, filename: str):
    if directory:
        return os.path.abspath(os.path.join(ROOT_DIR, "%s/%s" % (directory, filename)))
    return os.path.abspath(os.path.join(ROOT_DIR, "%s" % filename))


user_dir = os.path.join(os.path.abspath(os.path.expanduser("~")), f".Underwater_Battles")
if not os.path.exists(user_dir):
    os.mkdir(user_dir)

RESOLUTIONS = os.path.join(user_dir, 'resolution.json')


def img_path(filename: str): return path("images", filename)
def font_path(filename: str): return path("fonts", filename)
def music_path(filename: str): return path("music", filename)
def sound_path(filename: str): return path("sounds", filename)


ROOT_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

# images
BG = img_path("bg.png")
ROOM_BG = img_path("room_bg.png")
START_MENU_CAPTION_BG = img_path("start_menu_caption.png")
UPGRADE_CAPTION_RUS_BG = img_path("upgrade_caption_rus.png")
UPGRADE_CAPTION_ENG_BG = img_path("upgrade_caption_eng.png")
UPGRADE_BUTTON_PRESSED_BG = img_path("upgrade_button_pressed.png")
UPGRADE_BUTTON_WIDE_PRESSED_BG = img_path("upgrade_button_wide_pressed.png")
UPGRADE_BUTTON_BG = img_path("upgrade_button.png")
UPGRADE_BUTTON_WIDE_BG = img_path("upgrade_button_wide.png")
SIDE_BUTTON_BG = img_path("side_button.png")
SIDE_BUTTON_PRESSED_BG = img_path("side_button_pressed.png")
ROOM_GLARE_BG = img_path("room_glare.png")
ROOM_AIM = img_path("room_aim.png")
BOSS_AIM = img_path("boss_aim.png")
PARALYZING_EXPLOSION = img_path("paralyzing_explosion.png")
POWERFUL_EXPLOSION = img_path("powerful_explosion.png")
TELEPORTATION = img_path("teleportation.png")
HEALTH_WINDOW_BG = img_path("health_window_bg.png")
COOLDOWN_WINDOW_BG = img_path("cooldown_window_bg.png")
BUBBLE_HALO = img_path("bubble_halo.png")
PLAY_BUTTON_BG = img_path("play_button.png")
SETTINGS_BUTTON_BG = img_path("settings_button.png")
INFO_BUTTON_BG = img_path("info_button.png")
SCROLL_BUTTON_BG = img_path("scroll_button.png")

# fonts
FONT_1 = font_path('font_1.otf')
FONT_2 = font_path('font_2.ttf')
FONT_3 = font_path('font_3.ttf')
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
UI_CHOOSE = sound_path('ui_choose.wav')
UI_CLICK = sound_path('ui_click.wav')
WATER_SPLASH = sound_path('water_splash.wav')


__all__ = [

    "ROOT_DIR",
    "BG",
    "ROOM_BG",
    "START_MENU_CAPTION_BG",
    "UPGRADE_CAPTION_RUS_BG",
    "UPGRADE_CAPTION_ENG_BG",
    "UPGRADE_BUTTON_PRESSED_BG",
    "UPGRADE_BUTTON_WIDE_PRESSED_BG",
    "UPGRADE_BUTTON_BG",
    "UPGRADE_BUTTON_WIDE_BG",
    "SIDE_BUTTON_BG",
    "SIDE_BUTTON_PRESSED_BG",
    "ROOM_GLARE_BG",
    "ROOM_AIM",
    "BOSS_AIM",
    "PARALYZING_EXPLOSION",
    "POWERFUL_EXPLOSION",
    "TELEPORTATION",
    "HEALTH_WINDOW_BG",
    "COOLDOWN_WINDOW_BG",
    "BUBBLE_HALO",
    "FONT_1",
    "FONT_2",
    "FONT_3",
    "CALIBRI",
    "CALIBRI_BOLD",
    "GAME_MUSIC",
    "START_MUSIC",
    "BUBBLE_DEATH",
    "MOB_DEATH",
    "PLAYER_INJURE",
    "PLAYER_BULLET_HIT",
    "PLAYER_BULLET_SHOT",
    "THUNDER",
    "UI_CHOOSE",
    "UI_CLICK",
    "WATER_SPLASH",
    "SETTINGS_BUTTON_BG",
    "INFO_BUTTON_BG",
    "PLAY_BUTTON_BG",
    "SCROLL_BUTTON_BG",
    "RESOLUTIONS"

]

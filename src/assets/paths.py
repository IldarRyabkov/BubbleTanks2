"""
Module contains paths to all files used in the game.

"""

import os


def path(directory: str, filename: str):
    if directory:
        file_path = os.path.join(directory, filename)
        return os.path.abspath(os.path.join(ROOT_DIR, "%s" % file_path))
    return os.path.abspath(os.path.join(ROOT_DIR, "%s" % filename))


def img_path(filename: str):
    return path("images", filename)


def font_path(filename: str):
    return path("fonts", filename)


def music_path(filename: str):
    return path("music", filename)


def sound_path(filename: str):
    return path("sounds", filename)


def language_path(filename: str):
    return path("sounds", filename)


def sapper_attack_img_path(filename: str):
    return img_path(os.path.join("sapper_attack", filename))


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


# images
BG = img_path("bg.png")
ROOM_BG = img_path("room_bg.png")
MAIN_MENU_CAPTION_BG = img_path("main_menu_caption.png")
UPGRADE_CAPTION = img_path("upgrade_menu_caption.png")
UPGRADE_BUTTON_PRESSED_BG = img_path("upgrade_button_pressed.png")
UPGRADE_BUTTON_WIDE_PRESSED_BG = img_path("upgrade_button_wide_pressed.png")
UPGRADE_BUTTON_BG = img_path("upgrade_button.png")
UPGRADE_BUTTON_WIDE_BG = img_path("upgrade_button_wide.png")
SIDE_BUTTON_BG = img_path("side_button.png")
ROOM_GLARE_BG = img_path("room_glare.png")
ROOM_AIM = img_path("room_aim.png")
BOSS_AIM = img_path("boss_aim.png")
STUN_BURST_IMAGE = img_path("stun_burst.png")
DAMAGE_BURST_IMAGE = img_path("damage_burst.png")
DAMAGE_BURST_BG_IMAGE = img_path("damage_burst_bg.png")
DRONE_CONVERSION = img_path("drone_conversion.png")
TELEPORTATION = img_path("teleportation.png")
HEALTH_WINDOW_BG = img_path("health_window_bg.png")
COOLDOWN_WINDOW_BG = img_path("cooldown_window_bg.png")
BUBBLE_HALO = img_path("bubble_halo.png")
PLAY_BUTTON_BG = img_path("play_button.png")
SETTINGS_BUTTON_BG = img_path("settings_button.png")
CREDITS_BUTTON_BG = img_path("info_button.png")
SCROLL_BUTTON_BG = img_path("scroll_button.png")
EXIT_BUTTON_BG = img_path("exit_button.png")
EXIT_BUTTON_PRESSED_BG = img_path("exit_button_pressed.png")
CREDITS_BG_1 = img_path("credits_bg_1.png")
CREDITS_BG_2 = img_path("credits_bg_2.png")
CREDITS_BG_3 = img_path("credits_bg_3.png")
CONTROLS_BG = img_path("controls_bg.png")
SAVE_BUTTON_BG = img_path("save_button_bg.png")
DELETE_BUTTON_BG = img_path("delete_button.png")
STICKY_IMAGE = img_path("sticky.png")
START_BUTTON_IMAGE = img_path("play_button.png")
SAPPER_IMG_1 = sapper_attack_img_path("1.png")
SAPPER_IMG_2 = sapper_attack_img_path("2.png")
SAPPER_IMG_3 = sapper_attack_img_path("3.png")
SAPPER_IMG_4 = sapper_attack_img_path("4.png")
SAPPER_IMG_5 = sapper_attack_img_path("5.png")
SAPPER_IMG_6 = sapper_attack_img_path("6.png")
SAPPER_IMG_7 = sapper_attack_img_path("7.png")
SAPPER_IMG_8 = sapper_attack_img_path("8.png")


# fonts
FONT_1 = font_path('font_1.otf')
CALIBRI = font_path('calibri.ttf')
CALIBRI_BOLD = font_path('calibri_bold.ttf')


# music
GAME_MUSIC = music_path('game.wav')
TITLE_MUSIC = music_path('title.wav')


# sounds
COLLECT_BUBBLE = sound_path('collect.wav')
ENEMY_DEATH = sound_path('enemy_death.wav')
ENEMY_HIT = sound_path('hit.wav')
SHOOT = sound_path('shoot.wav')
PLAYER_HIT = sound_path('avatar_hit.wav')
BUTTON_CLICK = sound_path('button_click.wav')
WATER_SPLASH = sound_path('water_splash.wav')


__all__ = [

    "ROOT_DIR",
    "BG",
    "ROOM_BG",
    "MAIN_MENU_CAPTION_BG",
    "UPGRADE_CAPTION",
    "UPGRADE_BUTTON_PRESSED_BG",
    "UPGRADE_BUTTON_WIDE_PRESSED_BG",
    "UPGRADE_BUTTON_BG",
    "UPGRADE_BUTTON_WIDE_BG",
    "SIDE_BUTTON_BG",
    "ROOM_GLARE_BG",
    "ROOM_AIM",
    "BOSS_AIM",
    "STUN_BURST_IMAGE",
    "DAMAGE_BURST_IMAGE",
    "DAMAGE_BURST_BG_IMAGE",
    "DRONE_CONVERSION",
    "TELEPORTATION",
    "HEALTH_WINDOW_BG",
    "COOLDOWN_WINDOW_BG",
    "BUBBLE_HALO",
    "CREDITS_BG_1",
    "CREDITS_BG_2",
    "CREDITS_BG_3",
    "CONTROLS_BG",
    "DELETE_BUTTON_BG",
    "SAVE_BUTTON_BG",
    "SETTINGS_BUTTON_BG",
    "CREDITS_BUTTON_BG",
    "PLAY_BUTTON_BG",
    "SCROLL_BUTTON_BG",
    "EXIT_BUTTON_BG",
    "EXIT_BUTTON_PRESSED_BG",
    "STICKY_IMAGE",
    "START_BUTTON_IMAGE",
    "SAPPER_IMG_1",
    "SAPPER_IMG_2",
    "SAPPER_IMG_3",
    "SAPPER_IMG_4",
    "SAPPER_IMG_5",
    "SAPPER_IMG_6",
    "SAPPER_IMG_7",
    "SAPPER_IMG_8",
    "FONT_1",
    "CALIBRI",
    "CALIBRI_BOLD",
    "GAME_MUSIC",
    "TITLE_MUSIC",
    "COLLECT_BUBBLE",
    "ENEMY_DEATH",
    "PLAYER_HIT",
    "ENEMY_HIT",
    "SHOOT",
    "BUTTON_CLICK",
    "WATER_SPLASH"

]

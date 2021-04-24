import os
import sys

ROOT_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

# images
BG = os.path.abspath(os.path.join(ROOT_DIR, "images/bg.png"))
ROOM_BG = os.path.abspath(os.path.join(ROOT_DIR, "images/room_bg.png"))
START_MENU_CAPTION_BG = os.path.abspath(os.path.join(ROOT_DIR, "images/start_menu_caption.png"))
UPGRADE_CAPTION_RUS = os.path.abspath(os.path.join(ROOT_DIR, "images/upgrade_caption_rus.png"))
UPGRADE_BUTTON = os.path.abspath(os.path.join(ROOT_DIR, "images/upgrade_button.png"))
UPGRADE_BUTTON_WIDE = os.path.abspath(os.path.join(ROOT_DIR, "images/upgrade_button_wide.png"))
UPGRADE_BUTTON_TRANSPARENT = os.path.abspath(os.path.join(ROOT_DIR, "images/upgrade_button_transparent.png"))
UPGRADE_BUTTON_WIDE_TRANSPARENT = os.path.abspath(os.path.join(ROOT_DIR, "images/upgrade_button_wide_transparent.png"))
UPGRADE_CAPTION_ENG = os.path.abspath(os.path.join(ROOT_DIR, "images/upgrade_caption_eng.png"))
SIDE_BUTTON = os.path.abspath(os.path.join(ROOT_DIR, "images/side_button.png"))
SIDE_BUTTON_CLICKED = os.path.abspath(os.path.join(ROOT_DIR, "images/side_button_clicked.png"))
PAUSE_MENU_MASK = os.path.abspath(os.path.join(ROOT_DIR, "images/pause_menu.png"))
ROOM_GLARE = os.path.abspath(os.path.join(ROOT_DIR, "images/room_glare.png"))
PARALYZING_EXPLOSION = os.path.abspath(os.path.join(ROOT_DIR, "images/paralyzing_explosion.png"))
POWERFUL_EXPLOSION = os.path.abspath(os.path.join(ROOT_DIR, "images/powerful_explosion.png"))
TELEPORTATION = os.path.abspath(os.path.join(ROOT_DIR, "images/teleportation.png"))
HEALTH_WINDOW_BG = os.path.abspath(os.path.join(ROOT_DIR, "images/health_window_bg.png"))
COOLDOWN_WINDOW_BG = os.path.abspath(os.path.join(ROOT_DIR, "images/cooldown_window_bg.png"))
BUBBLE_HALO = os.path.abspath(os.path.join(ROOT_DIR, "images/bubble_halo.png"))
RUS_FLAG = os.path.abspath(os.path.join(ROOT_DIR, "images/russian_flag.png"))
ENG_FLAG = os.path.abspath(os.path.join(ROOT_DIR, "images/english_flag.png"))

# fonts
FONT_1 = os.path.abspath(os.path.join(ROOT_DIR, 'fonts/font_1.otf'))
FONT_2 = os.path.abspath(os.path.join(ROOT_DIR, 'fonts/font_2.ttf'))

# music
GAME_MUSIC = os.path.abspath(os.path.join(ROOT_DIR, 'music/game_music.wav'))
START_MUSIC = os.path.abspath(os.path.join(ROOT_DIR, 'music/start_music.wav'))


# sounds
BUBBLE_DEATH = os.path.abspath(os.path.join(ROOT_DIR, 'sounds/bubble_death.wav'))
MOB_DEATH = os.path.abspath(os.path.join(ROOT_DIR, 'sounds/mob_death.wav'))
PLAYER_BULLET_HIT = os.path.abspath(os.path.join(ROOT_DIR, 'sounds/player_bullet_hit.wav'))
PLAYER_BULLET_SHOT = os.path.abspath(os.path.join(ROOT_DIR, 'sounds/player_bullet_shot.wav'))
PLAYER_INJURE = os.path.abspath(os.path.join(ROOT_DIR, 'sounds/player_injure.wav'))

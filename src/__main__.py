import pygame as pg
import os
import platform
from data.constants import SCR_SIZE


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.mixer.pre_init(44100, -16, 2, 512)
    pg.init()
    pg.mixer.set_num_channels(26)
    pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
    pg.event.set_blocked(None)
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP])

    # Make sure the game will display correctly on high DPI monitors on Windows.
    if platform.system() == 'Windows':
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(2)

    screen = pg.display.set_mode(SCR_SIZE, flags=0)

    from components.game import Game
    Game(screen).run()


if __name__ == "__main__":
    main()

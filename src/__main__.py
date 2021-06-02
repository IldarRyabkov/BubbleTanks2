import pygame as pg
import platform
from constants import SCR_SIZE


def main():
    pg.init()
    pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
    pg.event.set_blocked(None)
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP])

    # Make sure the game will display correctly on high DPI monitors on Windows.
    if platform.system() == 'Windows':
        from ctypes import windll
        try:
            windll.user32.SetProcessDPIAware()
        except AttributeError:
            pass

    screen = pg.display.set_mode(SCR_SIZE, flags=pg.NOFRAME)

    from game import Game
    Game(screen).run()


if __name__ == "__main__":
    main()

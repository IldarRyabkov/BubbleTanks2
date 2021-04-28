import pygame as pg
import ctypes
import platform


from game import Game
from data.cursor import CURSOR


def main():
    # Initialize all imported pygame modules
    pg.init()

    # Set the game cursor
    cursor = pg.cursors.compile(CURSOR, black='.', white='X')
    pg.mouse.set_cursor((32, 32), (0, 0), *cursor)

    # Set the event types allowed to appear on the event queue
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP,
                          pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP])

    # Make sure the game will display correctly on high DPI monitors on Windows
    if platform.system() == 'Windows':
        ctypes.windll.user32.SetProcessDPIAware()

    # Run the game
    Game().run()


if __name__ == "__main__":
    main()

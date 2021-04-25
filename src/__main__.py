import pygame as pg
import ctypes

from game import Game
from data.config import SCR_SIZE
from data.cursor import CURSOR


def main():
    pg.init()
    cursor = pg.cursors.compile(CURSOR, black='.', white='X')
    pg.mouse.set_cursor((32, 32), (0, 0), *cursor)
    pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP,
                          pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP])
    ctypes.windll.user32.SetProcessDPIAware()
    screen = pg.display.set_mode(SCR_SIZE)
    pg.display.set_caption("Underwater Battles")

    Game(screen).run()


if __name__ == "__main__":
    main()
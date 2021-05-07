import pygame as pg

from data.colors import DARK_GREY, LIGHT_GREY, WHITE
from data.paths import CALIBRI_BOLD
from gui.text import Text
from utils import H


class LongButton:
    """Button which is used in the Pause menu and
    the Victory menu to go back to the Main menu.
    """
    WIDTH = H(256)
    HEIGHT = H(64)

    def __init__(self, x: int, y: int):
        self.colors = {True: DARK_GREY, False: LIGHT_GREY}
        self.rect = pg.Rect(x, y, self.WIDTH , self.HEIGHT)
        self.text_widget = Text(self.rect.centerx, self.rect.y + H(17), CALIBRI_BOLD, H(30), WHITE, True)
        self.set_text('')

    def set_text(self, text):
        self.text_widget.set_text(text)

    @property
    def cursor_on_button(self) -> bool:
        return bool(self.rect.collidepoint(pg.mouse.get_pos()))

    def draw(self, screen):
        pg.draw.rect(screen, self.colors[self.cursor_on_button], self.rect, 0, self.HEIGHT // 2)
        self.text_widget.draw(screen)


__all__ = ["LongButton"]

import pygame as pg
from data.colors import DARK_GREY, LIGHT_GREY, WHITE

WIDTH = 256
HEIGHT = 64


def create_text_surface(text: str) -> pg.Surface:
    pg.font.init()
    font = pg.font.SysFont('Calibri', 30, True)
    surface = font.render(text, True, WHITE)
    return surface


def get_text_pos(text: pg.Surface, x: int, y: int) -> list:
    text_x = x + (WIDTH - text.get_width()) // 2
    text_y = y + (HEIGHT - text.get_height()) // 2
    return [text_x, text_y]


class LongButton:
    def __init__(self, x: int,
                 y: int,
                 clicked: bool,
                 text: str,
                 color_1=DARK_GREY,
                 color_2=LIGHT_GREY):
        self.clicked = clicked
        self.text = text
        self.colors = (color_1, color_2)
        self.color = color_1 if self.clicked else color_2
        self.rect = pg.Rect(x, y, WIDTH , HEIGHT)
        self.text_surface = create_text_surface(text)
        self.text_pos = get_text_pos(self.text_surface, x, y)

    def cursor_on_button(self) -> bool:
        return bool(self.rect.collidepoint(pg.mouse.get_pos()))

    def can_be_clicked(self):
        return self.cursor_on_button() and not self.clicked

    def update_color(self):
        if self.cursor_on_button():
            self.color = self.colors[0]
        elif not self.clicked:
            self.color = self.colors[1]

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect, 0, HEIGHT // 2)
        surface.blit(self.text_surface, self.text_pos)
import pygame as pg
import sys

from data.config import SCR_W2, SCR_H2, SCR_H, SCR_SIZE
from data.paths import FONT_1, FONT_2
from data.colors import WHITE
from objects.bubble import Bubble
from gui.long_button import LongButton
import data.languages.english as eng
import data.languages.russian as rus


def create_bubbles():
    bubbles = [Bubble(SCR_W2 - 192, SCR_H2 - 80, 0, 0, "big"),
               Bubble(SCR_W2 + 192, SCR_H2 - 80, 0, 0, "big"),
               Bubble(SCR_W2, SCR_H2 - 80, 0, 0, "big")]
    for bubble in bubbles:
        bubble.vel = 0
    return bubbles


def create_caption(text):
    pg.font.init()
    font = pg.font.Font(FONT_1, 90)
    return font.render(text, True, WHITE)


def create_text(text):
    pg.font.init()
    font = pg.font.Font(FONT_2, 48)
    return font.render(text, True, WHITE)


def create_button(text):
    x = int(SCR_W2 - 128)
    y = int(0.75 * SCR_H - 32)
    return LongButton(x, y, False, text)


class VictoryMenu:
    caption = None
    text = None
    button = None
    bubbles = None
    bg_surface = pg.Surface(SCR_SIZE)
    mask_surface = pg.Surface(SCR_SIZE)
    mask_surface.set_alpha(195)
    running = True
    clock = pg.time.Clock()

    def __init__(self):
        self.bubbles = create_bubbles()
        self.set_language("English")

    def set_language(self, language):
        if language == 'English':
            self.caption = create_caption(eng.VICTORYMENU_CAPTION)
            self.text = create_text(eng.VICTORYMENU_TEXT)
            self.button = create_button(eng.VICTORYMENU_BUTTON)
        else:
            self.caption = create_caption(rus.VICTORYMENU_CAPTION)
            self.text = create_text(rus.VICTORYMENU_TEXT)
            self.button = create_button(rus.VICTORYMENU_BUTTON)

    def handle_mouse_click(self):
        if self.button.cursor_on_button():
            self.running = False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_mouse_click()

    def update(self, dt):
        for bubble in self.bubbles:
            bubble.update_body(dt)
        self.button.update_color()

    def draw_bubbles(self, screen):
        for bubble in self.bubbles:
            bubble.draw(screen)

    def draw(self, screen):
        screen.blit(self.mask_surface, (0, 0))
        screen.blit(self.caption, (SCR_W2 - self.caption.get_width()/2, 128))
        screen.blit(self.text,    (SCR_W2 - self.text.get_width()/2, 232))
        self.button.draw(screen)
        self.draw_bubbles(screen)
        pg.display.update()

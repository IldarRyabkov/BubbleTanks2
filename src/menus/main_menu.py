import pygame as pg
import sys

from gui.play_button import PlayButton
from gui.language_button import LanguageButton
from gui.text import Text
from entities.main_menu_bubbles import Bubbles
from data.config import SCR_W2, SCR_SIZE, WAIT, OPEN, MAIN_MENU_ANIMATION_TIME as TIME
from data.colors import WHITE
from data.gui_texts import MAIN_MENU_CAPTIONS
from data.paths import BG, RUS_FLAG, ENG_FLAG, START_MENU_CAPTION_BG, FONT_1
from utils import W, H


class MainMenu:
    """Main menu of the game, where player can choose
    language and start a new game.
    """
    def __init__(self, language="English"):
        self.running = True
        self.language = language
        self.bubbles = Bubbles()
        self.play_button = PlayButton()
        self.eng_button = LanguageButton(W(64), ENG_FLAG)
        self.rus_button = LanguageButton(W(64) + H(102), RUS_FLAG)
        self.caption = Text(SCR_W2, H(432), FONT_1, H(112), WHITE, True)
        bg = pg.image.load(BG).convert()
        caption_bg = pg.image.load(START_MENU_CAPTION_BG).convert_alpha()
        self.bg = pg.transform.scale(bg, SCR_SIZE)
        self.caption_bg = pg.transform.scale(caption_bg, (H(1280), H(256)))
        self.set_language(language)

    def set_language(self, language):
        self.language = language
        self.caption.set_text(MAIN_MENU_CAPTIONS[language])
        self.play_button.set_language(language)

    def handle_events(self, animation=False):
        for event in pg.event.get():
            if (event.type == pg.QUIT or
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)):
                pg.quit()
                sys.exit()
            if (event.type == pg.MOUSEBUTTONDOWN and
                        event.button == pg.BUTTON_LEFT and not animation):
                if self.play_button.cursor_on_button:
                    self.running = False
                elif self.rus_button.cursor_on_button:
                    self.set_language("Russian")
                elif self.eng_button.cursor_on_button:
                    self.set_language("English")

    def update_caption_alpha(self, time, state):
        """Updates alpha-value of caption and its background,
        based on Main menu state.
        """
        alpha = 255 * time/TIME if state == OPEN else 255 - 255 * time / TIME
        self.caption.set_alpha(alpha)
        self.caption_bg.set_alpha(alpha)

    def update(self, dt, animation_time=0, state=WAIT):
        self.bubbles.update(dt)
        self.play_button.update(dt, animation_time, state)
        self.rus_button.update(dt, animation_time, state)
        self.eng_button.update(dt, animation_time, state)
        if state != WAIT:
            self.update_caption_alpha(animation_time, state)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        self.bubbles.draw(screen)
        screen.blit(self.caption_bg, (SCR_W2 - H(640), H(352)))
        self.caption.draw(screen)
        self.play_button.draw(screen)
        self.rus_button.draw(screen)
        self.eng_button.draw(screen)
        pg.display.update()


__all__ = ["MainMenu"]

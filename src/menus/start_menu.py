import pygame as pg
import sys

from gui.play_button import PlayButton
from gui.language_button import LanguageButton
from gui.start_menu_caption import StartMenuCaption
from objects.background_bubbles import BackgroundBubbles
from data.config import *
from data.paths import BG


clock = pg.time.Clock()


class StartMenu:
    def __init__(self):
        self.caption = StartMenuCaption()
        self.running = True
        self.bubbles = BackgroundBubbles()
        self.play_button = PlayButton()
        self.language = "English"
        self.language_changed = False
        self.rus_button = LanguageButton("Russian")
        self.eng_button = LanguageButton("English")
        self.bg = pg.transform.scale(pg.image.load(BG).convert(), SCR_SIZE)

    def set_language(self, language):
        self.language = language
        self.caption.set_language(language)
        self.play_button.set_language(language)

    def reset_data(self):
        self.play_button.reset()
        self.caption.reset()
        self.rus_button.reset()
        self.eng_button.reset()
        self.bubbles.reset()
        self.running = True
        self.language_changed = False

    def handle_events(self):
        for event in pg.event.get():
            if (event.type == pg.QUIT or
                    (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)):
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.play_button.cursor_on_button():
                    self.running = False
                elif self.rus_button.cursor_on_button() and not self.rus_button.clicked:
                    self.set_language("Russian")
                    self.rus_button.clicked = True
                    self.eng_button.clicked = False
                    self.language_changed = True
                elif self.eng_button.cursor_on_button() and not self.eng_button.clicked:
                    self.set_language("English")
                    self.eng_button.clicked = True
                    self.rus_button.clicked = False
                    self.language_changed = True

    def update(self, dt, animation_time=0, state=START_MENU_WAIT):
        self.bubbles.update(dt)
        self.play_button.update(dt, animation_time, state)
        self.rus_button.update(dt, animation_time, state)
        self.eng_button.update(dt, animation_time, state)

        if state != START_MENU_WAIT:
            self.caption.update_alpha(animation_time, state)

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        self.bubbles.draw(screen)
        self.caption.draw(screen)
        self.play_button.draw(screen)
        self.rus_button.draw(screen)
        self.eng_button.draw(screen)
        pg.display.update()

    def run_animation(self, state, screen, fps_manager):
        self.play_button.set_pos(state)

        animation_time = dt = 0
        while animation_time <= START_MENU_ANIMATION_TIME:
            self.handle_events()
            clock.tick()
            self.update(dt, animation_time, state)
            self.draw(screen)
            dt = clock.tick()
            fps_manager.update(dt)
            animation_time += dt

    def run(self, screen, fps_manager):
        self.reset_data()
        self.run_animation(START_MENU_SHOW, screen, fps_manager)
        dt = 0
        self.running = True
        while self.running:
            self.handle_events()
            clock.tick()
            self.update(dt)
            self.draw(screen)
            dt = clock.tick()
            fps_manager.update(dt)
        self.run_animation(START_MENU_HIDE, screen, fps_manager)
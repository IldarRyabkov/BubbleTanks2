import pygame as pg
import sys

from constants import *


class Menu:
    """A parent class for all menus. """
    def __init__(self, game):
        self.game = game
        self.pressed_button = None
        self.state = 0
        self.buttons = dict()
        self.widgets = dict()
        self.running = False
        self.is_opening = False
        self.is_closing = False

    @property
    def animation_time(self):
        return 0

    def close(self):
        self.pressed_button = None
        self.is_closing = True
        self.animation(CLOSE)
        self.is_closing = False
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        for button in self.buttons[self.state]:
            button.reset()
        self.running = False

    def open(self):
        for button in self.buttons[self.state]:
            button.reset()
        self.is_opening = True
        self.animation(OPEN)
        self.is_opening = False

    def set_language(self, language):
        pass

    def set_widgets_state(self, state):
        pass

    def set_state(self, state, button=None, animation=True):
        if button is not None:
            self.click_animation(button)
        if animation:
            self.animation(CLOSE)
        for button in self.buttons[self.state]:
            button.reset()
        for button in self.buttons[state]:
            button.reset()
        self.state = state
        self.set_widgets_state(state)
        if animation:
            self.animation(OPEN)

    def handle_event(self, event):
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONUP and event.button == pg.BUTTON_LEFT:
            button = self.pressed_button
            self.pressed_button = None
            if button is not None and button.clicked:
                button.action()
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
            for button in self.buttons[self.state]:
                if button.pressed:
                    self.pressed_button = button
                    break

    def handle_events(self):
        for event in pg.event.get():
            self.handle_event(event)

    @staticmethod
    def handle_events_animation():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def draw_background(self, screen):
        pass

    def draw(self, screen):
        self.draw_background(screen)
        for widget in self.widgets[self.state]:
            widget.draw(screen)
        for button in self.buttons[self.state]:
            button.draw(screen)
        pg.display.update()

    def set_cursor(self):
        cursor = pg.SYSTEM_CURSOR_ARROW
        for button in self.buttons[self.state]:
            if button.cursor_on_button:
                cursor = button.cursor
                break
        pg.mouse.set_cursor(cursor)

    def update_press_animation(self, button, dt):
        button.update_size(dt, True, default_alpha=255)

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        for widget in self.widgets[self.state]:
            widget.update(dt, animation_state, time_elapsed)

        for button in self.buttons[self.state]:
            button.update_look(dt, animation_state, time_elapsed)

        if self.pressed_button is not None:
            self.pressed_button.update(dt, animation_state, time_elapsed)
        else:
            for button in self.buttons[self.state]:
                button.update(dt, animation_state, time_elapsed)
            self.set_cursor()

    def click_animation(self, button):
        if button is None:
            return
        dt = time = 0
        duration = 200
        self.game.clock.tick()
        while time < duration:
            self.handle_events_animation()
            self.update_press_animation(button, dt)
            self.draw(self.game.screen)
            self.game.fps_manager.update(dt)
            dt = self.game.clock.tick()
            time += dt
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        self.game.clock.tick()

    def animation(self, animation_state):
        dt = time = 0
        duration = self.animation_time
        self.game.clock.tick()
        while time < duration:
            self.handle_events_animation()
            self.update(dt, animation_state, time / duration)
            self.draw(self.game.screen)
            self.game.fps_manager.update(dt)
            dt = self.game.clock.tick()
            time += dt
        self.game.clock.tick()

    def run(self):
        self.open()
        self.running = True
        dt = 0
        self.game.clock.tick()
        while self.running:
            self.handle_events()
            if self.running:
                self.update(dt)
            if self.running:
                self.draw(self.game.screen)
            self.game.fps_manager.update(dt)
            dt = self.game.clock.tick()


__all__ = ["Menu"]

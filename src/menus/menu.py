import pygame as pg

from data.constants import *


class Menu:
    """A parent class for all menus. """
    def __init__(self, game):
        self.game = game
        self.pressed_button = None
        self.state = 0
        self.previous_state = None
        self.buttons = dict()
        self.widgets = dict()
        self.running = False
        self.is_opening = False
        self.is_closing = False

    @property
    def animation_time(self):
        return 0

    def reset_buttons(self, state):
        for button in self.buttons[state]:
            button.reset(state)

    def close(self):
        self.pressed_button = None
        self.is_closing = True
        self.animation(CLOSE)
        self.is_closing = False
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        self.reset_buttons(self.state)
        self.running = False

    def open(self):
        self.reset_buttons(self.state)
        self.is_opening = True
        self.animation(OPEN)
        self.is_opening = False

    def set_language(self, language):
        pass

    def set_widgets_state(self, state):
        pass

    def set_state(self, state, button=None, animation=True):
        self.previous_state = self.state
        if button is not None:
            self.click_animation(button)
        if animation:
            self.animation(CLOSE)
        self.reset_buttons(self.state)
        self.reset_buttons(state)
        self.state = state
        self.set_widgets_state(state)
        if animation:
            self.animation(OPEN)

    def handle_event(self, event):
        if event.type == pg.QUIT:
            self.game.quit()
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

    def handle_events_animation(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()

    def draw_background(self, screen):
        pass

    def draw(self, screen, animation_state=WAIT):
        self.draw_background(screen)
        for widget in self.widgets[self.state]:
            widget.draw(screen, animation_state=animation_state)
        for button in self.buttons[self.state]:
            button.draw(screen, animation_state=animation_state)
        pg.display.update()

    def set_cursor(self):
        cursor = pg.SYSTEM_CURSOR_ARROW
        for button in self.buttons[self.state]:
            if button.cursor_on_button:
                cursor = button.cursor
                break
        pg.mouse.set_cursor(cursor)

    def update_click_animation(self, pressed_button, dt):
        for button in self.buttons[self.state]:
            button.update_look(dt)
        pressed_button.update_click_animation(dt)

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
            self.update_click_animation(button, dt)
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
            self.draw(self.game.screen, animation_state)
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

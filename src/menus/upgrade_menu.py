import sys
import pygame as pg

from gui.upgrade_button import UpgradeButton
from gui.upgrade_caption import UpgradeCaption
from data.config import SCR_H, SCR_W, UPGRADE_MENU_ANIMATION_TIME
import data.languages.english as eng
import data.languages.russian as rus


class UpgradeMenu:
    buttons = list()
    clock = pg.time.Clock()
    chosen_state = None
    is_running = False
    bg_surface = pg.Surface((SCR_W, SCR_H))
    text = None
    button_labels = None

    def __init__(self):
        self.caption = UpgradeCaption()
        self.set_language("English")

    def set_language(self, language):
        self.caption.set_language(language)
        if language == 'English':
            self.text = eng.UPGRADE_TEXT
            self.button_labels = eng.UPGRADEMENU_LABELS
        else:
            self.text = rus.UPGRADE_TEXT
            self.button_labels = rus.UPGRADEMENU_LABELS

    def setup(self, states):
        self.is_running = True
        self.caption.reset_velocity()
        self.buttons = []

        if len(states) == 3:
            self.buttons.append(UpgradeButton(*self.text[states[0]], self.button_labels, 1, states[0]))
            self.buttons.append(UpgradeButton(*self.text[states[1]], self.button_labels, 2, states[1]))
            self.buttons.append(UpgradeButton(*self.text[states[2]], self.button_labels, 3, states[2]))
        else:
            self.buttons.append(UpgradeButton(*self.text[states[0]], self.button_labels, 4, states[0]))
            self.buttons.append(UpgradeButton(*self.text[states[1]], self.button_labels, 5, states[1]))

    def handle_mouse_click(self):
        pos = pg.mouse.get_pos()
        for b in self.buttons:
            if b.cursor_on_button(pos):
                self.chosen_state = b.player_state
                self.is_running = False
                break

    def move(self, screen, action_marker):
        if action_marker == 'close':
            self.caption.vel_y *= -1
            for button in self.buttons:
                button.vel_x *= -1
                button.vel_y *= -1

        time, dt = 0, 0
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.clock.tick()
            self.update(dt)
            self.draw(screen)
            pg.display.update()
            dt = self.clock.tick()
            if time >= UPGRADE_MENU_ANIMATION_TIME:
                running = False
            elif time + dt > UPGRADE_MENU_ANIMATION_TIME:
                time = UPGRADE_MENU_ANIMATION_TIME
            else:
                time += dt

    def update(self, dt):
        for button in self.buttons:
            button.update(dt)
        self.caption.update_pos(dt)

    def draw(self, surface):
        surface.blit(self.bg_surface, (0, 0))
        for button in self.buttons:
            button.draw(surface)
        self.caption.draw(surface)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_mouse_click()

    def run(self, player_states, screen):
        self.setup(player_states)

        self.bg_surface.blit(screen, (0, 0))

        self.move(screen, 'open')

        while self.is_running:
            self.handle_events()
            self.update(0)
            self.draw(screen)
            pg.display.update()

        self.move(screen, 'close')
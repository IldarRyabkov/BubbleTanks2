import sys
import pygame as pg

from gui.upgrade_button import *
from gui.upgrade_menu_caption import UpgradeMenuCaption
from constants import *


class UpgradeMenu:
    """Menu that opens when the player has collected enough
    bubbles to gain a new level. In the upgrade menu, the
    player is asked to choose one of several tank improvements.
    When the player chooses a new tank, the upgrade menu closes.
    """
    def __init__(self, game):
        self.game = game

        self.animation_duration = 350
        self.caption = UpgradeMenuCaption(self.animation_duration)
        self.buttons = []
        self.chosen_tank = None
        self.running = False
        self.bg_surface = pg.Surface(SCR_SIZE)

    def set_buttons(self):
        new_tanks = self.get_next_tanks()
        lang = self.game.language
        sp = self.game.sound_player
        if len(new_tanks) == 3:
            self.buttons = (
                UpgradeButton(ButtonType.LEFT, new_tanks[0], lang, sp, self.animation_duration),
                UpgradeButton(ButtonType.CENTER, new_tanks[1], lang, sp, self.animation_duration),
                UpgradeButton(ButtonType.RIGHT, new_tanks[2], lang, sp, self.animation_duration)
            )
        else:
            self.buttons = (
                UpgradeButton(ButtonType.WIDE_LEFT, new_tanks[0], lang, sp, self.animation_duration),
                UpgradeButton(ButtonType.WIDE_RIGHT, new_tanks[1], lang, sp, self.animation_duration)
            )


    def get_next_tanks(self):
        """Returns new tanks available for player. """
        level, i = self.game.player.tank
        new_level = level + 1

        if level in (0, 2):
            indexes = (i, i + 1, i + 2)
        elif level == 1:
            indexes = (i, i + 1)
        elif i == 0:
            indexes = (i, i + 1, i + 2)
        elif i == 5:
            indexes = (i - 2, i - 1, i)
        else:
            indexes = (i - 1, i, i + 1)

        return [(new_level, new_index) for new_index in indexes]

    def set_language(self, language):
        self.caption.set_language(language)

    def handle_mouse_click(self):
        """Method is called when mouse button is pressed.
        Checks if any of buttons was pressed.
        """
        for button in self.buttons:
            if button.clicked:
                self.chosen_tank = button.tank
                self.running = False
                self.run_animation(CLOSE)
                break

    def handle_events(self, animation=False):
        """Handles user events. It does not handle mouse clicks during
        menu opening/closing animation, so that player can't
        accidentally press upgrade button during animation.
        """
        for e in pg.event.get():
            if e.type == pg.QUIT:
                sys.exit()

            elif e.type == pg.KEYDOWN and e.key in [pg.K_p, pg.K_ESCAPE]:
                self.game.pause_menu.run()
                self.running = self.game.running

            elif (not animation and e.type == pg.MOUSEBUTTONDOWN
                  and e.button == pg.BUTTON_LEFT):
                self.handle_mouse_click()

    def update(self, dt, animation_state=WAIT):
        for button in self.buttons:
            button.update(dt, animation_state)
        self.caption.update(dt, animation_state)

    def draw(self):
        """Draws menu background, buttons and caption. """
        self.game.screen.blit(self.bg_surface, (0, 0))
        for button in self.buttons:
            button.draw(self.game.screen)
        self.caption.draw(self.game.screen)
        pg.display.update()

    def run_animation(self, animation_state):
        """Upgrade menu animation loop which begins when
        the upgrade menu starts opening or closing.
        """
        dt = time = 0
        self.game.clock.tick()
        while time <= self.animation_duration:
            self.handle_events(animation=True)
            self.update(dt, animation_state)
            self.draw()
            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
            time += dt
        self.game.clock.tick()

    def run(self):
        self.running = True
        self.set_buttons()
        self.bg_surface.blit(self.game.screen, (0, 0))
        self.run_animation(OPEN)
        dt = 0
        self.game.clock.tick()
        while self.running:
            self.update(dt)
            self.draw()
            self.handle_events()
            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
        self.game.clock.tick()


__all__ = ["UpgradeMenu"]

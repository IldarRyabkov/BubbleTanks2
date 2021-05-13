import sys
import pygame as pg

from gui.upgrade_button import UpgradeButton
from gui.upgrade_menu_caption import UpgradeMenuCaption
from data.config import *


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
            if button.cursor_on_button:
                self.chosen_tank = button.tank
                self.running = False
                break

    def handle_events(self, animation=False):
        """Handles user events. It does not handle mouse clicks during
        menu opening/closing animation, so that player can't
        accidentally press upgrade button during animation.
        """
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif (not animation and e.type == pg.MOUSEBUTTONDOWN
                  and e.button == pg.BUTTON_LEFT):
                self.handle_mouse_click()

    def run_animation(self, action):
        """Upgrade menu animation loop which begins when
        the upgrade menu starts opening or closing.
        """
        self.game.clock.tick()
        dt = time = 0
        while time <= self.animation_duration:
            self.handle_events(animation=True)

            for button in self.buttons:
                button.update_pos(dt, action)
            self.caption.update_pos(dt, action)

            self.draw()

            dt = self.game.clock.tick()
            self.game.fps_manager.update(dt)
            time += dt

    def run(self):
        self.running = True

        new_tanks = self.get_next_tanks()
        lang = self.game.language
        if len(new_tanks) == 3:
            self.buttons = (
                UpgradeButton(UPG_BUTTON_LEFT, new_tanks[0], lang, self.animation_duration),
                UpgradeButton(UPG_BUTTON_CENTER, new_tanks[1], lang, self.animation_duration),
                UpgradeButton(UPG_BUTTON_RIGHT, new_tanks[2], lang, self.animation_duration)
            )
        else:
            self.buttons = (
                UpgradeButton(UPG_BUTTON_WIDE_LEFT, new_tanks[0], lang, self.animation_duration),
                UpgradeButton(UPG_BUTTON_WIDE_RIGHT, new_tanks[1], lang, self.animation_duration)
            )

        self.bg_surface.blit(self.game.screen, (0, 0))

        self.run_animation(OPEN)

        while self.running:
            self.handle_events()
            self.draw()

        self.run_animation(CLOSE)

        self.game.clock.tick()

    def draw(self):
        """Draws menu background, buttons and caption. """
        self.game.screen.blit(self.bg_surface, (0, 0))
        for button in self.buttons:
            button.draw(self.game.screen)
        self.caption.draw(self.game.screen)
        pg.display.update()


__all__ = ["UpgradeMenu"]

import sys
import pygame as pg

from gui.upgrade_button import UpgradeButton
from gui.upgrade_menu_caption import UpgradeMenuCaption
from data.config import *
from utils import get_next_tanks


class UpgradeMenu:
    """Menu that opens when the player has collected enough
    bubbles to gain a new level. In the upgrade menu, the
    player is asked to choose one of several tank improvements.
    When the player chooses a new tank, the upgrade menu closes.
    """
    def __init__(self):
        self.caption = UpgradeMenuCaption()
        self.buttons = []
        self.chosen_tank = None
        self.language = "English"
        self.running = False
        self.bg_surface = pg.Surface(SCR_SIZE)

    def set_language(self, language):
        self.caption.set_language(language)

    def set(self, player_tank):
        """Method is called when upgrade menu starts running.
        Sets all upgrade buttons based on player's current tank.
        """
        self.running = True

        new_tanks = get_next_tanks(player_tank)
        if len(new_tanks) == 3:
            self.buttons = (
                UpgradeButton(UPG_BUTTON_LEFT, new_tanks[0], self.language),
                UpgradeButton(UPG_BUTTON_CENTER, new_tanks[1], self.language),
                UpgradeButton(UPG_BUTTON_RIGHT, new_tanks[2], self.language)
            )
        else:
            self.buttons = (
                UpgradeButton(UPG_BUTTON_WIDE_LEFT, new_tanks[0], self.language),
                UpgradeButton(UPG_BUTTON_WIDE_RIGHT, new_tanks[1], self.language)
            )

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

    def update_pos(self, dt, action):
        """Method is called during menu opening/closing animations.
        Updates positions of buttons and caption.
        """
        for button in self.buttons:
            button.update_pos(dt, action)
        self.caption.update_pos(dt, action)

    def draw(self, screen):
        """Draws menu background, buttons and caption. """
        screen.blit(self.bg_surface, (0, 0))
        for button in self.buttons:
            button.draw(screen)
        self.caption.draw(screen)
        pg.display.update()

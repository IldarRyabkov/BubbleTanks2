import pygame as pg

from menus.menu import Menu
from gui.buttons.upgrade_button import *
from gui.widgets.upgrade_menu_caption import UpgradeMenuCaption
from constants import *
from utils import *
from states import UpgradeButtonType as Bt
from states import UpgradeMenuStates as St


class UpgradeMenu(Menu):
    """Menu that opens when the player has collected enough
    bubbles to gain a new level. In the upgrade menu, the
    player is asked to choose one of several tank improvements.
    When the player chooses a new tank, the upgrade menu closes.
    """
    def __init__(self, game):
        super().__init__(game)
        self.bg_surface = pg.Surface(SCR_SIZE)

        self.caption = UpgradeMenuCaption()
        self.widgets = {St.MAIN_STATE: (self.caption,)}

        self.upgrade_buttons = None
        self.chosen_tank = None

    def set_buttons(self):
        new_tanks = self.get_next_tanks()
        if len(new_tanks) == 3:
            self.upgrade_buttons = (
                UpgradeButton(self, Bt.LEFT, new_tanks[0]),
                UpgradeButton(self, Bt.CENTER, new_tanks[1]),
                UpgradeButton(self, Bt.RIGHT, new_tanks[2])
            )
        else:
            self.upgrade_buttons = (
                UpgradeButton(self, Bt.WIDE_LEFT, new_tanks[0]),
                UpgradeButton(self, Bt.WIDE_RIGHT, new_tanks[1])
            )
        self.buttons = {St.MAIN_STATE: self.upgrade_buttons}

    @property
    def animation_time(self):
        return 350

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

    def draw_background(self, screen):
        self.game.screen.blit(self.bg_surface, (0, 0))

    def open(self):
        self.set_buttons()
        self.caption.reset()
        self.bg_surface.blit(self.game.screen, (0, 0))
        super().open()

    @set_cursor_grab(False)
    def run(self):
        super().run()


__all__ = ["UpgradeMenu"]

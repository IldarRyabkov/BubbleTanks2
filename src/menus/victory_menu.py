import pygame as pg
from constants import *
from data.paths import *
from menus.menu import Menu
from gui.text_button import TextButton
from gui.text_widget import TextWidget
from gui.victory_menu_bubbles import VictoryMenuBubbles
from utils import *
from languages.texts import TEXTS
from states import VictoryMenuStates as St


class VictoryMenu(Menu):
    """Victory menu opens when player defeated the Final Boss.
    It has a button to return to the Main menu. """
    def __init__(self, game):
        super().__init__(game)
        # background
        self.bg_surface = pg.Surface(SCR_SIZE)
        self.mask = pg.Surface(SCR_SIZE)
        self.mask.set_alpha(195)

        # widgets
        self.bubbles = VictoryMenuBubbles()
        self.labels = (
            TextWidget(SCR_W2, H(128), FONT_1, H(90), WHITE, 1),
            TextWidget(SCR_W2, H(232), FONT_1, H(50), WHITE, 1),
        )
        # widgets dictionary
        self.widgets = { St.MAIN_STATE: (self.bubbles, *self.labels)}

        # buttons
        self.exit_button = TextButton(SCR_W2, H(628),
                                      TEXTS["exit to menu text"],
                                      CALIBRI_BOLD, H(58), 200,
                                      self.game.sound_player,
                                      action=self.exit, w=H(600))
        # buttons dictionary
        self.buttons = {St.MAIN_STATE: (self.exit_button,)}

    def exit(self):
        """Action of the 'exit' button. """
        self.game.sound_player.fade_out(250)
        self.click_animation(self.exit_button)
        self.running = False

    def set_language(self, language):
        for i, label in enumerate(self.labels):
            label.set_text(TEXTS["victory menu labels"][language][i])
        self.exit_button.set_language(language)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        self.game.update_scaling_objects(dt)
        super().update(dt, animation_state, time_elapsed)

    def draw_background(self, screen):
        """Draws all objects in the background and victory menu items. """
        screen.blit(self.bg_surface, (0, 0))
        self.game.draw_foreground()
        screen.blit(self.mask, (0, 0))

    @set_cursor_grab(False)
    def run(self):
        """Victory menu loop which starts after the Boss is defeated. """
        self.game.draw_background(self.bg_surface)
        self.exit_button.reset()
        super().run()

__all__ = ["VictoryMenu"]


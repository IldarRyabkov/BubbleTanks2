import pygame as pg

from data.constants import *
from data.languages import TEXTS
from data.states import VictoryMenuStates as St
from assets.paths import *
from menus.menu import Menu
from gui.buttons.text_button import TextButton
from gui.widgets.text_widget import TextWidget
from gui.widgets.victory_menu_bubbles import VictoryMenuBubbles
from gui.widgets.menu_caption import MenuCaption
from gui.widgets.mask import Mask
from components.utils import *


class VictoryMenu(Menu):
    """Victory menu opens when player defeated the Final Boss.
    It has a button to return to the Main menu. """
    def __init__(self, game):
        super().__init__(game)
        # background
        self.bg_surface = pg.Surface(SCR_SIZE)
        mask_surface = pg.Surface(SCR_SIZE, pg.SRCALPHA)
        mask_surface.fill((0, 0, 0, 175))
        self.mask = Mask(self, mask_surface)

        # widgets
        self.bubbles = VictoryMenuBubbles(self, game.rect, H(335))
        self.caption = MenuCaption(self, SCR_W2, H(50), FONT_1, H(90), WHITE, 1)
        self.texts = (
            TextWidget(SCR_W2, H(170), CALIBRI, H(45), WHITE, 1, H(960)),
            TextWidget(SCR_W2, H(410), CALIBRI, H(45), WHITE, 1, H(960)),
            TextWidget(SCR_W2, H(580), CALIBRI, H(45), WHITE, 1, H(960)),
            TextWidget(SCR_W2, H(720), CALIBRI, H(45), WHITE, 1, H(960)),
        )
        # widgets dictionary
        self.widgets = {St.MAIN_STATE: (self.mask, self.caption, self.bubbles, *self.texts)}

        # buttons
        self.exit_button = TextButton(SCR_W2, H(670),
                                      TEXTS["return to main menu text"],
                                      CALIBRI_BOLD, H(50), 255,
                                      self.game.sound_player,
                                      action=self.exit, w=H(620))

        self.continue_button = TextButton(SCR_W2, H(810),
                                          TEXTS["continue playing text"],
                                          CALIBRI_BOLD, H(50), 255,
                                          self.game.sound_player,
                                          action=self.continue_playing, w=H(980))

        # buttons dictionary
        base_buttons = self.exit_button, self.continue_button
        self.buttons = {St.MAIN_STATE: (*base_buttons,)}

    def exit(self):
        """Action of the 'exit' button. """
        self.game.sound_player.fade_out(200)
        self.click_animation(self.exit_button)
        self.running = False
        self.game.running = False

    def continue_playing(self):
        """Action of the 'continue playing' button. """
        self.game.bg_environment.boss_disposition = BOSS_IS_FAR_AWAY
        self.game.bg_environment.new_boss_disposition = BOSS_IS_FAR_AWAY
        self.game.bg_environment.boss_pos = None
        self.game.pause_menu.map_button.boss_aim.pos = None
        self.click_animation(self.continue_button)
        self.close()

    @property
    def animation_time(self):
        return 400

    def handle_event(self, event):
        super().handle_event(event)
        if event.type in [pg.KEYDOWN, pg.KEYUP]:
            self.game.player.handle(event.type, event.key)
        elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
            self.game.player.handle(event.type, event.button)

    def set_language(self, language):
        self.caption.set_text(TEXTS["victory menu caption"][language])
        for i, label in enumerate(self.texts):
            label.set_text(TEXTS["victory menu texts"][language][i])
        self.exit_button.set_language(language)
        self.continue_button.set_language(language)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        self.game.update_scaling_objects(dt)
        super().update(dt, animation_state, time_elapsed)

    def draw_background(self, screen):
        """Draws all objects in the background and victory menu items. """
        screen.blit(self.bg_surface, (0, 0))
        self.game.draw_foreground()

    def open(self):
        self.game.draw_background(self.bg_surface)
        super().open()

    @set_cursor_grab(False)
    def run(self):
        super().run()


__all__ = ["VictoryMenu"]

import pygame as pg

from data.paths import EXIT_BUTTON, EXIT_BUTTON_PRESSED, UI_CLICK
from utils import *


class ExitButton:
    """Button that is used to exit pause menu. """
    def __init__(self, xo, sound_player):
        self.x = xo + H(15)
        self.y = H(840)
        self.radius = H(34)

        self.sound_player = sound_player

        size = (2 * self.radius, 2 * self.radius)
        self.images = (
            pg.transform.scale(pg.image.load(EXIT_BUTTON).convert_alpha(), size),
            pg.transform.scale(pg.image.load(EXIT_BUTTON_PRESSED).convert_alpha(), size)
        )

    @property
    def cursor_on_button(self) -> bool:
        return circle_collidepoint(self.x + self.radius, self.y + self.radius,
                                   self.radius, *pg.mouse.get_pos())

    @property
    def clicked(self):
        """Handles left mouse button press event.
        Returns True, if scaling button was clicked. """
        if self.cursor_on_button:
            self.sound_player.play_sound(UI_CLICK)
            return True
        return False

    def draw(self, screen):
        screen.blit(self.images[self.cursor_on_button], (self.x, self.y))


__all__ = ["ExitButton"]

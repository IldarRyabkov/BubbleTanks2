from constants import *


class Mask:
    def __init__(self, menu, surface, pos=(0, 0)):
        self.menu = menu
        self.surface = surface
        self.pos = pos

    def set_alpha(self, alpha):
        self.surface.set_alpha(alpha)

    def update(self, dt, animation_state, time_elapsed):
        if animation_state == OPEN and self.menu.is_opening:
            self.set_alpha(round(255 * time_elapsed))
        elif animation_state == CLOSE and self.menu.is_closing:
            self.set_alpha(round(255 - 255 * time_elapsed))
        else:
            self.set_alpha(255)

    def draw(self, screen):
        screen.blit(self.surface, self.pos)


_all__ = ["Mask"]

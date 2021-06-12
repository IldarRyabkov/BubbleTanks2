from gui.widgets.text_widget import TextWidget
from data.constants import *


class MenuCaption(TextWidget):
    def __init__(self, menu, *args):
        super().__init__(*args)
        self.menu = menu

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        if animation_state == WAIT:
            self.set_alpha(255)
        elif self.menu.is_opening:
            self.set_alpha(round(255 * time_elapsed))
        elif self.menu.is_closing:
            self.set_alpha(round(255 - 255 * time_elapsed))


__all__ = ["MenuCaption"]

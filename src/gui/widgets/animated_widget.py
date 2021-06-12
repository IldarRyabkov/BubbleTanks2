from gui.widgets.widget import Widget
from data.constants import *


class AnimatedWidget(Widget):
    def __init__(self):
        super().__init__()

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        pass


__all__ = ["AnimatedWidget"]

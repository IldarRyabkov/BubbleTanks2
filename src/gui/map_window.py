from data.colors import WHITE
from gui.text import Text
from gui.map import Map
from data.gui_texts import MAP_WINDOW_CAPTION
from data.paths import CALIBRI_BOLD
from utils import H, HF


class MapWindow:
    """Window that shows map of rooms visited by player. """
    def __init__(self, xo):
        self.caption = Text(xo + HF(587), HF(176), CALIBRI_BOLD, H(56), WHITE, 1)
        self.map = Map(xo)

    def set_language(self, language):
        self.caption.set_text(MAP_WINDOW_CAPTION[language])

    def reset(self):
        self.map.reset()

    def update(self, dt):
        self.map.update(dt)

    def draw(self, screen):
        self.caption.draw(screen)
        self.map.draw(screen)


__all__ = ["MapWindow"]

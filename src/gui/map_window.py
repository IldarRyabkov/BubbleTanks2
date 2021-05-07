from data.colors import WHITE
from gui.text import Text
from gui.map import Map
from data.gui_texts import MAP_WINDOW_CAPTIONS as CAPTIONS
from data.paths import CALIBRI_BOLD
from utils import H, HF, WF


class MapWindow:
    """Window that shows map of rooms visited by player. """
    def __init__(self, xo):
        self.caption = Text(WF(584), HF(176), CALIBRI_BOLD, H(56), WHITE)
        self.map = Map(xo)

    def set_language(self, language):
        self.caption.set_text(CAPTIONS[language])

    def reset(self):
        self.map.reset()

    def update(self, dt):
        self.map.update(dt)

    def draw(self, screen):
        self.caption.draw(screen)
        self.map.draw(screen)


__all__ = ["MapWindow"]

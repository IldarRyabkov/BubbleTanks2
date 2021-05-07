from pygame import draw

from data.tank_bodies import TANK_BODIES
from data.gui_texts import STATS_WINDOW_TEXTS as TEXTS
from data.colors import WHITE, PAUSEMENU_PLAYER_BG
from data.paths import FONT_2, CALIBRI_BOLD
from gui.text import Text
from objects.body import Body
from utils import H


class StatsWindow:
    """Window that shows information about player's tank:
    name, appearance, description, main weapon, superpower.
    """
    def __init__(self, xo):
        self.language = "English"

        self.tank_body = None
        self.tank_body_pos = (xo + H(880), H(400))

        self.texts = (
            Text(xo + H(180), H(262), CALIBRI_BOLD, H(45), WHITE),
            Text(xo + H(180), H(646), CALIBRI_BOLD, H(37), WHITE),
            Text(xo + H(690), H(646), CALIBRI_BOLD, H(37), WHITE),
            Text(xo + H(180), H(318), FONT_2, H(30), WHITE),
            Text(xo + H(180), H(721), FONT_2, H(30), WHITE),
            Text(xo + H(690), H(721), FONT_2, H(30), WHITE)
        )

        self.captions = (
            Text(xo + H(512), H(176), CALIBRI_BOLD, H(56), WHITE),
            Text(xo + H(180), H(582), CALIBRI_BOLD, H(45), WHITE),
            Text(xo + H(690), H(582), CALIBRI_BOLD, H(45), WHITE)
        )

    def set_language(self, language):
        self.language = language
        for i, caption in enumerate(self.captions):
            caption.set_text(TEXTS[language]["captions"][i])
        self.set_player_stats((0, 0))

    def set_player_stats(self, player_state):
        """Sets tank description texts and tank appearance
        of player with given tank.
        """
        for i, text in enumerate(self.texts):
            text.set_text(TEXTS[self.language]["description"][player_state][i])
        self.tank_body = Body(TANK_BODIES[player_state])

    def update(self, dt):
        """Updates player's tank appearance. """
        x, y = self.tank_body_pos
        self.tank_body.update(x, y, dt, (9000, y))

    def draw_tank(self, screen):
        draw.circle(screen, WHITE, self.tank_body_pos, H(149))
        draw.circle(screen, PAUSEMENU_PLAYER_BG, self.tank_body_pos, H(142))
        self.tank_body.draw(screen)

    def draw(self, screen):
        for caption in self.captions:
            caption.draw(screen)
        for text in self.texts:
            text.draw(screen)
        self.draw_tank(screen)


__all__ = ["StatsWindow"]

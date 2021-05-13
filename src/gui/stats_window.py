from pygame import draw

from data.tank_bodies import TANK_BODIES
from data.gui_texts import STATS_WINDOW_TEXTS, STATS_WINDOW_CAPTION
from data.colors import WHITE, TANK_BG_COLOR
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

        self.text_widgets = (
            Text(xo + H(180), H(262), CALIBRI_BOLD, H(45), WHITE),
            Text(xo + H(180), H(646), CALIBRI_BOLD, H(37), WHITE),
            Text(xo + H(690), H(646), CALIBRI_BOLD, H(37), WHITE),
            Text(xo + H(180), H(318), FONT_2, H(30), WHITE),
            Text(xo + H(180), H(721), FONT_2, H(30), WHITE),
            Text(xo + H(690), H(721), FONT_2, H(30), WHITE),
        )
        self.labels = (
            Text(xo + H(180), H(582), CALIBRI_BOLD, H(45), WHITE),
            Text(xo + H(690), H(582), CALIBRI_BOLD, H(45), WHITE)
        )
        self.caption = Text(xo + H(578), H(176), CALIBRI_BOLD, H(56), WHITE, 1)

    def set_language(self, language):
        self.language = language
        self.caption.set_text(STATS_WINDOW_CAPTION[language])
        self.set_tank_descriptions((0, 0))

    def set_tank_descriptions(self, tank):
        for i, widget in enumerate(self.text_widgets):
            widget.set_text(STATS_WINDOW_TEXTS[self.language]["description"][tank][i])
        for i, label in enumerate(self.labels):
            label.set_text(STATS_WINDOW_TEXTS[self.language]["labels"][i])

    def set_player_stats(self, tank):
        """Sets tank description texts and tank appearance
        of player with given tank.
        """
        self.set_tank_descriptions(tank)
        self.tank_body = Body(TANK_BODIES[tank])

    def update(self, dt):
        """Updates player's tank appearance. """
        x, y = self.tank_body_pos
        self.tank_body.update(x, y, dt, (9000, y))

    def draw_tank(self, screen):
        draw.circle(screen, WHITE, self.tank_body_pos, H(149))
        draw.circle(screen, TANK_BG_COLOR, self.tank_body_pos, H(142))
        self.tank_body.draw(screen)

    def draw(self, screen):
        for label in self.labels:
            label.draw(screen)
        for widget in self.text_widgets:
            widget.draw(screen)
        self.caption.draw(screen)
        self.draw_tank(screen)


__all__ = ["StatsWindow"]

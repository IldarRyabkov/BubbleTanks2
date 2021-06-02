from bubble import Bubble
from utils import *
from constants import *


class VictoryMenuBubbles:
    def __init__(self):
        self.bubbles = (
            Bubble(SCR_W2 - H(192), SCR_H2 - H(80), 0, 0, "big"),
            Bubble(SCR_W2 + H(192), SCR_H2 - H(80), 0, 0, "big"),
            Bubble(SCR_W2, SCR_H2 - H(80), 0, 0, "big")
        )
        for bubble in self.bubbles:
            bubble.vel = 0

    def update(self, dt, animation_state, time_elapsed):
        for bubble in self.bubbles:
            bubble.update_body(dt)

    def draw(self, screen):
        for bubble in self.bubbles:
            bubble.draw(screen)


__all__ = ["VictoryMenuBubbles"]

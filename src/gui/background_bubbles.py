from random import uniform

from constants import *
from utils import *
from bubble import Bubble


class BackgroundBubbles:
    def __init__(self):
        self.bubbles = []
        self.time = 0

    def reset(self):
        self.__init__()

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        self.time += dt
        if self.time >= 150:
            self.time = 0
            new_bubble = Bubble(uniform(0, SCR_W), SCR_H + HF(13), 0, 0, "tiny")
            new_bubble.vel = -uniform(HF(0.32), HF(0.96))
            self.bubbles.append(new_bubble)

        for bubble in self.bubbles:
            bubble.y += bubble.vel * dt
            bubble.update_body(dt)

    def draw(self, screen):
        for bubble in self.bubbles:
            bubble.draw(screen)


__all__ = ["BackgroundBubbles"]

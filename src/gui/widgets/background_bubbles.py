from random import uniform

from data.constants import *
from components.utils import *
from components.bubble import Bubble
from gui.widgets.animated_widget import AnimatedWidget


class BackgroundBubbles(AnimatedWidget):
    def __init__(self, screen_rect):
        super().__init__()
        self.screen_rect = screen_rect
        self.bubbles = []
        self.time = 0

    def reset(self):
        self.__init__(self.screen_rect)

    def update(self, dt, animation_state=WAIT, time_elapsed=0.0):
        self.time += dt
        if self.time >= 180:
            self.time = 0
            new_bubble = Bubble(self.screen_rect, uniform(0, SCR_W), SCR_H + HF(13), 0, 0, "small")
            new_bubble.vel = -uniform(HF(0.32), HF(0.96))
            self.bubbles.append(new_bubble)

        for i, bubble in enumerate(self.bubbles):
            bubble.move(0, bubble.vel * dt)
            bubble.update_body(dt)
            if bubble.y < -bubble.radius:
                self.bubbles[i] = None
        self.bubbles = list(filter(lambda b: b is not None, self.bubbles))

    def draw(self, screen, animation_state=WAIT):
        for bubble in self.bubbles:
            bubble.draw(screen)


__all__ = ["BackgroundBubbles"]

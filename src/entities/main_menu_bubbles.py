from random import uniform

from objects.bubble import Bubble
from data.config import *


class Bubbles:
    BUBBLE_RADIUS = 11
    COOLDOWN = 200

    def __init__(self):
        self.time = 0
        self.bubbles = list()

    def add_bubble(self):
        x = uniform(0, SCR_W)
        y = SCR_H + self.BUBBLE_RADIUS
        new_bubble = Bubble(x, y)
        new_bubble.vel = (-0.2 - uniform(0, 0.4)) * SCR_H/600
        self.bubbles.append(new_bubble)

    def move_bubbles(self, dt):
        for bubble in self.bubbles:
            bubble.y += bubble.vel * dt
            bubble.update_body(dt)

    def delete_needless_bubbles(self):
        needless_bubbles = []
        for i in range(len(self.bubbles)):
            if self.bubbles[i].y <= -self.BUBBLE_RADIUS:
                needless_bubbles.append(i)
        needless_bubbles.reverse()
        for i in needless_bubbles:
            self.bubbles.pop(i)

    def update(self, dt):
        self.time += dt
        if self.time >= self.COOLDOWN:
            self.time -= self.COOLDOWN
            self.add_bubble()

        self.move_bubbles(dt)
        self.delete_needless_bubbles()

    def draw(self, surface):
        for bubble in self.bubbles:
            bubble.draw(surface, 0, 0)
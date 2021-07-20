from math import sin, cos

from components.bubble import Bubble
from components.utils import HF
from data.constants import CONFUSION_COLORS


class EnemyEvent:
    def __init__(self, owner, game, data: dict):
        self.owner = owner
        self.game = game
        self.trigger_value = data["trigger value"]
        self.action = self.set_action(data["action"])
        self.hit = False
        self.value = data["value"]

    def set_action(self, action: str):
        if action == "event bubbles":
            return self.drop_bubble
        if action == "change speed":
            return self.change_speed
        if action == "spawn enemies":
            return self.spawn_enemies
        if action == "enemy split":
            return self.enemy_split
        if action == "change color":
            return self.change_color
        return lambda: None

    def drop_bubble(self):
        bubble = Bubble(self.game.rect, self.owner.x, self.owner.y,
                        gravitation_radius=self.game.room.gravitation_radius)
        self.game.room.bubbles.append(bubble)

    def change_speed(self):
        self.owner.velocity = HF(self.value)

    def spawn_enemies(self):
        for _ in range(self.value[1]):
            self.game.room.spawn_enemy(self.value[0], self.owner.x, self.owner.y)

    def enemy_split(self):
        x, y, angle = self.owner.x, self.owner.y, self.owner.body.angle
        dx = HF(58.44) * sin(angle)
        dy = HF(58.44) * cos(angle)
        self.game.room.spawn_enemy("Twin", x + dx, y + dy, angle)
        self.game.room.spawn_enemy("Twin", x - dx, y - dy, angle)

    def change_color(self):
        color_1, color_2, color_3 = CONFUSION_COLORS[self.owner.health % 10]
        circle = self.owner.body.current_circles[0]
        circle.color = color_1
        circle.glares[0].color = circle.glares[1].color = circle.edge_color = color_2
        circle.glares[2].color = circle.glares[3].color = color_3


__all__ = ["EnemyEvent"]

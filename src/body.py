from math import pi

from circle import Circle
from utils import calculate_angle
from data.player import FROZEN_BODY, FROZEN_BODY_ROTATING
from constants import *


class Body:
    def __init__(self, circles, sticky_circles=()):
        self.angle = 0
        self.circles = [Circle(*circle_params) for circle_params in circles]
        self.sticky_circles = [Circle(*circle_params) for circle_params in sticky_circles]
        self.is_frozen = False
        self.frost_time = 0

    def become_infected(self):
        for circle in self.circles:
            circle.color = INFECTION_COLORS[circle.color]
            circle.edge_color = INFECTION_EDGE_COLOR
            for glare in circle.glares:
                glare.color = INFECTION_GLARE_COLORS[glare.color]

    def get_angle_of_rotation(self, destination_angle):
        """Method is called when player's tank body should be
        rotated due to tank movement.
        Returns the maximum angle body can be rotated.
        """
        # make sure that -pi <= self.angle <= pi for correct calculations
        if self.angle > pi: self.angle %= -2*pi
        elif self.angle < -pi: self.angle %= 2*pi

        # calculate delta_angle the body should turn
        delta_angle = abs(destination_angle - self.angle)
        if destination_angle < self.angle:
            delta_angle *= -1
        if abs(destination_angle - self.angle) > pi:
            delta_angle *= -1
        return delta_angle

    def move(self, dx, dy):
        for circle in self.circles:
            circle.move(dx, dy)
        if self.is_frozen:
            for circle in self.sticky_circles:
                circle.move(dx, dy)

    def move_to(self, x, y):
        for circle in self.circles:
            circle.update(x, y)
        if self.is_frozen:
            for circle in self.sticky_circles:
                circle.update(x, y)

    def make_unfrozen(self):
        self.is_frozen = False
        self.frost_time = 0

    def make_frozen(self):
        self.is_frozen = True
        self.frost_time = 0

    def update_frozen_state(self, dt):
        if self.is_frozen:
            self.frost_time += dt
            if self.frost_time >= 3000:
                self.make_unfrozen()

    def update(self, x, y, dt=0, target_x=0, target_y=0):
        angle_to_target = calculate_angle(x, y, target_x, target_y)
        for circle in self.circles:
            circle.update(x, y, dt, target_x, target_y, angle_to_target, self.angle)

        if self.is_frozen:
            for circle in self.sticky_circles:
                circle.update(x, y, dt, target_x, target_y, angle_to_target, self.angle)


    def draw(self, surface, dx=0, dy=0):
        for circle in self.circles:
            circle.draw(surface, dx, dy)

        if self.is_frozen:
            for circle in self.sticky_circles:
                circle.draw(surface, dx, dy)


class PlayerBody(Body):
    def __init__(self, circles, is_rotating, player, is_frozen=False):
        sticky_circles = FROZEN_BODY_ROTATING if is_rotating else FROZEN_BODY
        super().__init__(circles, sticky_circles)
        self.player = player
        self.is_rotating = is_rotating
        if is_frozen:
            self.make_frozen()

    def make_frozen(self):
        if not self.is_frozen:
            self.player.max_vel /= 4
            self.player.max_acc /= 4
            self.player.max_angular_acc /= 4
            self.player.max_angular_vel /= 4
        super().make_frozen()

    def make_unfrozen(self):
        if self.is_frozen:
            self.player.max_vel *= 4
            self.player.max_acc *= 4
            self.player.max_angular_acc *= 4
            self.player.max_angular_vel *= 4
        super().make_unfrozen()

    def update_pos(self, dt):
        x, y = self.player.x, self.player.y
        target_x, target_y = self.player.get_mouse_pos()
        angle_to_target = calculate_angle(x, y, target_x, target_y)
        if not self.is_rotating:
            self.angle = angle_to_target

        for circle in self.circles:
            circle.update(x, y, dt, target_x, target_y, angle_to_target, self.angle)

        if self.is_frozen:
            for circle in self.sticky_circles:
                circle.update(x, y, dt, target_x, target_y, angle_to_target, self.angle)



__all__ = ["Body", "PlayerBody"]

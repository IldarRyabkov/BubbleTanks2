from math import pi

from data.player_tanks import PLAYER_TANKS

from components.circle import make_circles_list
from components.utils import *


class PlayerBody:
    def __init__(self, owner, screen_rect, tank):
        data = PLAYER_TANKS[tank]
        self.screen_rect = screen_rect
        self.owner = owner
        self.angle = 0
        self.state = 0
        self.circles = self.init_circles(data)
        self.is_rotating = data["rotating"]

    @property
    def current_circles(self) -> list:
        return self.circles[self.state]

    def init_circles(self, data: dict) -> dict:
        all_circles = make_circles_list(self.screen_rect, data["circles"])
        circles = {}
        for (left, right), indexes in data["circles states"].items():
            for state in range(left, right + 1):
                circles[state] = [all_circles[i] for i in indexes]
        return circles

    def set_params(self, new_tank):
        """Method is called when player is being upgraded/downgraded.
        Updates body parameters according to new player's tank state"""
        data = PLAYER_TANKS[new_tank]
        self.circles = self.init_circles(data)
        self.is_rotating = data["rotating"]

    def get_angle_of_rotation(self, destination_angle):
        """Method is called when player's tank body should be
        rotated due to tank movement.
        Returns the maximum angle body can be rotated by.
        """
        # make sure that -pi <= self.angle <= pi for correct calculations
        if self.angle > pi:
            self.angle %= -2*pi
        elif self.angle < -pi:
            self.angle %= 2*pi

        # calculate delta_angle the body should turn by
        delta_angle = abs(destination_angle - self.angle)
        if destination_angle < self.angle:
            delta_angle *= -1
        if abs(destination_angle - self.angle) > pi:
            delta_angle *= -1
        return delta_angle

    def update_state(self, state):
        self.state = state
        x, y, angle = self.owner.x, self.owner.y, self.angle
        for circle in self.current_circles:
            circle.update(x, y, 0, angle)

    def update_shape(self, dt):
        x, y = self.owner.x, self.owner.y
        if not self.is_rotating:
            self.angle = calculate_angle(x, y, *self.owner.get_mouse_pos())
        angle = self.angle
        for circle in self.current_circles:
            circle.update(x, y, dt, angle)

    def draw(self, surface, dx=0, dy=0):
        for circle in self.current_circles:
            circle.draw(surface, dx, dy)


__all__ = ["PlayerBody"]

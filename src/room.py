from math import pi
import pygame as pg
from random import uniform

from bubble import Bubble
from constants import *
from utils import HF
from mobs import get_mob


class Room:
    """Class that stores, updates and draws all objects in the room, such as:

        - mobs;
        - bullets of mobs;
        - mines of mobs;
        - seekers of mobs;
        - bubbles;
        - special effects.

    It also stores some parameters of the room such as:

        - radius of player's gravitational field, in which bubbles are attracted to the player;
        - screen offset according to player's position, which is used to check if a mob should be drawn or not

    """
    bullets = []
    mines = []
    seekers = []
    bubbles = []

    # Bottom/top effects are drawn before/after player, mobs, bullets and bubbles are drawn.
    bottom_effects = []
    top_effects = []

    # new_mobs is a temporary list used to draw mobs of the new room during transportation of the player.
    # After transportation is done, list of mobs is replaced with the list of new mobs.
    mobs = []
    new_mobs = []

    gravitation_radius = HF(1.5 * 160)  # radius of player's gravitational field
    rect = pg.Rect(0, 0, SCR_W, SCR_H)  # rectangle within which the mobs will be drawn

    def __init__(self, game):
        self.game = game
        self.player = game.player

    def boss_defeated(self, boss_disposition) -> bool:
        return boss_disposition == BOSS_IN_CURRENT_ROOM and not self.mobs

    def reset(self):
        """ Method is called when a new game is started.
        Resets all room data.
        """
        self.bubbles = []
        self.bullets = []
        self.mines = []
        self.seekers = []
        self.top_effects = []
        self.bottom_effects = []
        self.mobs = []
        self.new_mobs = []

    def save_new_mobs(self, mobs_dict):
        self.new_mobs = []
        for name, n in mobs_dict.items():
            for _ in range(n):
                new_mob = get_mob(name, self.game, self.rect)
                self.new_mobs.append(new_mob)

    def move_new_mobs(self, dx, dy):
        for mob in self.new_mobs:
            mob.move(dx, dy)

    def set_params_after_transportation(self):
        """Clears all lists of objects in room and replaces the list
        of mobs with the list of new mobs for this room.
        """
        new_mobs = self.new_mobs
        self.reset()
        self.mobs = new_mobs

    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)
        self.bullets = list(filter(lambda b: not b.killed, self.bullets))[-50:]

    def update_mines(self, dt):
        for mine in self.mines:
            mine.update(dt)
        self.mines = list(filter(lambda m: not m.killed, self.mines))[-40:]

    def update_seekers(self, dt):
        for seeker in self.seekers:
            seeker.update(dt)
        self.seekers = list(filter(lambda s: not s.killed, self.seekers))[-40:]

    def update_bubbles(self, dt):
        x, y = self.player.x, self.player.y
        for bubble in self.bubbles:
            bubble.update(x, y, dt)
        self.bubbles = list(filter(lambda b: not b.is_outside, self.bubbles))
        if not self.mobs:
            for bubble in self.bubbles:
                bubble.maximize_gravity()

    def update_effects(self, dt):
        for effect in self.top_effects:
            effect.update(dt)
        for effect in self.bottom_effects:
            effect.update(dt)
        self.top_effects = list(filter(lambda e: e.running, self.top_effects))
        self.bottom_effects = list(filter(lambda e: e.running, self.bottom_effects))

    def set_gravity_radius(self, gravitation_radius):
        """Method is called when the player is being upgraded.
        Sets the new radius of player's gravitational field.
        """
        if self.mobs:
            self.gravitation_radius = gravitation_radius

            for bubble in self.bubbles:
                bubble.gravitation_radius = gravitation_radius

    def update_mobs(self, dt):
        """Updates all mobs in the room. If some mobs are killed,
        removes them from the list and adds bubbles.
        """
        for mob in self.mobs:
            mob.update(dt)
            if mob.health <= 0:
                self.add_bubbles(mob)
        self.mobs = list(filter(lambda m: m.health > 0, self.mobs))

    def update_new_mobs(self, dt):
        """ Updates all mobs in the room player is being transported to. """
        for mob in self.new_mobs:
            mob.update(dt)

    def update_screen_rect(self):
        """Sets the center of room screen-rectangle equal to the player's new pos. """
        self.rect.center = self.player.x, self.player.y

    def update(self, dt):
        """Updates all objects in the room and room parameters. """
        self.update_screen_rect()
        self.update_mobs(dt)
        self.update_new_mobs(dt)
        self.update_bubbles(dt)
        self.update_bullets(dt)
        self.update_mines(dt)
        self.update_seekers(dt)
        self.update_effects(dt)

    def add_bubbles(self, obj):
        """Method is called when an object is killed.
        Adds new bubbles to the list of bubbles.
        """
        for bubble_name, n in obj.bubbles.items():
            for i in range(n):
                bubble = Bubble(obj.x, obj.y, uniform(0, 2 * pi), self.gravitation_radius, bubble_name)
                self.bubbles.append(bubble)

    def draw_bubbles(self, surface, dx, dy):
        for bubble in self.bubbles:
            bubble.draw(surface, dx, dy)

    def draw_mobs(self, surface, dx, dy):
        for mob in self.mobs:
            mob.draw(surface, dx, dy)

    def draw_new_mobs(self, surface, dx, dy):
        for mob in self.new_mobs:
            mob.draw(surface, dx, dy)

    def draw_mines(self, surface, dx, dy):
        for mine in self.mines:
            mine.draw(surface, dx, dy)

    def draw_bullets(self, surface, dx, dy):
        for bullet in self.bullets:
            bullet.draw(surface, dx, dy)

        for bullet in self.seekers:
            bullet.draw(surface, dx, dy)

    def draw_top_effects(self, surface, dx, dy):
        for effect in self.top_effects:
            effect.draw(surface, dx, dy)

    def draw_bottom_effects(self, surface, dx, dy):
        for effect in self.bottom_effects:
            effect.draw(surface, dx, dy)


__all__ = ["Room"]

from math import pi, hypot
import pygame as pg
from random import uniform

from objects.bubble import Bubble
from objects.mobs import Mother
from entities.mob_guns import GunBossLeg
from entities.special_effects import add_effect
from data.config import *
from utils import HF


class Room:
    """Class that stores, updates and draws all objects in the room, such as:

        - mobs;
        - bullets of mobs;
        - homing bullets of mobs;
        - bubbles;
        - special effects.

    It also stores some parameters of the room such as:

        - radius of player's gravitational field, in which bubbles are attracted to the player;
        - screen offset according to player's position, which is used to check if a mob should be drawn or not

    """
    # Homing bullets are different from regular bullets. They have their own health
    # and can be knocked down by the player's bullets. Therefore, they are kept in a separate list.
    bullets = []
    homing_bullets = []

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

    def boss_defeated(self, boss_disposition):
        return boss_disposition == BOSS_IN_CURRENT_ROOM and not self.mobs

    def reset(self):
        """ Method is called when a new game is started.
        Resets all room data.
        """
        self.bubbles = []
        self.bullets = []
        self.homing_bullets = []
        self.top_effects = []
        self.bottom_effects = []
        self.mobs = []
        self.new_mobs = []

    def set_params_after_transportation(self):
        """Clears all lists of objects in room and replaces the list
        of mobs with the list of new mobs for this room.
        After that the temporary list of new mobs is cleared.
        """
        self.bubbles = []
        self.bullets = []
        self.homing_bullets = []
        self.top_effects = []
        self.bottom_effects = []
        self.mobs = self.new_mobs.copy()
        self.new_mobs = []

    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)
        # filter out bullets that hit the target or are outside the room and
        # make sure there are not more than 70 bullets (for performance reasons)
        self.bullets = list(filter(lambda b: not b.is_outside and not b.hit_the_target,
                                   self.bullets))[:70]

    def update_homing_bullets(self, player_x, player_y, dt):
        for bullet in self.homing_bullets:
            bullet.update(dt, player_x, player_y)
        # filter out homing bullets that hit the target or were shot down
        self.homing_bullets = list(filter(lambda b: b.health > 0 and not b.hit_the_target,
                                          self.homing_bullets))

    def update_bubbles(self, x, y, dt):
        for bubble in self.bubbles:
            bubble.update(x, y, dt)
        # filter out bubbles that are outside the room
        self.bubbles = list(filter(lambda b: not b.is_outside, self.bubbles))

    def update_effects(self, dt):
        for effect in self.top_effects:
            effect.update(dt)
        for effect in self.bottom_effects:
            effect.update(dt)
        # filter out effects that are not longer running
        self.top_effects = list(filter(lambda e: e.running, self.top_effects))
        self.bottom_effects = list(filter(lambda e: e.running, self.bottom_effects))

    def handle_bullet_explosion(self, bul_x, bul_y):
        """ Changes mobs' states according to their positions relative
        to the explosion, and adds some special effects.
        """
        for mob in self.mobs:
            if hypot(bul_x - mob.pos[0], bul_y - mob.pos[1]) <= 500:
                mob.health -= 25
                mob.update_body_look()
                add_effect('BigHitLines', self.top_effects, *mob.pos)
        add_effect('PowerfulExplosion', self.bottom_effects, bul_x, bul_y)
        add_effect('Flash', self.top_effects)

    def move_objects(self, offset):
        """ Method is called when the player is being transported
        to the next room. The objects of previous room become
        moved by the given offset to be drawn properly during
        player's transportation
        """
        for bubble in self.bubbles:
            bubble.move(*offset)

        for mob in self.mobs:
            mob.move(*offset)

        for bullet in self.bullets:
            bullet.move(*offset)

        for bullet in self.homing_bullets:
            bullet.move(*offset)

    def set_gravity_radius(self, gravitation_radius):
        """Method is called when the player is being upgraded.
        Sets the new radius of player's gravitational field.
        """
        if self.mobs:
            self.gravitation_radius = gravitation_radius

            for bubble in self.bubbles:
                bubble.gravitation_radius = gravitation_radius

    def update_mobs(self, target, dt):
        """Updates mobs in the room. All mobs receive a list of bullets
        as input in order to add new generated bullets to it.
        Some mobs are capable of creating new mobs.
        New mobs generated by them are put into the list of generated mobs
        Then the main list of mobs is extended with this list of generated mobs.
        """
        generated_mobs = []
        for mob in self.mobs:
            if isinstance(mob.gun, GunBossLeg):
                mob.update(target, self.homing_bullets, self.rect, dt)
            else:
                mob.update(target, self.bullets, self.rect, dt)
            if isinstance(mob, Mother):
                generated_mobs.extend(mob.generate_mob(dt))
        self.mobs.extend(generated_mobs)

        # add new bubbles for killed mobs
        for mob in self.mobs:
            if mob.health <= 0:
                self.add_bubbles(mob.pos, mob.bubbles)

        # filter out the mobs that are killed by player
        self.mobs = list(filter(lambda m: m.health > 0, self.mobs))

    def update_new_mobs(self, player_x, player_y, dt):
        """
        Method updates positions and bodies of all mobs of the room,
        player is being transported to.
        """
        target = (player_x, player_y)
        for mob in self.new_mobs:
            mob.update_pos(dt)
            mob.gamma = mob.count_gamma()
            mob.update_body(self.rect, dt, target)

    def set_screen_rect(self, pos):
        """Sets the center of room screen-rectangle equal to the player's new pos. """
        self.rect.center = pos

    def update(self, player_pos, dt):
        """Updates all objects in the room and room parameters. """
        self.set_screen_rect(player_pos)
        self.update_mobs(player_pos, dt)
        self.update_bubbles(*player_pos, dt)
        self.update_bullets(dt)
        self.update_homing_bullets(*player_pos, dt)
        self.update_effects(dt)

        # If all mobs are killed, we maximize gravity, so that all bubbles
        # start moving towards the player regardless of his position.
        if not self.mobs:
            for bubble in self.bubbles:
                bubble.maximize_gravity()

    def add_bubbles(self, mob_pos, mob_bubbles):
        """Method is called when a mob is killed.
        Adds mob's bubbles to the list of bubbles.
        """
        for bubble_name, n in mob_bubbles.items():
            for i in range(n):
                bubble = Bubble(*mob_pos, uniform(0, 2 * pi),
                                self.gravitation_radius, bubble_name)
                self.bubbles.append(bubble)

    def draw_bubbles(self, surface, dx, dy):
        for bubble in self.bubbles:
            bubble.draw(surface, dx, dy)

    def draw_mobs(self, surface, dx, dy):
        for mob in self.mobs:
            mob.draw(surface, dx, dy, self.rect)

    def draw_new_mobs(self, surface, dx, dy):
        for mob in self.new_mobs:
            mob.draw(surface, dx, dy, self.rect)

    def draw_bombs(self, surface, dx, dy):
        for bullet in self.bullets:
            if bullet.vel == 0:
                bullet.draw(surface, dx, dy)

    def draw_bullets(self, surface, dx, dy):
        for bullet in self.bullets:
            if bullet.vel != 0:
                bullet.draw(surface, dx, dy)

        for bullet in self.homing_bullets:
            bullet.draw(surface, dx, dy)

    def draw_top_effects(self, surface, dx, dy):
        for effect in self.top_effects:
            effect.draw(surface, dx, dy)

    def draw_bottom_effects(self, surface, dx, dy):
        for effect in self.bottom_effects:
            effect.draw(surface, dx, dy)


__all__ = ["Room"]

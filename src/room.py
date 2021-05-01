from math import pi, hypot
import pygame as pg
from random import uniform

from objects.bubble import Bubble
from objects.body import Body
from objects.mobs import Mother
from objects.mob_guns import GunBossLeg
from gui.text_box import TextBox
from special_effects import add_effect
from data.config import *
from data.colors import WHITE
from data.paths import FONT_1
from data.mobs import BOSS_SKELETON_BODY
from data.player import BG_RADIUS_00
from room_generator import BOSS_PIECES


class Room:
    """Class that stores, updates and draws all objects in the room, such as:

        - mobs;
        - bullets;
        - homing bullets;
        - bubbles;
        - special effects;
        - room hint text;
        - Boss Skeleton body

    It also stores some parameters of the room such as:

        - radius of player's gravitational field, in which bubbles are attracted to the player;

        - screen offset according to player's position (mobs should be drawn only if they are on screen)

        - boss disposition state ('in current room', 'in neighbour room', 'far away')
          which is used to determine should we draw boss skeleton or not.
          Normally mobs in a neighbour room aren't being drawn, but Boss Skeleton is too large,
          so it has to be drawn even if the Boss is in the neighbour room;

    """
    mobs = []
    bullets = []

    # Homing bullets are different from regular bullets. They have their own health
    # and can be knocked down by the player's bullets. Therefore, they are kept in a separate list.
    homing_bullets = []

    bubbles = []
    bottom_effects = []  # bottom effects are being drawn before all room objects are drawn
    top_effects = []  # top effects are being drawn after all room objects are drawn
    hint_text = None
    boss_skeleton = Body(BOSS_SKELETON_BODY)

    # This is a list that temporarily stores mobs for the next room while the player is being transported.
    # It is needed in order to separately draw and update mobs in the previous room and mobs
    # in the next room during the player's transportation. After the end of transportation,
    # the main list of mobs is replaced with a temporary list, and the temporary list is cleared.
    new_mobs = []

    # Additional parameters of the room
    gravity_radius = BG_RADIUS_00
    screen_rect = pg.Rect(0, 0, SCR_W, SCR_H)
    boss_state = BOSS_IN_NEIGHBOUR_ROOM

    def __init__(self):
        self.set_hint_text('')
        self.boss_skeleton.update(SCR_W2, SCR_H2, 0, (0, 0), 0.5 * pi)

    @property
    def boss_defeated(self):
        return self.boss_state == BOSS_IN_CURRENT_ROOM and not self.mobs

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
        self.boss_state = BOSS_IS_FAR_AWAY

    def set_params_after_transportation(self):
        """Clears all lists of objects in room and replaces the list
        of mobs to list of new mobs for this room.
        After that the temporary list of new mobs is cleared.
        """
        self.bubbles = []
        self.bullets = []
        self.homing_bullets = []
        self.top_effects = []
        self.bottom_effects = []
        self.mobs = self.new_mobs.copy()
        self.new_mobs = []

    def update_boss_state(self):
        """Updates the boss disposition state due to
        transportation of the player to the next room.
        """
        if self.boss_state == BOSS_IN_CURRENT_ROOM:
            self.boss_state = BOSS_IN_NEIGHBOUR_ROOM
        elif any(mob.name in BOSS_PIECES for mob in self.new_mobs):
            self.boss_state = BOSS_IN_CURRENT_ROOM
        else:
            self.boss_state = BOSS_IS_FAR_AWAY

    def set_hint_text(self, text):
        """
        :param text: list of strings
        sets background room hint text, explaining the rules of the game
        """
        self.hint_text = TextBox(text, FONT_1, int(47 * SCR_H/600), True,
                                 WHITE, (2/3 * SCR_H, 11/60 * SCR_H))

    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)
        # filter out bullets that hit the target or are outside the room and
        # make sure there are not more than 100 bullets (for performance reasons)
        self.bullets = list(filter(lambda b: not b.is_outside and
                                             not b.hit_the_target,
                                   self.bullets))[:100]

    def update_homing_bullets(self, player_x, player_y, dt):
        for bullet in self.homing_bullets:
            bullet.update(dt, player_x, player_y)
        # filter out homing bullets that hit the target or were shot down
        self.homing_bullets = list(filter(lambda b: b.health > 0 and
                                                    not b.hit_the_target,
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
        """
        Changes mobs' states according to their positions relative
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
        """
        Method is called when the player is being transported
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

        self.boss_skeleton.update(SCR_W2, SCR_H2, 0, (0, 0), 0.5 * pi)
        if self.boss_state == BOSS_IN_NEIGHBOUR_ROOM:
            self.boss_skeleton.move(*offset)

    def set_gravity_radius(self, gravity_radius):
        """ Sets the new radius of player's gravitational field. """
        if self.mobs:
            self.gravity_radius = gravity_radius

            for bubble in self.bubbles:
                bubble.gravity_r = gravity_radius

    def maximize_gravity(self):
        """
        Method is called when all mobs in the room are killed.
        The radius of player's gravitational field is set equal to
        the diameter of room, so that every bubble starts
        gravitating to player regardless of his position in the room.
        Also speeds of bubbles are maximized to reach player faster.
        """
        for bubble in self.bubbles:
            bubble.gravity_r = 2 * ROOM_RADIUS
            bubble.maximize_vel()

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
                mob.update(target, self.homing_bullets, self.screen_rect, dt)
            else:
                mob.update(target, self.bullets, self.screen_rect, dt)
            if isinstance(mob, Mother):
                generated_mobs.extend(mob.generate_mob(dt))
        self.mobs.extend(generated_mobs)

        # filter out the mobs that are killed by player
        for mob in self.mobs:
            if mob.health <= 0:
                self.add_bubbles(mob.pos, mob.bubbles)
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
            mob.update_body(self.screen_rect, dt, target)

    def set_screen_rect(self, pos):
        """Sets the center of room screen-rectangle equal to the player's new pos. """
        self.screen_rect.center = pos

    def update(self, player_pos, dt):
        """Updates all objects in the room and room parameters. """
        self.set_screen_rect(player_pos)
        self.update_mobs(player_pos, dt)
        self.update_bubbles(*player_pos, dt)
        self.update_bullets(dt)
        self.update_homing_bullets(*player_pos, dt)
        self.update_effects(dt)
        if not self.mobs:
            self.maximize_gravity()

    def add_bubbles(self, mob_pos, mob_bubbles):
        """Method is called when a mob is killed.
        Adds mob's bubbles to the list of bubbles.
        """
        for name, n in mob_bubbles.items():
            for i in range(n):
                bubble = Bubble(*mob_pos, uniform(0, 2 * pi),
                                self.gravity_radius, name)
                self.bubbles.append(bubble)

    def draw_hint_text(self, surface, dx, dy):
        self.hint_text.draw(surface, dx, dy)

    def draw_bubbles(self, surface, dx, dy):
        for bubble in self.bubbles:
            bubble.draw(surface, dx, dy)

    def draw_mobs(self, surface, dx, dy):
        for mob in self.mobs:
            mob.draw(surface, dx, dy, self.screen_rect)

    def draw_new_mobs(self, surface, dx, dy):
        for mob in self.new_mobs:
            mob.draw(surface, dx, dy, self.screen_rect)

    def draw_boss_skeleton(self, surface, dx, dy):
        if self.boss_state != BOSS_IS_FAR_AWAY:
            self.boss_skeleton.draw(surface, dx, dy)

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
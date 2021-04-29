
from math import pi, hypot
import pygame as pg
from random import uniform

from objects.bubble import Bubble
from objects.body import Body
from objects.mobs import MobMother
from gui.text_box import TextBox
from special_effects import add_effect
from data.config import SCR_H, SCR_W, SCR_H2, SCR_W2, ROOM_RADIUS
from data.colors import WHITE
from data.paths import FONT_1
from data.mobs import BOSS_SKELETON_BODY


class Room:
    """
    List of bullets is made separately from list of mobs, because
    when mob is dead and deleted, its bullets should continue existing.
    'new_mobs' is a temporary list of mobs, which is created
    to draw the mobs of room player is being transported to.
    When player is transported, self.mobs = self.new_mobs.copy().
    Text is a text text_surface of room, containing rules of the game.
    Screen rectangle is used to check if mob's rectangle collides
    with it. If yes, then a mob is drawn.
    Gravity radius is a radius of circle around player, in which bubbles
    gravitate to player.
    'Bottom effects' are drawn below player, mobs, bubbles and bullets,
    other effects are 'Top effects'.
    """
    bubbles = list()
    mobs = list()
    new_mobs = list()
    bullets = list()
    homing_bullets = list()
    bottom_effects = list()
    top_effects = list()
    text = None
    screen_rect = pg.Rect(0, 0, SCR_W, SCR_H)
    gravity_radius = 160
    boss_skeleton = Body(BOSS_SKELETON_BODY)
    boss_position_marker = 0

    def __init__(self):
        self.set_text('')
        self.boss_skeleton.update(SCR_W2, SCR_H2, 0, (0, 0), 0.5 * pi)

    def reset(self, new_game=False):
        """
        Method is called when a new game is started
        or a new room is visited. Resets all room data.
        """
        self.bubbles = []
        self.bullets = []
        self.homing_bullets = []
        self.top_effects = []
        self.bottom_effects = []
        self.mobs = [] if new_game else self.new_mobs.copy()
        self.new_mobs = []
        if new_game:
            self.boss_position_marker = 0

    def check_boss(self):
        if self.boss_position_marker in [1, 2]:
            self.boss_position_marker -= 1
        for mob in self.new_mobs:
            if mob.name in ['BossLeg', 'BossHead', 'BossHand']:
                self.boss_position_marker = 2
                break

    def set_new_mobs(self, new_mobs):
        self.new_mobs = new_mobs
        self.check_boss()

    def set_text(self, text):
        """
        :param text: list of strings
        sets background room text, explaining the rules of the game
        """
        self.text = TextBox(text, FONT_1, int(47 * SCR_H/600), True,
                            WHITE, (2/3 * SCR_H, 11/60 * SCR_H))

    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)
        # filter out bullets that hit the target or are outside the room and
        # make sure there are not more than 100 bullets (for performance reasons)
        self.bullets = list(filter(lambda b: not b.is_outside() and
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
        self.bubbles = list(filter(lambda b: not b.is_outside(), self.bubbles))

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
            if hypot(bul_x - mob.x, bul_y - mob.y) <= 500:
                mob.health -= 25
                mob.update_body_look()
                add_effect('BigHitLines', self.top_effects, mob.x, mob.y)
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
        if self.boss_position_marker == 1:
            self.boss_skeleton.move(*offset)

    def set_gravity_radius(self, gravity_radius):
        """ Sets the new radius of player's gravitational field. """
        if self.mobs:
            self.gravity_radius = gravity_radius

            for bubble in self.bubbles:
                bubble.gravity_r = gravity_radius

    def maximize_gravity(self):
        """
        Method is called when all mobs in the room are dead.
        The radius of player's gravitational field is set equal to
        the diameter of room, so that every bubble starts
        gravitating to player regardless of his position in the room.
        Also speeds of bubbles are maximized to reach player faster.
        """

        for bubble in self.bubbles:
            bubble.gravity_r = 2 * ROOM_RADIUS
            bubble.maximize_vel()

    def update_mobs(self, target, dt):
        generated_mobs = []
        for mob in self.mobs:
            mob.update(target, self.bullets, self.homing_bullets, self.screen_rect, dt)
            if isinstance(mob, MobMother):
                generated_mobs.extend(mob.generate_mob(dt))
        self.mobs.extend(generated_mobs)

        # filter out the mobs that are killed by player
        for mob in self.mobs:
            if mob.health <= 0:
                self.add_bubbles(mob.x, mob.y, mob.bubbles)
        self.mobs = list(filter(lambda x: x.health > 0, self.mobs))

    def update_new_mobs(self, player_x, player_y, dt):
        """
        Method updates positions and bodies of mobs of the room,
        player is being transported to.
        """
        target = (player_x, player_y)
        for mob in self.new_mobs:
            mob.update_pos(dt)
            mob.gamma = mob.count_gamma()
            if mob.body_rect.colliderect(self.screen_rect):
                mob.update_body(dt, target)

    def set_screen_rect(self, pos):
        self.screen_rect.center = pos

    def game_is_over(self):
        return self.boss_position_marker == 2 and not self.mobs

    def update(self, player_pos, dt):
        self.set_screen_rect(player_pos)

        self.update_mobs(player_pos, dt)
        self.update_bubbles(*player_pos, dt)
        self.update_bullets(dt)
        self.update_homing_bullets(*player_pos, dt)
        self.update_effects(dt)

        if not self.mobs:
            self.maximize_gravity()

    def add_bubbles(self, mob_x, mob_y, mob_bubbles):
        for name, n in mob_bubbles.items():
            for i in range(n):
                bubble = Bubble(mob_x, mob_y, uniform(0, 2 * pi),
                                self.gravity_radius, name)
                self.bubbles.append(bubble)

    def draw_text(self, surface, dx, dy):
        self.text.draw(surface, dx, dy)

    def draw_bubbles(self, surface, dx, dy):
        for bubble in self.bubbles:
            bubble.draw(surface, dx, dy)

    def draw_mobs(self, surface, dx, dy):
        for mob in self.mobs:
            if mob.body_rect.colliderect(self.screen_rect):
                mob.body.draw(surface, dx, dy)

    def draw_new_mobs(self, surface, dx, dy):
        for mob in self.new_mobs:
            if mob.body_rect.colliderect(self.screen_rect):
                mob.body.draw(surface, dx, dy)

    def draw_boss_skeleton(self, surface, dx, dy):
        if self.boss_position_marker:
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
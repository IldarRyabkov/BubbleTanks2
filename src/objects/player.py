import pygame as pg
from math import cos, sin, copysign, pi
import numpy as np

from data.config import *

from data.player import PLAYER_PARAMS
from data.paths import PLAYER_BULLET_SHOT
from objects.player_guns import get_gun
from superpowers import get_superpower
from objects.mob import Mob
from objects.body import Body
from utils import circle_collidepoint
from special_effects import add_effect


class Player(Mob):
    def __init__(self):
        (max_health, health_states, radius, body,
         MAX_VEL, ACC, gun_type, bg_radius, superpower) = PLAYER_PARAMS[(0, 0)]

        Mob.__init__(self,
                     name='Player',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=0,
                     health_states=health_states,
                     bubbles=0,
                     radius=radius,
                     body=body,
                     gun_type=gun_type)

        self.pos = np.array([self.x, self.y], dtype=float)
        self.MAX_VEL = MAX_VEL
        self.vel_x, self.vel_y = 0, 0
        self.ACC = ACC
        self.acc_x, self.acc_y = 0, 0
        self.MU = MU
        self.mu_x, self.mu_y = 0, 0
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.superpower = get_superpower(superpower)
        self.is_shooting = False
        self.bullets = []
        self.homing_bullets = []
        self.shurikens = []
        self.is_max_tank = False
        self.max_health = max_health
        self.bg_radius = bg_radius
        self.delta_health = 0
        self.defeated = False
        self.armor_on = [False]
        self.invisible = [False]
        self.state = (0, 0)
        self.states_history = [(0, 0)]

    def move(self, dx, dy):
        self.pos += np.array([dx, dy])

    def move_bullets(self, offset):
        for bullet in self.bullets:
            bullet.move(*offset)

        for bullet in self.homing_bullets:
            bullet.move(*offset)

    def stop_moving(self):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def set_params_after_transportation(self):
        self.vel_x = 0
        self.vel_y = 0
        self.delta_health = 0
        self.defeated = False
        self.clear_bullets()

    def is_ready_to_upgrade(self):
        return not self.is_max_tank and self.health >= self.max_health

    def get_mouse_pos(self):
        """
        :return: Mouse position relative to the center of the room
        """
        pos = pg.mouse.get_pos()
        mouse_pos = self.pos + np.array((pos[0] - SCR_W2, pos[1] - SCR_H2))
        return mouse_pos

    def rotate_body(self, dt):
        dest_angle = None
        if self.moving_left == self.moving_right:
            if self.moving_up and not self.moving_down:
                dest_angle = 0.5 * pi
            elif not self.moving_up and self.moving_down:
                dest_angle = -0.5 * pi

        elif self.moving_left and not self.moving_right:
            if self.moving_up and not self.moving_down:
                dest_angle = 0.75 * pi
            elif not self.moving_up and self.moving_down:
                dest_angle = -0.75 * pi
            else:
                dest_angle = pi

        else:
            if self.moving_up and not self.moving_down:
                dest_angle = 0.25 * pi
            elif not self.moving_up and self.moving_down:
                dest_angle = -0.25 * pi
            else:
                dest_angle = 0

        if dest_angle is not None:
            self.body.rotate(dest_angle, dt)

    def update_body(self, dt, target=(0, 0)):
        mouse_pos = self.get_mouse_pos()
        self.rotate_body(dt)
        self.body.update(*self.pos, dt, mouse_pos)

    def setup(self, max_health, health_states, radius, body,
         MAX_VEL, ACC, gun_type, bg_radius, superpower):
        self.gun = get_gun(gun_type)
        self.superpower = get_superpower(superpower)
        self.max_health = max_health
        self.health = 0
        self.health_states = health_states
        self.radius = radius
        self.body = Body(body)
        self.bg_radius = bg_radius
        self.MAX_VEL = MAX_VEL
        self.ACC = ACC
        self.armor_on = [False]
        self.invisible = [False]

    def collide_bullet(self, x, y):
        radius = self.bg_radius if self.armor_on[0] else self.radius
        return circle_collidepoint(*self.pos, radius, x, y)

    def collide_bubble(self, x, y):
        return circle_collidepoint(*self.pos, self.radius // 2, x, y)

    def in_latest_state(self):
        return self.state == self.states_history[-1]

    def handle_injure(self, damage):
        if not self.armor_on[0]:
            super().handle_injure(damage)
            self.delta_health += damage
            if self.health < 0 and self.state[0] == 0:
                self.defeated = True

    def handle_bubble_eating(self, bubble_health):
        self.health += bubble_health
        self.delta_health += bubble_health
        self.update_body_look()

    def make_body_frozen(self):
        for i in range(-6, 0):
            self.body.circles[i].visible = True

    def make_body_unfrozen(self):
        for i in range(-6, 0):
            self.body.circles[i].visible = False

    def make_frozen(self):
        self.frost_time = 0
        if not self.is_frozen:
            self.is_frozen = True
            self.MAX_VEL *= 0.2
            self.ACC *= 0.2
            self.make_body_frozen()

    def make_unfrozen(self):
        if self.is_frozen:
            self.is_frozen = False
            self.frost_time = 0
            self.MAX_VEL *= 5
            self.ACC *= 5
            self.make_body_unfrozen()

    def set_transportation_vel(self, alpha, max_vel):
        self.vel_x = max_vel * cos(alpha)
        self.vel_y = -max_vel * sin(alpha)

    def clear_bullets(self):
        """
        Method is called when player is transported to the next room.
        Deletes all player's bullets except orbiting shurikens.

        """
        self.bullets = []
        self.homing_bullets = []
        self.delete_needless_shurikens()

    def upgrade(self, new_state, state=None):
        self.shurikens = []
        if new_state:
            self.states_history.append(state)
            self.state = state
            self.moving_left = False
            self.moving_right = False
            self.moving_up = False
            self.moving_down = False
            self.is_shooting = False
        else:
            self.state = self.states_history[self.state[0] + 1]

        self.setup(*PLAYER_PARAMS[self.state])
        if new_state:
            self.is_shooting = False

        if self.state[0] == 5:
            self.is_max_tank = True

        if self.is_frozen:
            self.MAX_VEL *= 0.2
            self.ACC *= 0.2
            self.make_body_frozen()
        else:
            self.make_body_unfrozen()

    def downgrade(self):
        self.shurikens = []
        if self.state[0] >= 1:
            self.is_max_tank = False
            self.state = self.states_history[self.state[0] - 1]
            self.setup(*PLAYER_PARAMS[self.state])
            self.health = self.max_health - 1
            self.update_body_look()

            if self.is_frozen:
                self.MAX_VEL *= 0.2
                self.ACC *= 0.2
                self.make_body_frozen()
            else:
                self.make_body_unfrozen()
        else:
            self.health = 0

    def get_next_states(self):
        i, j = self.state[0], self.state[1]

        if self.state == (2, 3):
            return (i+1, j), (i+1, j+1), (i+1, j+2)

        if i == 1 or self.state == (4, 0):
            return (i+1, j), (i+1, j+1)

        elif self.state == (4, 5):
            return (i+1, j-1), (i+1, j)

        elif self.state == (3, 5):
            return (i+1, j-2), (i+1, j-1), (i+1, j)

        elif j == 0 or self.state == (0, 0):
            return (i+1, j), (i+1, j+1), (i+1, j+2)

        return (i+1, j-1), (i+1, j), (i+1, j+1)

    def delete_needless_bullets(self):
        """
        Deletes bullets that hit a target
        (or are outside the room) from the list.

        """
        needless_bullets = []
        for i, bullet in enumerate(self.bullets):
            if bullet.is_outside() or bullet.hit_the_target:
                needless_bullets.append(i)
        needless_bullets.reverse()
        for i in needless_bullets:
            self.bullets.pop(i)

    def delete_needless_homing_bullets(self, mobs, top_effects):
        """
        Deletes homing bullets with health <= 0 (or if they hit a target) from the list.
        If there are no mobs in the room, deletes all homing bullets.
        Adds special effects in the places the needless homing bullets were.

        """
        needless_bullets = []
        for i, bullet in enumerate(self.homing_bullets):
            if not mobs or bullet.health <= 0 or bullet.hit_the_target:
                needless_bullets.append(i)
                if not bullet.hit_the_target:
                    add_effect('RedHitCircle', top_effects, bullet.x, bullet.y)
        needless_bullets.reverse()
        for i in needless_bullets:
            self.homing_bullets.pop(i)

    def delete_needless_shurikens(self):
        """
        Deletes all shurikens that hit a target
        (or are outside the room and not orbiting) from the list.

        """
        needless_shurikens = []
        for i, shuriken in enumerate(self.shurikens):
            if not shuriken.is_orbiting and shuriken.is_outside() or shuriken.hit_the_target:
                needless_shurikens.append(i)
        needless_shurikens.reverse()
        for i in needless_shurikens:
            self.shurikens.pop(i)

    def add_bullets(self, dt, sound_player, mobs):
        """
        Adds new bullets generated by gun to the list.
        If there are new bullets, plays a "player_shot" sound.

        """
        sound_player.reset()

        self.gun.update_time(dt)
        old_length = len(self.bullets)

        if self.is_shooting and not self.invisible[0]:
            target = self.get_mouse_pos()
            self.gun.append_bullets(*self.pos, target, self.bullets, self.body.angle)

        if self.gun.automatic and len(mobs):
            self.gun.append_bullets_auto(*self.pos, mobs, self.bullets, self.body.angle)

        if len(self.bullets) > old_length:
            sound_player.play_sound(PLAYER_BULLET_SHOT)

    def update_bullets(self, dt, mobs, sound_player):
        self.add_bullets(dt, sound_player, mobs)
        fragments = []
        for bullet in self.bullets:
            params = (dt, fragments) if bullet.frangible else (dt,)
            bullet.update(*params)
        self.bullets.extend(fragments)
        self.delete_needless_bullets()

    def update_homing_bullets(self, dt, mobs, top_effects):
        target = (mobs[-1].x, mobs[-1].y) if len(mobs) else (0, 0)
        for bullet in self.homing_bullets:
            params = [dt, *target]
            bullet.update(*params)

        self.delete_needless_homing_bullets(mobs, top_effects)

    def update_shurikens(self, dt, mobs):
        for shuriken in self.shurikens:
            shuriken.update(dt, *self.pos, mobs)

        self.delete_needless_shurikens()

    def update_acc(self):
        if not self.moving_right ^ self.moving_left:
            self.acc_x = -copysign(1, self.vel_x)*self.MU if self.vel_x else 0
        elif abs(self.vel_x) == self.MAX_VEL:
                self.acc_x = 0
        else:
            self.acc_x = -self.ACC if self.moving_left else self.ACC

        if not self.moving_up ^ self.moving_down:
            self.acc_y = -copysign(1, self.vel_y)*self.MU if self.vel_y else 0
        elif abs(self.vel_y) == self.MAX_VEL:
                self.acc_y = 0
        else:
            self.acc_y = -self.ACC if self.moving_up else self.ACC

    def update_pos(self, dt, target=(0, 0)):
        dx = self.vel_x * dt + self.acc_x * dt*dt/2
        dy = self.vel_y * dt + self.acc_y * dt*dt/2
        self.move(dx, dy)

    def update_vel(self, dt):
        self.vel_x += self.acc_x * dt
        if self.vel_x * (self.vel_x - self.acc_x * dt) < 0:
            self.vel_x = 0
        elif abs(self.vel_x) > self.MAX_VEL:
            self.vel_x = copysign(1, self.vel_x) * self.MAX_VEL

        self.vel_y += self.acc_y * dt
        if self.vel_y * (self.vel_y - self.acc_y * dt) < 0:
            self.vel_y = 0
        elif abs(self.vel_y) > self.MAX_VEL:
            self.vel_y = copysign(1, self.vel_y) * self.MAX_VEL

    def update_superpower(self, dt, mobs, top_effects, bottom_effects,
                          camera):
        params = list()
        if self.superpower.name == "Armor":
            params = self.armor_on, top_effects

        elif self.superpower.name in ("Bombs", "ExplosionStar", "StickyExplosion"):
            params = self.pos, self.bullets

        elif self.superpower.name in ("ParalysingExplosion", "PowerfulExplosion"):
            params = self.pos, mobs, top_effects, bottom_effects, camera

        elif self.superpower.name == "Teleportation":
            params = self.pos, top_effects, camera

        elif self.superpower.name == "Ghost":
            params = self.invisible, self.body

        elif self.superpower.name == "HomingMissiles":
            params = self.pos, self.homing_bullets, self.health, self.body.angle

        elif self.superpower.name == "Shurikens":
            params = self.pos, self.shurikens

        elif self.superpower.name == "StickyCannon":
            params = *self.pos, self.body.angle, self.get_mouse_pos(), self.bullets

        elif self.superpower.name == "PowerfulCannon":
            params = *self.pos, self.get_mouse_pos(), self.bullets

        elif self.superpower.name == "GiantCannon":
            params = *self.pos, self.bullets, self.body.angle, camera

        self.superpower.update(dt, *params)

    def update(self, dt, mobs, top_effects, bottom_effects,
               camera, sound_player, transportation=False):
        if not transportation:
            self.update_acc()
            self.update_pos(dt)
            self.update_vel(dt)
        self.update_superpower(dt, mobs, top_effects, bottom_effects, camera)
        self.update_body(dt)
        if not transportation:
            self.update_bullets(dt, mobs, sound_player)
            self.update_homing_bullets(dt, mobs, top_effects)
        self.update_shurikens(dt, mobs)
        self.update_frozen_state(dt)

    def draw(self, surface, dx, dy):
        for bullet in self.bullets:
            if bullet.vel == 0:
                bullet.draw(surface, dx, dy)

        self.body.draw(surface, dx, dy)

        for bullet in self.bullets:
            if bullet.vel != 0:
                bullet.draw(surface, dx, dy)

        for bullet in self.homing_bullets:
            bullet.draw(surface, dx, dy)

        for shuriken in self.shurikens:
            shuriken.draw(surface, dx, dy)
import pygame as pg
from math import cos, sin, pi
import numpy as np

from data.config import *
from data.player import PLAYER_PARAMS
from data.paths import PLAYER_BULLET_SHOT

from entities.player_guns import get_gun
from entities.superpowers import *
from entities.special_effects import add_effect

from objects.bullets import FrangibleBullet, DrillingBullet
from objects.gun import GunAutomatic
from objects.base_mob import BaseMob

from utils import circle_collidepoint


class Player(BaseMob):
    def __init__(self):
        (max_health, health_states, radius, body, max_vel, max_acc,
         gun_type, bg_radius, superpower) = PLAYER_PARAMS[(0, 0)].values()

        super().__init__(0,
                         max_health,
                         health_states,
                         radius,
                         body)
        self.pos = np.array([SCR_W2, SCR_H2], dtype=float)
        self.bg_radius = bg_radius
        self.max_vel = max_vel
        self.vel_x = self.vel_y = 0
        self.max_acc = max_acc
        self.acc_x= self.acc_y = 0

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.shooting = False

        self.superpower = get_superpower(superpower)
        self.gun = get_gun(gun_type)

        self.bullets = []
        self.homing_bullets = []
        self.shurikens = []

        self.max_health = max_health
        self.delta_health = 0

        self.tank = (0, 0)
        self.tanks_history = [(0, 0)]

    @property
    def level(self):
        return self.tank[0]

    @property
    def is_ready_to_upgrade(self):
        return self.level < 5 and self.health >= self.max_health

    @property
    def last_tank_in_history(self):
        """ Called when player requests tank upgrade.
        Checks if player's current tank is last in his history of tanks.
        If so, there is a need to open upgrade menu to choose a new tank.
        """
        return self.tank == self.tanks_history[-1]

    @property
    def defeated(self):
        return self.health < 0 and self.level == 0

    @property
    def armor_on(self):
        return (isinstance(self.superpower, Armor) and
                self.superpower.time < 0.4 * self.superpower.cooldown_time)

    @property
    def invisible(self):
        return (isinstance(self.superpower, Ghost) and
                (self.superpower.on or self.superpower.dist != 0))

    def reset(self):
        self.__init__()

    def move(self, dx, dy):
        self.pos += np.array([dx, dy], dtype=float)

    def move_bullets(self, offset):
        """Method is called when player is being transported to the next room.
        Moves all player's bullets by given offset to draw them
        properly during transportation.
        """
        for bullet in self.bullets:
            bullet.move(*offset)

        for bullet in self.homing_bullets:
            bullet.move(*offset)

        for shuriken in self.shurikens:
            if not shuriken.is_orbiting:
                shuriken.move(*offset)

    def stop_moving(self):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def set_params_after_transportation(self):
        self.vel_x = 0
        self.vel_y = 0
        self.health = max(self.health, 0)
        self.delta_health = 0
        self.clear_bullets()

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

    def update_body(self, dt):
        mouse_pos = self.get_mouse_pos()
        self.rotate_body(dt)
        self.body.update(*self.pos, dt, mouse_pos)

    def setup(self, max_health, health_states, radius, body,
              max_vel, max_acc, gun_type, bg_radius, superpower):
        super().__init__(0, max_health, health_states, radius, body)
        self.gun = get_gun(gun_type)
        self.superpower = get_superpower(superpower)
        self.bg_radius = bg_radius
        self.max_vel = max_vel
        self.max_acc = max_acc

    def collide_bullet(self, x, y, r):
        radius = self.bg_radius if self.armor_on else self.radius
        return circle_collidepoint(*self.pos, radius + r, x, y)

    def collide_bubble(self, x, y):
        return circle_collidepoint(*self.pos, self.radius // 2, x, y)

    def handle_injure(self, damage):
        if not self.armor_on:
            super().handle_injure(damage)
            self.delta_health += damage

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
        if not self.is_frozen:
            self.max_vel *= 0.2
            self.max_acc *= 0.2
        super().make_frozen()

    def make_unfrozen(self):
        if self.is_frozen:
            self.max_vel *= 5
            self.max_acc *= 5
        super().make_unfrozen()

    def set_transportation_vel(self, angle, velocity):
        self.vel_x = velocity * cos(angle)
        self.vel_y = -velocity * sin(angle)

    def clear_bullets(self):
        """
        Method is called when player is transported to the next room.
        Deletes all player's bullets except orbiting shurikens.

        """
        self.bullets = []
        self.homing_bullets = []
        self.shurikens = list(filter(lambda x: x.is_orbiting, self.shurikens))

    def upgrade(self, new_state, state=None):
        self.shurikens = []
        if new_state:
            self.tanks_history.append(state)
            self.tank = state
            self.stop_moving()
            self.shooting = False
        else:
            self.tank = self.tanks_history[self.tank[0] + 1]

        self.setup(*PLAYER_PARAMS[self.tank].values())
        if new_state:
            self.shooting = False

        if self.is_frozen:
            self.max_vel *= 0.2
            self.max_acc *= 0.2
            self.make_body_frozen()
        else:
            self.make_body_unfrozen()

    def downgrade(self):
        self.shurikens = []
        if self.level >= 1:
            self.tank = self.tanks_history[self.level - 1]
            self.setup(*PLAYER_PARAMS[self.tank].values())
            self.health = self.max_health - 1
            self.update_body_look()

            if self.is_frozen:
                self.max_vel *= 0.2
                self.max_acc *= 0.2
                self.make_body_frozen()
            else:
                self.make_body_unfrozen()
        else:
            self.health = 0

    def add_bullets(self, dt, sound_player, mobs):
        """
        Adds new bullets generated by gun to the list.
        If there are new bullets, plays a "player_shot" sound.

        """
        sound_player.reset()

        self.gun.update_time(dt)
        old_length = len(self.bullets)

        if self.shooting and not self.invisible:
            target = self.get_mouse_pos()
            self.gun.add_bullets(*self.pos, target, self.bullets, self.body.angle)

        if isinstance(self.gun, GunAutomatic) and mobs:
            self.gun.add_bullets_auto(self.pos, mobs, self.bullets, self.body.angle)

        # play bullet sound only one time, regardless of the number of added bullets
        if len(self.bullets) > old_length:
            sound_player.play_sound(PLAYER_BULLET_SHOT)

    def update_bullets(self, dt, mobs, sound_player):
        self.add_bullets(dt, sound_player, mobs)
        fragments = []
        for bullet in self.bullets:
            if isinstance(bullet, FrangibleBullet): params = dt, fragments
            elif isinstance(bullet, DrillingBullet): params = dt,
            else: params = dt,
            bullet.update(*params)
        self.bullets.extend(fragments)

        # filter all needless homing bullets
        self.bullets = list(filter(lambda b: not b.is_outside and not b.hit_the_target,
                                   self.bullets))

    def update_homing_bullets(self, dt, mobs, top_effects):
        if mobs:
            for bullet in self.homing_bullets:
                bullet.update(dt, *mobs[-1].pos)

        # add disappearing effects for needless homing bullets
        for b in self.homing_bullets:
            if not mobs or b.health <= 0 or b.hit_the_target:
                add_effect('RedHitCircle', top_effects, b.x, b.y)

        # filter all needless homing bullets
        self.homing_bullets = list(filter(lambda x: mobs and x.health > 0 and not x.hit_the_target,
                                          self.homing_bullets))

    def update_shurikens(self, dt, mobs):
        for shuriken in self.shurikens:
            shuriken.update(dt, *self.pos, mobs)

        # filter all needless shurikens
        self.shurikens = list(filter(lambda x: (x.is_orbiting or not x.is_outside)
                                               and not x.hit_the_target, self.shurikens))

    def update_acc(self):
        if not self.moving_right ^ self.moving_left:
            # If the left and right movement keys are not pressed
            # (or are pressed together), acceleration must be opposite
            # to speed in order to slow down the player's movement.
            self.acc_x = -np.sign(self.vel_x) * MU
        elif abs(self.vel_x) == self.max_vel:
            # If the player has reached maximum speed, he must stop accelerating
            self.acc_x = 0
        else:
            # In normal case acceleration must be co-directional
            # with movement according to the pressed movement key.
            self.acc_x = -self.max_acc if self.moving_left else self.max_acc

        # Same thing with acc_y
        if not self.moving_up ^ self.moving_down:
            self.acc_y = -np.sign(self.vel_y) * MU
        elif abs(self.vel_y) == self.max_vel:
                self.acc_y = 0
        else:
            self.acc_y = -self.max_acc if self.moving_up else self.max_acc

    def update_pos(self, dt):
        self.update_acc()
        self.update_vel(dt)
        dx = self.vel_x * dt + self.acc_x * dt*dt/2
        dy = self.vel_y * dt + self.acc_y * dt*dt/2
        self.move(dx, dy)

    def update_vel(self, dt):
        self.vel_x += self.acc_x * dt
        if self.vel_x * (self.vel_x - self.acc_x * dt) < 0:
            self.vel_x = 0
        elif abs(self.vel_x) > self.max_vel:
            self.vel_x = np.sign(self.vel_x) * self.max_vel

        self.vel_y += self.acc_y * dt
        if self.vel_y * (self.vel_y - self.acc_y * dt) < 0:
            self.vel_y = 0
        elif abs(self.vel_y) > self.max_vel:
            self.vel_y = np.sign(self.vel_y) * self.max_vel

    def update_superpower(self, dt, mobs, top_effects, bottom_effects, camera, sound_player):
        args = []
        if isinstance(self.superpower, Armor):
            args = top_effects,
        elif isinstance(self.superpower, (Bombs, ExplosionStar, StickyExplosion)):
            args = self.pos, self.bullets
        elif isinstance(self.superpower, (ParalysingExplosion, PowerfulExplosion)):
            args = self.pos, mobs, top_effects, bottom_effects, camera, sound_player
        elif isinstance(self.superpower, Teleportation):
            args = self.pos, top_effects, camera
        elif isinstance(self.superpower, Ghost):
            args = self.body,
        elif isinstance(self.superpower, HomingMissiles):
            args = self.pos, self.homing_bullets, self.health, self.body.angle
        elif isinstance(self.superpower, Shurikens):
            args = self.pos, self.shurikens
        elif isinstance(self.superpower, StickyCannon):
            args = *self.pos, self.body.angle, self.get_mouse_pos(), self.bullets
        elif isinstance(self.superpower, PowerfulCannon):
            args = *self.pos, self.get_mouse_pos(), self.bullets
        elif isinstance(self.superpower, GiantCannon):
            args = *self.pos, self.bullets, camera
        self.superpower.update(dt, *args)

    def update_during_transportation(self, dt):
        """Updates player's params during transportation. """
        self.move(self.vel_x * dt, self.vel_y * dt)
        self.update_body(dt)
        self.update_shurikens(dt, [])
        self.update_frozen_state(dt)
        self.gun.update_time(dt)
        if isinstance(self.superpower, Ghost):
            self.superpower.update(dt, self.body)
        else:
            self.superpower.update_time(dt)

    def update(self, dt, mobs, top_effects, bottom_effects, camera, sound_player):
        self.update_pos(dt)
        self.update_superpower(dt, mobs, top_effects, bottom_effects, camera, sound_player)
        self.update_body(dt)
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


__all__ = ["Player"]

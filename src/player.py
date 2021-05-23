import pygame as pg
from math import cos, sin, pi, hypot
import numpy as np

from constants import *
from data.player import *
from data.paths import PLAYER_BULLET_SHOT

from player_guns import get_gun
from superpowers import *
from special_effects import add_effect
from body import PlayerBody

from bullets import FrangibleBullet
from gun import GunAutomatic
from base_mob import BaseMob

from utils import *


class Player(BaseMob):
    def __init__(self, game):
        (max_health, health_states, radius, body, body_is_rotating, max_vel,
         max_acc, gun_type, bg_radius, superpower) = PLAYER_PARAMS[(0, 0)].values()

        super().__init__(0, max_health, health_states, radius, body)
        self.game = game

        self.pos = np.array([SCR_W2, SCR_H2], dtype=float)
        self.bg_radius = bg_radius
        self.body = PlayerBody(body, body_is_rotating, self)

        self.max_vel = max_vel
        self.vel_x = self.vel_y = 0
        self.max_acc = max_acc
        self.acc_x= self.acc_y = 0

        self.max_angular_vel = 0.00024 * pi
        self.max_angular_acc = 0.000002
        self.angular_vel = 0
        self.angular_acc = self.max_angular_acc

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.shooting = False

        self.superpower = get_superpower(superpower)
        self.superpower.game = game
        self.superpower.player = self
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
        self.__init__(self.game)

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
        """Rotates player's tank body according to its movement."""
        if self.moving_left == self.moving_right:
            if self.moving_up ^ self.moving_down:
                destination_angle = 0.5 * pi if self.moving_up else -0.5 * pi
            else:
                destination_angle = None

        elif self.moving_left:
            if self.moving_up ^ self.moving_down:
                destination_angle = 0.75 * pi if self.moving_up else -0.75 * pi
            else:
                destination_angle = pi

        else:
            if self.moving_up ^ self.moving_down:
                destination_angle = 0.25 * pi if self.moving_up else -0.25 * pi
            else:
                destination_angle = 0

        if destination_angle is not None:
            angle = self.body.get_angle_of_rotation(destination_angle, dt)
            self.angular_acc = np.sign(angle) * self.max_angular_acc

            self.angular_vel += self.angular_acc * dt
            if abs(self.angular_vel) > self.max_angular_vel:
                self.angular_vel = np.sign(self.angular_vel) * self.max_angular_vel

            d_angle = self.angular_vel * dt + self.angular_acc * dt*dt/2
            if abs(d_angle) > abs(angle):
                d_angle = angle
                self.angular_vel = 0
                self.angular_acc = 0
            self.body.angle += d_angle
        else:
            self.angular_acc = -np.sign(self.angular_vel) * self.max_angular_acc * 0.2

            self.angular_vel += self.angular_acc * dt
            if abs(self.angular_vel) > self.max_angular_vel:
                self.angular_vel = np.sign(self.angular_vel) * self.max_angular_vel
            d_angle = self.angular_vel * dt + self.angular_acc * dt*dt/2
            self.body.angle += d_angle

    def update_body(self, dt):
        if self.body.is_rotating:
            self.rotate_body(dt)

        mouse_pos = self.get_mouse_pos()
        self.body.update(*self.pos, dt, mouse_pos)
        self.body.update_frozen_state(dt)

    def setup(self, max_health, health_states, radius, body, body_is_rotating,
              max_vel, max_acc, gun_type, bg_radius, superpower):
        self.health = 0
        self.max_health = max_health
        self.health_states = health_states
        self.radius = radius
        self.body = PlayerBody(body, body_is_rotating, self)
        self.gun = get_gun(gun_type)
        self.superpower = get_superpower(superpower)
        self.superpower.game = self.game
        self.superpower.player = self
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

    def upgrade(self, tank_is_new: bool, tank=None):
        self.shurikens = []
        if tank_is_new:
            self.tanks_history.append(tank)
            self.tank = tank
            self.stop_moving()
            self.shooting = False
        else:
            self.tank = self.tanks_history[self.tank[0] + 1]

        self.setup(*PLAYER_PARAMS[self.tank].values())
        if tank_is_new:
            self.shooting = False

        if self.body.is_frozen:
            self.max_vel *= 0.2
            self.max_acc *= 0.2

    def downgrade(self):
        self.shurikens = []
        if self.level >= 1:
            self.tank = self.tanks_history[self.level - 1]
            self.setup(*PLAYER_PARAMS[self.tank].values())
            self.health = self.max_health - 1
            self.update_body_look()

            if self.body.is_frozen:
                self.max_vel *= 0.2
                self.max_acc *= 0.2
        else:
            self.health = 0

    def update_gun(self, dt):
        """ Updates gun and adds new bullets generated by gun. """
        self.gun.update_time(dt)

        if self.shooting and not self.invisible and self.gun.ready_to_shoot:
            self.bullets.extend(self.gun.generate_bullets(*self.pos, self.get_mouse_pos(), self.body.angle))
            self.game.sound_player.play_sound(PLAYER_BULLET_SHOT)

        if isinstance(self.gun, GunAutomatic) and self.game.room.mobs and self.gun.ready_to_shoot_auto:
            target_mob = min(self.game.room.mobs, key=lambda mob: hypot(*(self.pos - mob.pos)))
            self.bullets.extend(self.gun.generate_bullets_auto(*self.pos, target_mob, self.body.angle))
            self.game.sound_player.play_sound(PLAYER_BULLET_SHOT)

    def update_bullets(self, dt):
        for bullet in self.bullets:
            if isinstance(bullet, FrangibleBullet):
                bullet.update(dt, self.bullets)
            else:
                bullet.update(dt)

        self.bullets = list(filter(lambda b: not b.is_outside and
                                             not b.hit_the_target, self.bullets))

    def update_homing_bullets(self, dt):
        if self.game.room.mobs:
            for bullet in self.homing_bullets:
                bullet.update(dt, *self.game.room.mobs[-1].pos)

        for i, bullet in enumerate(self.homing_bullets):
            if not self.game.room.mobs or bullet.health <= 0 or bullet.hit_the_target:
                self.homing_bullets[i] = None
                add_effect('RedHitCircle', self.game.room.top_effects, bullet.x, bullet.y)

        self.homing_bullets = list(filter(lambda b: b is not None, self.homing_bullets))

    def update_shurikens(self, dt, transportation=False):
        mobs = [] if transportation else self.game.room.mobs
        for shuriken in self.shurikens:
            shuriken.update(dt, *self.pos, mobs)

        self.shurikens = list(filter(lambda x: (x.is_orbiting or not x.is_outside)
                                               and not x.hit_the_target, self.shurikens))

    def update_acc(self):
        if not self.moving_right ^ self.moving_left:
            # If the left and right movement keys are not pressed
            # (or are pressed together), acceleration must be opposite
            # to speed in order to slow down the player's movement.
            self.acc_x = -np.sign(self.vel_x) * 0.2 * self.max_acc
        elif abs(self.vel_x) == self.max_vel:
            # If the player has reached maximum speed, he must stop accelerating
            self.acc_x = 0
        else:
            # In normal case acceleration must be co-directional
            # with movement according to the pressed movement key.
            self.acc_x = -self.max_acc if self.moving_left else self.max_acc

        # Same thing with acc_y
        if not self.moving_up ^ self.moving_down:
            self.acc_y = -np.sign(self.vel_y) * 0.2 * self.max_acc
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

    def update_during_transportation(self, dt):
        """Updates player's params during transportation. """
        self.move(self.vel_x * dt, self.vel_y * dt)
        self.update_body(dt)
        self.update_shurikens(dt, True)
        self.gun.update_time(dt)
        if isinstance(self.superpower, Ghost):
            self.superpower.update(dt)
        else:
            self.superpower.update_time(dt)

    def update(self, dt):
        self.update_pos(dt)
        self.superpower.update(dt)
        self.update_body(dt)
        self.update_gun(dt)
        self.update_bullets(dt)
        self.update_homing_bullets(dt)
        self.update_shurikens(dt)

    def draw(self, screen, dx, dy):
        for bullet in self.bullets:
            if bullet.vel == 0:
                bullet.draw(screen, dx, dy)

        self.body.draw(screen, dx, dy)

        for bullet in self.bullets:
            if bullet.vel != 0:
                bullet.draw(screen, dx, dy)

        for bullet in self.homing_bullets:
            bullet.draw(screen, dx, dy)

        for shuriken in self.shurikens:
            shuriken.draw(screen, dx, dy)


__all__ = ["Player"]

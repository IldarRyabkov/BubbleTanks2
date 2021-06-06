import pygame as pg
from math import cos, sin, pi
from numpy import sign
from itertools import chain

from constants import *
from data.player import *

from player_guns import *
from superpowers import *
from special_effects import add_effect
from body import PlayerBody
from data.paths import PLAYER_INJURE

from bullets import *
from base_mob import BaseMob

from utils import *


class Player(BaseMob):
    MAX_ANGULAR_VEL = 0.00024 * pi
    MAX_ANGULAR_ACC = 0.000002

    def __init__(self, game):
        basic_tank = (0, 0)
        (max_health, health_states, radius, body, body_is_rotating, max_vel,
         max_acc, gun_type, bg_radius, superpower) = PLAYER_PARAMS[basic_tank].values()

        super().__init__(SCR_W2, SCR_H2, 0, max_health, health_states, radius, body)
        self.game = game

        self.bg_radius = bg_radius
        self.body = PlayerBody(body, body_is_rotating, self)

        self.max_vel = max_vel
        self.vel_x = self.vel_y = 0
        self.max_acc = max_acc
        self.acc_x = self.acc_y = 0

        self.max_angular_vel = self.MAX_ANGULAR_VEL
        self.max_angular_acc = self.MAX_ANGULAR_ACC
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
        self.gun = get_gun(gun_type, self, game)

        self.bullets = []
        self.mines = []
        self.seekers = []
        self.drones = []
        self.orbital_seekers = []

        self.max_health = max_health
        self.delta_health = 0

        self.tank = basic_tank
        self.tanks_history = [basic_tank]

    @property
    def level(self):
        return self.tank[0]

    @property
    def has_to_upgrade(self) -> bool:
        return self.level < 5 and self.health >= self.max_health

    @property
    def has_to_downgrade(self) -> bool:
        return self.level > 0 and self.health < 0

    @property
    def last_tank_in_history(self) -> bool:
        """ Called when player requests tank upgrade.
        Checks if player's current tank is last in his history of tanks.
        If so, there is a need to open upgrade menu to choose a new tank.
        """
        return self.tank == self.tanks_history[-1]

    @property
    def defeated(self) -> bool:
        return self.health < 0 and self.level == 0

    @property
    def shield_on(self) -> bool:
        return isinstance(self.superpower, Shield) and self.superpower.shield_on

    @property
    def disassembled(self) -> bool:
        return isinstance(self.superpower, Ghost) and self.superpower.disassembled

    def reset(self):
        self.__init__(self.game)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

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
        self.drones = []
        self.seekers = []
        self.bullets = []
        self.mines = []

    def get_mouse_pos(self):
        x, y = pg.mouse.get_pos()
        return self.x + x - SCR_W2, self.y + y - SCR_H2

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
            angle = self.body.get_angle_of_rotation(destination_angle)
            self.angular_acc = sign(angle) * self.max_angular_acc

            self.angular_vel += self.angular_acc * dt
            if abs(self.angular_vel) > self.max_angular_vel:
                self.angular_vel = sign(self.angular_vel) * self.max_angular_vel

            d_angle = self.angular_vel * dt + self.angular_acc * dt*dt/2
            if abs(d_angle) > abs(angle):
                d_angle = angle
                self.angular_vel = 0
                self.angular_acc = 0
            self.body.angle += d_angle
        else:
            self.angular_acc = -sign(self.angular_vel) * self.max_angular_acc * 0.2

            self.angular_vel += self.angular_acc * dt
            if abs(self.angular_vel) > self.max_angular_vel:
                self.angular_vel = sign(self.angular_vel) * self.max_angular_vel
            d_angle = self.angular_vel * dt + self.angular_acc * dt*dt/2
            self.body.angle += d_angle

    def update_body(self, dt):
        if self.body.is_rotating:
            self.rotate_body(dt)
        self.body.update_pos(dt)
        self.body.update_frozen_state(dt)

    def setup(self, max_health, health_states, radius, body, body_is_rotating,
              max_vel, max_acc, gun_type, bg_radius, superpower):

        self.max_vel = max_vel
        self.max_acc = max_acc
        self.max_angular_vel = self.MAX_ANGULAR_VEL
        self.max_angular_acc = self.MAX_ANGULAR_ACC

        self.health = 0
        self.max_health = max_health
        self.health_states = health_states

        self.radius = radius
        self.bg_radius = bg_radius

        self.body = PlayerBody(body, body_is_rotating, self, self.body.is_frozen)
        self.gun = get_gun(gun_type, self, self.game)
        self.orbital_seekers = list(filter(lambda s: not s.is_orbiting, self.orbital_seekers))

        self.superpower = get_superpower(superpower)
        self.superpower.game = self.game
        self.superpower.player = self

    def handle(self, e_type, e_key):
        if e_key == pg.K_a:
            self.moving_left = (e_type == pg.KEYDOWN)
        elif e_key == pg.K_d:
            self.moving_right = (e_type == pg.KEYDOWN)
        elif e_key == pg.K_w:
            self.moving_up = (e_type == pg.KEYDOWN)
        elif e_key == pg.K_s:
            self.moving_down = (e_type == pg.KEYDOWN)
        elif e_key == pg.BUTTON_LEFT:
            self.shooting = (e_type == pg.MOUSEBUTTONDOWN)
        elif e_key == pg.K_SPACE:
            self.superpower.on = (e_type == pg.KEYDOWN)

    def collide_bullet(self, bul_x, bul_y, r):
        radius = self.bg_radius if self.shield_on else self.radius
        return circle_collidepoint(self.x, self.y, radius + r, bul_x, bul_y)

    def collide_bubble(self, x, y):
        return circle_collidepoint(self.x, self.y, self.radius // 2, x, y)

    def handle_injure(self, damage):
        if not self.shield_on:
            super().handle_injure(damage)
            self.delta_health += damage
            self.game.sound_player.play_sound(PLAYER_INJURE, False)

    def handle_bubble_eating(self, bubble_health):
        self.health += bubble_health
        self.delta_health += bubble_health
        self.update_body_look()

    def set_transportation_vel(self, angle, velocity):
        self.vel_x = velocity * cos(angle)
        self.vel_y = -velocity * sin(angle)

    def upgrade(self, tank_is_new: bool, tank=None):
        if tank_is_new:
            self.tanks_history.append(tank)
            self.tank = tank
            self.stop_moving()
            self.shooting = False
        else:
            self.tank = self.tanks_history[self.tank[0] + 1]
        self.setup(*PLAYER_PARAMS[self.tank].values())

    def downgrade(self):
        if self.level > 0:
            self.tank = self.tanks_history[self.level - 1]
            self.setup(*PLAYER_PARAMS[self.tank].values())
            self.health = self.max_health - 1
            self.update_body_look()
        else:
            self.health = 0

    def update_bullets(self, dt):
        for bullet in self.bullets:
            if isinstance(bullet, FrangibleBullet):
                bullet.update(dt, self.bullets)
            else:
                bullet.update(dt)
        self.bullets = list(filter(lambda b: not b.killed, self.bullets))

    def update_mines(self, dt):
        for mine in self.mines:
            mine.update(dt)
        self.mines = list(filter(lambda m: not m.killed, self.mines))[-15:]

    def update_seekers(self, dt):
        if self.game.room.mobs or self.game.room.seekers:
            for seeker in self.seekers:
                seeker.update(dt, targets=chain(self.game.room.mobs, self.game.room.seekers))
                if seeker.killed:
                    add_effect('RedHitCircle', self.game.room.top_effects, seeker.x, seeker.y)
            self.seekers = list(filter(lambda s: not s.killed, self.seekers))
        else:
            for seeker in self.seekers:
                add_effect('RedHitCircle', self.game.room.top_effects, seeker.x, seeker.y)
            self.seekers = []

    def update_drones(self, dt):
        for drone in self.drones:
            drone.update(dt)
        self.drones = list(filter(lambda d: not d.is_divided, self.drones))

    def update_orbital_seekers(self, dt):
        mobs = self.game.room.mobs
        for seeker in self.orbital_seekers:
            seeker.update(dt, self.x, self.y, mobs)
        self.orbital_seekers = list(filter(lambda s: not s.killed, self.orbital_seekers))

    def update_acc(self):
        if not self.moving_right ^ self.moving_left:
            self.acc_x = -sign(self.vel_x) * 0.2 * self.max_acc
        elif self.moving_left:
            self.acc_x = -self.max_acc
        else:
            self.acc_x = self.max_acc

        if not self.moving_up ^ self.moving_down:
            self.acc_y = -sign(self.vel_y) * 0.2 * self.max_acc
        elif self.moving_up:
            self.acc_y = -self.max_acc
        else:
            self.acc_y = self.max_acc

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
            self.vel_x = sign(self.vel_x) * self.max_vel

        self.vel_y += self.acc_y * dt
        if self.vel_y * (self.vel_y - self.acc_y * dt) < 0:
            self.vel_y = 0
        elif abs(self.vel_y) > self.max_vel:
            self.vel_y = sign(self.vel_y) * self.max_vel

    def update(self, dt):
        if self.game.transportation:
            self.move(self.vel_x * dt, self.vel_y * dt)
            self.update_body(dt)
            self.gun.update_time(dt)
            self.superpower.update_during_transportation(dt)
        else:
            self.update_pos(dt)
            self.update_body(dt)
            self.gun.update(dt)
            self.superpower.update(dt)

        self.update_bullets(dt)
        self.update_mines(dt)
        self.update_seekers(dt)
        self.update_drones(dt)
        self.update_orbital_seekers(dt)

    def draw(self, screen, dx, dy):
        for obj in chain(self.mines, (self.body,), self.bullets,
                         self.seekers, self.drones, self.orbital_seekers):
            obj.draw(screen, dx, dy)


__all__ = ["Player"]

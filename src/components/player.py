import pygame as pg
from math import cos, sin, pi, hypot
from itertools import chain

from data.constants import *
from data.player_tanks import PLAYER_TANKS
from assets.paths import PLAYER_HIT

from components.utils import *
from components.superpowers import *
from components.base_mob import BaseMob
from components.player_body import PlayerBody
from components.player_weapons import PlayerWeapons


class Player(BaseMob):
    MAX_ANGULAR_VEL = 0.0002 * pi
    MAX_ANGULAR_ACC = 0.000004
    MAX_ACC = HF(0.0024)
    RESISTANCE = HF(0.00048)

    def __init__(self, game, tank=(0, 0)):
        tank_data = PLAYER_TANKS[tank]

        super().__init__(SCR_W2, SCR_H2, 0, tank_data["max health"], tank_data["radius"],
                         PlayerBody(self, game.rect, tank), PlayerWeapons(self, game, tank))
        self.game = game
        self.camera = game.camera

        self.tank = tank
        self.tanks_history = None

        '''
        Whichever device (mouse or controller) last changed, will hvae control of the player.
        '''
        self.use_controller = False  # used to toggle between mouse/controller
        self.controllerVector = pg.Vector2(0, 0)  # where is the controller pointing, in reference to the player
        self._lastX = 0  # keeps track of last mouse position, to detect changes
        self._lastY = 0

        self.bg_radius = tank_data["background radius"]
        self.max_vel = tank_data["max velocity"]
        k = self.max_vel / HF(0.84)
        self.max_acc = k * self.MAX_ACC
        self.resistance = k * self.RESISTANCE
        self.acc_x = self.acc_y = 0
        self.vel_x = self.vel_y = 0
        rect_size = round(2 * self.radius)
        self.rect.size = rect_size, rect_size

        self.max_angular_vel = self.MAX_ANGULAR_VEL
        self.max_angular_acc = k * self.MAX_ANGULAR_ACC
        self.angular_vel = 0
        self.angular_acc = self.max_angular_acc

        self.max_cumulative_health = 0
        self.prev_cumulative_health = 0

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.shooting = False

        self.superpower = get_superpower(tank, game, self)

        self.bullets = []
        self.mines = []
        self.seekers = []
        self.drones = []
        self.orbital_seekers = []

        self.killed = False
        self.update_component_states()

    @property
    def is_outside(self):
        return hypot(*self.camera.offset) > ROOM_RADIUS

    @property
    def level(self) -> int:
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
        Checks if player's current tank state is last in his history of tank states.
        If so, there is a need to open upgrade menu to choose a new tank.
        """
        return self.tank == self.tanks_history[-1]

    @property
    def shield_on(self) -> bool:
        return isinstance(self.superpower, Shield) and self.superpower.shield_on

    @property
    def disassembled(self) -> bool:
        return isinstance(self.superpower, Disassemble) and self.superpower.disassembled

    @property
    def cumulative_health(self):
        if self.level == 0:
            return self.health
        if self.level == 1:
            return 75 + self.health
        if self.level == 2:
            return 200 + self.health
        if self.level == 3:
            return 400 + self.health
        if self.level == 4:
            return 800 + self.health
        return 1300 + self.health

    @property
    def health_change(self):
        return self.prev_cumulative_health - self.cumulative_health

    @property
    def is_help_needed(self):
        return self.cumulative_health < 0.8 * self.max_cumulative_health

    def set_save_data(self, save_data: dict):
        """Sets save data loaded from save file. """
        tank = tuple(save_data["tank"])
        self.__init__(self.game, tank)
        self.tanks_history = [tuple(tank) for tank in save_data["tanks history"]]
        self.set_health(save_data["health"])
        self.max_cumulative_health = save_data["max cumulative health"]
        self.prev_cumulative_health = self.cumulative_health

    def update_component_states(self):
        if self.level == 5:
            state = 0
        elif self.health > self.max_health:
            state = self.max_health
        elif self.health < 0:
            state = 0
        else:
            state = self.health

        self.body.update_state(state)
        self.weapons.update_state(state)
        self.superpower.update_state(state)

    def decrease_speed(self):
        k = 0.25
        self.max_vel *= k
        self.max_acc *= k
        self.max_angular_vel *= k
        self.max_angular_acc *= k

    def become_sticky(self):
        if not self.sticky:
            self.decrease_speed()
        super().become_sticky()

    def stop_being_sticky(self):
        k = 4
        self.max_vel *= k
        self.max_acc *= k
        self.max_angular_vel *= k
        self.max_angular_acc *= k
        super().stop_being_sticky()

    def move(self, dx, dy, dt=0):
        super().move(dx, dy)
        self.camera.update(self.x, self.y, dt)

    def stop_moving(self):
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def set_params_after_transportation(self):
        self.vel_x = 0
        self.vel_y = 0
        self.health = max(self.health, 0)
        self.prev_cumulative_health = self.cumulative_health
        self.drones.clear()
        self.seekers.clear()
        self.bullets.clear()
        self.mines.clear()

    def get_mouse_pos(self):
        x, y = pg.mouse.get_pos()
        if self._lastX != x or self._lastY != y:
            self.use_controller = False  # switch to mouse
            self._lastX = x
            self._lastY = y

        if self.use_controller is False:
            return self.x + x - SCR_W2, self.y + y - SCR_H2
        else:  # use controller
            return (self.controllerVector * 10) + pg.Vector2((self.x, self.y))

    def rotate_body(self, dt):
        """Rotates player's tank body according to its movement."""
        if not self.body.is_rotating:
            return

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

            d_angle = self.angular_vel * dt + self.angular_acc * dt * dt / 2
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
            d_angle = self.angular_vel * dt + self.angular_acc * dt * dt / 2
            self.body.angle += d_angle

    def update_shape(self, dt):
        self.body.update_shape(dt)
        self.weapons.update_shape(dt)

    def set_params(self, upgrade: bool):
        """Method is called when player is being upgraded/downgraded.
        Sets new player's parameters according to tank state.
        """
        data = PLAYER_TANKS[self.tank]

        self.radius = data["radius"]
        self.bg_radius = data["background radius"]
        rect_size = round(2 * self.radius)
        self.rect.size = rect_size, rect_size

        self.max_health = data["max health"]
        self.health = 0 if upgrade else self.max_health - 1

        self.max_vel = data["max velocity"]
        self.max_angular_vel = self.MAX_ANGULAR_VEL
        k = self.max_vel / HF(0.84)
        self.max_acc = k * self.MAX_ACC
        self.resistance = k * self.RESISTANCE
        self.max_angular_acc = k * self.MAX_ANGULAR_ACC
        if self.sticky:
            self.decrease_speed()

        self.body.set_params(self.tank)
        self.weapons.set_params(self.tank)
        self.superpower = get_superpower(self.tank, self.game, self)
        self.update_component_states()

        self.orbital_seekers = list(filter(lambda s: not s.orbiting, self.orbital_seekers))

    def handle(self, e_type, e_key):
        print('player.handle(', e_type, e_key)
        if e_key == self.game.controls["left"]:
            self.moving_left = (e_type == pg.KEYDOWN)
        elif e_key == self.game.controls["right"]:
            self.moving_right = (e_type == pg.KEYDOWN)
        elif e_key == self.game.controls["up"]:
            self.moving_up = (e_type == pg.KEYDOWN)
        elif e_key == self.game.controls["down"]:
            self.moving_down = (e_type == pg.KEYDOWN)
        elif e_key == pg.BUTTON_LEFT:
            self.shooting = (e_type == pg.MOUSEBUTTONDOWN)
        elif e_key == self.game.controls["superpower"]:
            self.superpower.on = (e_type == pg.KEYDOWN)

    def collide_bullet(self, bullet):
        if self.shield_on:
            return circle_collidepoint(self.x, self.y, self.bg_radius + bullet.radius, bullet.x, bullet.y)
        return super().collide_bullet(bullet)

    def collide_bubble(self, bubble):
        return circle_collidepoint(self.x, self.y, self.radius * 0.5, bubble.x, bubble.y)

    def update_health(self, delta_health: int):
        self.health += delta_health
        self.update_component_states()
        self.max_cumulative_health = max(self.max_cumulative_health, self.cumulative_health)

    def receive_damage(self, damage, play_sound=True):
        if self.shield_on:
            return
        super().receive_damage(damage)
        if play_sound:
            self.game.sound_player.play_sound(PLAYER_HIT)

    def set_transportation_vel(self, angle, velocity):
        self.vel_x = velocity * cos(angle)
        self.vel_y = -velocity * sin(angle)

    def upgrade(self, tank_is_new: bool, tank=None):
        if tank_is_new:
            self.tank = tank
            self.tanks_history.append(tank)
            self.stop_moving()
            self.shooting = False
        else:
            self.tank = self.tanks_history[self.level + 1]
        self.set_params(upgrade=True)

    def downgrade(self):
        self.tank = self.tanks_history[self.level - 1]
        self.set_params(upgrade=False)

    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)
        self.bullets = list(filter(lambda b: not b.killed, self.bullets))

    def update_mines(self, dt):
        for mine in self.mines:
            mine.update(dt)
        self.mines = list(filter(lambda m: not m.killed, self.mines))[-30:]

    def update_seekers(self, dt):
        for seeker in self.seekers:
            seeker.update(dt)
        self.seekers = list(filter(lambda s: not s.killed, self.seekers))

    def update_drones(self, dt):
        for drone in self.drones:
            drone.update(dt)
        self.drones = list(filter(lambda d: not d.killed, self.drones))

    def update_orbital_seekers(self, dt):
        for seeker in self.orbital_seekers:
            seeker.update(dt)
        self.orbital_seekers = list(filter(lambda s: s.orbiting, self.orbital_seekers))

    def update_acc(self):
        if not self.moving_right ^ self.moving_left:
            self.acc_x = -sign(self.vel_x) * self.resistance
        elif self.moving_left:
            self.acc_x = -self.max_acc
        else:
            self.acc_x = self.max_acc

        if not self.moving_up ^ self.moving_down:
            self.acc_y = -sign(self.vel_y) * self.resistance
        elif self.moving_up:
            self.acc_y = -self.max_acc
        else:
            self.acc_y = self.max_acc

    def update_pos(self, dt):
        self.update_acc()
        self.update_vel(dt)
        dx = self.vel_x * dt + self.acc_x * dt * dt / 2
        dy = self.vel_y * dt + self.acc_y * dt * dt / 2
        self.move(dx, dy, dt)

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
        self.update_sticky_state(dt)

        if self.game.transportation:
            self.move(self.vel_x * dt, self.vel_y * dt, dt)
            self.rotate_body(dt)
            self.update_shape(dt)
            self.weapons.update_time(dt)
            self.superpower.update_during_transportation(dt)
        else:
            self.update_pos(dt)
            self.rotate_body(dt)
            self.update_shape(dt)
            self.weapons.update_shooting(dt)
            self.superpower.update(dt)

        self.update_bullets(dt)
        self.update_mines(dt)
        self.update_seekers(dt)
        self.update_drones(dt)
        self.update_orbital_seekers(dt)

    def draw(self, screen, dx=0, dy=0):
        for obj in chain(self.mines, (self.body, self.weapons), self.bullets,
                         self.seekers, self.drones, self.orbital_seekers):
            obj.draw(screen, dx, dy)


__all__ = ["Player"]

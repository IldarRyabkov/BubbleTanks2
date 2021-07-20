from math import cos, sin, hypot, pi
from random import uniform
from itertools import chain


from components.circle import make_circles_list
from data.guns import GUNS
from data.shapes import SHAPES
from data.constants import *
from assets.paths import SHOOT
from components.utils import *
from components.bullets import *
from data.player_tanks import PLAYER_TANKS


class PlayerWeapons:
    def __init__(self, player, game, tank):
        self.player = player
        self.game = game
        self.state = 0

        self.guns = dict()
        self.auto_guns = dict()
        self.init_guns(tank)

        self.cooldown = PLAYER_TANKS[tank]["cooldown"]
        self.cooldown_auto = PLAYER_TANKS[tank]["cooldown auto"]
        self.time = self.cooldown
        self.time_auto = self.cooldown_auto
        self.sticky_shape = make_circles_list(game.rect, SHAPES["sticky"])

    @property
    def current_guns(self):
        return self.guns[self.state]

    @property
    def current_auto_guns(self):
        return self.auto_guns[self.state]

    def set_params(self, tank):
        self.init_guns(tank)
        self.cooldown = PLAYER_TANKS[tank]["cooldown"]
        self.cooldown_auto = PLAYER_TANKS[tank]["cooldown auto"]
        self.time = self.cooldown
        self.time_auto = self.cooldown_auto

    def make_gun(self, data):
        gun_params = GUNS[data["name"]]
        distance = HF(data["distance"])
        angle = data["angle"]
        emitter_offset = HF(gun_params["emitter offset"])
        circles_data = gun_params["circles"]
        rotation_type = data["rotation type"]
        shooting_type = data["shooting type"]
        bullet_type = gun_params["bullet type"]
        bullet_name = data["bullet name"]
        bullet_vel = HF(data["bullet velocity"])
        bullet_dmg = data["bullet damage"]
        scale = data["scale"]
        return Gun(self.player, self.game.rect, distance, angle, emitter_offset,
                   circles_data, rotation_type, shooting_type, bullet_type,
                   bullet_name, bullet_vel, bullet_dmg, scale)

    def init_guns(self, tank):
        self.guns = dict()
        self.auto_guns = dict()
        guns_list = [self.make_gun(data) for data in PLAYER_TANKS[tank]["guns"]]
        states = PLAYER_TANKS[tank]["guns states"]
        for (left, right), indexes in states.items():
            for state in range(left, right + 1):
                self.guns[state] = [guns_list[i] for i in indexes if guns_list[i].rotation_type != AUTO_GUN]
                self.auto_guns[state] = [guns_list[i] for i in indexes if guns_list[i].rotation_type == AUTO_GUN]

    def update_state(self, state):
        self.state = state

    def update_time(self, dt):
        self.time += dt
        self.time_auto += dt

    def update_shape(self, dt):
        """Updates appearance of player's primary weapons. """
        x, y, body_angle = self.player.x, self.player.y, self.player.body.angle
        mouse_pos = self.player.get_mouse_pos()

        for gun in self.current_guns:
            gun.update_shape(x, y, dt, body_angle, mouse_pos)

        if self.current_auto_guns:
            target = None
            if self.game.room.mobs or self.game.room.seekers:
                target = min(chain(self.game.room.mobs, self.game.room.seekers),
                             key=lambda m: hypot(x - m.x, y - m.y))
            for gun in self.current_auto_guns:
                gun.update_shape(x, y, dt, body_angle, target)

    def update_shooting(self, dt):
        self.update_time(dt)
        if self.current_auto_guns and self.time_auto >= self.cooldown_auto and self.game.room.mobs:
            self.time_auto = 0
            self.shoot_auto()
        if self.time >= self.cooldown and self.player.shooting and not self.player.disassembled:
            self.time = 0
            self.shoot()

    def shoot(self):
        for gun in self.current_guns:
            gun.shoot()
        self.game.sound_player.play_sound(SHOOT)

    def shoot_auto(self):
        for gun in self.current_auto_guns:
            gun.shoot()
        self.game.sound_player.play_sound(SHOOT)

    def update(self, dt):
        self.update_shape(dt)
        self.update_shooting(dt)

    def draw_sticky_shape(self, screen):
        angle = self.player.body.angle
        for circle in self.sticky_shape:
            circle.update(SCR_W2, SCR_H2, 0, angle)
            circle.draw(screen)

    def draw(self, screen, dx=0, dy=0):
        for gun in self.current_guns:
            gun.draw(screen, dx, dy)
        for gun in self.current_auto_guns:
            gun.draw(screen, dx, dy)
        if self.player.sticky:
            self.draw_sticky_shape(screen)


class Gun:
    def __init__(self, player, screen_rect, distance, angle, emitter_offset,
                 circles_data, rotation_type, shooting_type, bullet_type,
                 bullet_name, bullet_vel, bullet_dmg, scale):

        self.player = player
        self.screen_rect = screen_rect
        self.x = 0
        self.y = 0
        self.distance = distance
        self.angle = angle
        self.angle_to_target = 0
        self.emitter_offset = emitter_offset * scale

        self.circles = make_circles_list(screen_rect, circles_data, scale)
        self.rotation_type = rotation_type
        self.shoot = self.get_shooting_func(shooting_type)

        self.bullet = get_bullet_type(bullet_type)
        self.bullet_is_custom = self.bullet in (PierceShot, ExplosivePierceShot, LeecherBullet)
        self.bullet_name = bullet_name
        self.bullet_vel = bullet_vel
        self.bullet_dmg = bullet_dmg

    def make_bullet(self, x, y, angle):
        if self.bullet_is_custom:
            return self.bullet(self.screen_rect, x, y, self.bullet_dmg, self.bullet_vel, angle)
        return self.bullet(self.bullet_name, self.screen_rect, x, y,
                           self.bullet_dmg, self.bullet_vel, angle)

    def get_shooting_func(self, shooting_type):
        if shooting_type == "single":
            return self.shoot_single
        if shooting_type == "2 small parallel":
            return self.shoot_2_small_parallel
        if shooting_type == "2 medium parallel":
            return self.shoot_2_medium_parallel
        if shooting_type == "3 small parallel":
            return self.shoot_3_small_parallel
        if shooting_type == "5 small parallel":
            return self.shoot_5_small_parallel
        if shooting_type == "3 spread":
            return self.shoot_3_spread
        if shooting_type == "5 spread":
            return self.shoot_5_spread
        if shooting_type == "drone":
            return self.shoot_drone
        if shooting_type == "superpower":
            return lambda: None

    def shoot_single(self):
        x = self.x + self.emitter_offset * cos(self.angle_to_target)
        y = self.y - self.emitter_offset * sin(self.angle_to_target)
        bullet = self.make_bullet(x, y, self.angle_to_target)
        self.player.bullets.append(bullet)

    def shoot_2_small_parallel(self):
        angle = self.angle_to_target
        sina, cosa = sin(angle), cos(angle)
        x = self.x + self.emitter_offset * cosa
        y = self.y - self.emitter_offset * sina
        dx = HF(9) * sina
        dy = HF(9) * cosa
        for k in (-1, 1):
            bullet = self.make_bullet(x + k * dx, y + k * dy, angle)
            self.player.bullets.append(bullet)

    def shoot_2_medium_parallel(self):
        angle = self.angle_to_target
        sina, cosa = sin(angle), cos(angle)
        x = self.x + self.emitter_offset * cosa
        y = self.y - self.emitter_offset * sina
        dx = HF(18) * sina
        dy = HF(18) * cosa
        for k in (-1, 1):
            bullet = self.make_bullet(x + k * dx, y + k * dy, angle)
            self.player.bullets.append(bullet)

    def shoot_3_spread(self):
        for k in (-1, 0, 1):
            angle = self.angle_to_target + k * 0.255*pi
            x = self.x + self.emitter_offset * cos(angle)
            y = self.y - self.emitter_offset * sin(angle)
            bullet = self.make_bullet(x, y, self.angle_to_target + k * 0.167*pi)
            self.player.bullets.append(bullet)

    def shoot_5_spread(self):
        angle_to_target = self.angle_to_target
        delta_angle_1 = 0.056 * pi
        delta_angle_2 = 0.156 * pi
        for k in (-2, -1, 0, 1, 2):
            angle = angle_to_target + k * delta_angle_2
            x = self.x + self.emitter_offset * cos(angle)
            y = self.y - self.emitter_offset * sin(angle)
            bullet = self.make_bullet(x, y, angle_to_target + k * delta_angle_1)
            self.player.bullets.append(bullet)

    def shoot_3_small_parallel(self):
        angle = self.angle_to_target
        sina, cosa = sin(angle), cos(angle)
        x = self.x + self.emitter_offset * cosa
        y = self.y - self.emitter_offset * sina
        dx = HF(19) * sina
        dy = HF(19) * cosa
        for k in (-1, 0, 1):
            bullet = self.make_bullet(x + k * dx, y + k * dy, angle)
            self.player.bullets.append(bullet)

    def shoot_5_small_parallel(self):
        angle = self.angle_to_target
        sina, cosa = sin(angle), cos(angle)
        x = self.x + self.emitter_offset * cosa
        y = self.y - self.emitter_offset * sina
        dx1, dy1 = HF(19) * sina, HF(19) * cosa
        dx2, dy2 = HF(38) * sina, HF(38) * cosa
        dx3, dy3 = HF(5) * cosa, HF(5) * sina
        for dx, dy in (0, 0), (dx1, dy1), (-dx1, -dy1), (dx2-dx3, dy2+dy3), (-dx2-dx3, -dy2+dy3):
            bullet = self.make_bullet(x + dx, y + dy, angle)
            self.player.bullets.append(bullet)

    def shoot_drone(self):
        x = self.x + self.emitter_offset * cos(self.angle_to_target)
        y = self.y - self.emitter_offset * sin(self.angle_to_target)
        drone = Drone(self.bullet_name, self.screen_rect, x, y, self.bullet_dmg,
                      self.bullet_vel, uniform(0, 2 * pi), self.player)
        drone.update(0)
        self.player.drones.append(drone)

    def shoot_mine(self):
        x = self.x + self.emitter_offset * cos(self.angle_to_target)
        y = self.y - self.emitter_offset * sin(self.angle_to_target)
        mine = self.make_bullet(x, y, self.angle_to_target)
        self.player.mines.append(mine)

    def predicted_angle(self, target):
        if target.sticky or target.stunned:
            return calculate_angle(self.x, self.y, target.x, target.y)
        time = (hypot(self.x - target.x, self.y - target.y) - self.emitter_offset) / self.bullet_vel
        x = target.x + target.vel_x * time
        y = target.y + target.vel_y * time
        return calculate_angle(self.x, self.y, x, y)

    def update_shape(self, xo, yo, dt, body_angle, target):
        x = xo + self.distance * cos(self.angle + body_angle)
        y = yo - self.distance * sin(self.angle + body_angle)
        self.x, self.y = x, y

        if self.rotation_type == FIXED_GUN:
            self.angle_to_target = body_angle
        elif self.rotation_type == AUTO_GUN:
            if target is not None:
                self.angle_to_target = self.predicted_angle(target)
        else:
            self.angle_to_target = calculate_angle(x, y, *target)

        angle_to_target = self.angle_to_target
        for circle in self.circles:
            circle.update(x, y, dt, angle_to_target)

    def draw(self, screen, dx=0, dy=0):
        for circle in self.circles:
            circle.draw(screen, dx, dy)


__all__ = ["PlayerWeapons"]

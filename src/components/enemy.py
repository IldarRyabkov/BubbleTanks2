from random import uniform
from math import pi, cos, sin, hypot
import pygame as pg

from assets.paths import *
from data.constants import *
from data.enemies import ENEMIES

from components.utils import *
from components.base_mob import BaseMob
from components.enemy_body import EnemyBody
from components.enemy_weapons import EnemyWeapons
from components.enemy_event import EnemyEvent
from components.special_effects import infection_surfaces


sticky_w = H(108.391)
sticky_h = H(99.248)
sticky_image = pg.image.load(STICKY_IMAGE).convert_alpha()
sticky_image = pg.transform.smoothscale(sticky_image, (sticky_w, sticky_h))


class Enemy(BaseMob):
    def __init__(self, game, name):
        self.name = name
        data = ENEMIES[name]
        super().__init__(*self.start_pos(), data["max health"], data["max health"],
                         data["radius"], EnemyBody(self, game.rect, data), EnemyWeapons(self, game, data))
        self.game = game
        self.death_award = data["death award"]
        self.screen_rect = game.rect
        self.rect = pg.Rect(0, 0, data["rect size"], data["rect size"])
        self.rect.center = self.x, self.y
        self.update_component_states()
        self.events = [EnemyEvent(self, game, event_data) for event_data in data["events"]]
        self.velocity = data["velocity"]
        self.vel_x = 0
        self.vel_y = 0
        self.body.angle = uniform(0, 2*pi) if self.velocity != 0 else 0
        self.set_velocity()
        self.angle_to_turn = 0
        self.last_angle = 0
        self.safety_turn = False
        self.time_to_turn = 0
        self.time_to_hold_turning = 0
        self.spawners_data = data["spawners"]
        self.killed = False
        self.chasing_infectors = set()

        self.infected = False
        self.infection_time = 0
        self.infection_cooldown = 170
        self.infection_effect_time = 0

    @property
    def is_on_screen(self):
        return self.rect.colliderect(self.screen_rect)

    @property
    def about_to_exit(self):
        if self.velocity == 0:
            return False
        distance = self.rect.w/2 + HF(132)
        x = self.x + distance * self.vel_x / self.velocity
        y = self.y + distance * self.vel_y / self.velocity
        return hypot(x - SCR_W2, y - SCR_H2) > ROOM_RADIUS

    @staticmethod
    def start_pos():
        distance = uniform(0, ROOM_RADIUS * 0.7)
        angle = uniform(0, 2*pi)
        x = SCR_W2 + distance * cos(angle)
        y = SCR_H2 - distance * sin(angle)
        return x, y

    def update_health(self, delta_health: int):
        self.health = min(self.max_health, self.health + delta_health)
        self.update_component_states()
        if self.health <= 0:
            self.killed = True

    def become_infected(self):
        if not self.infected:
            self.infected = True
            self.body.become_infected()
            self.weapons.become_infected()

    def update_infected_state(self, dt):
        if self.infected:
            self.infection_time += dt
            if self.infection_time >= self.infection_cooldown:
                self.receive_damage(-1, play_sound=False)
                self.infection_time = 0

    def get_angle_pos(self):
        return calculate_angle(SCR_W2, SCR_H2, self.x, self.y)

    def set_velocity(self):
        self.vel_x = self.velocity * cos(self.body.angle)
        self.vel_y = -self.velocity * sin(self.body.angle)

    def move(self, dx, dy):
        super().move(dx, dy)
        self.rect.center = self.x, self.y

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = x, y

    def move_by_time(self, dt):
        self.move(self.vel_x * dt, self.vel_y * dt)

    def update_angle(self, delta_angle):
        self.body.angle += delta_angle
        self.set_velocity()

    def update_pos(self, dt):
        if self.stunned or self.sticky:
            return
        last_angle_pos = self.get_angle_pos()
        self.move_by_time(dt)
        if self.velocity == 0:
            self.weapons.update_pos()
            return
        about_to_exit = self.about_to_exit
        if self.time_to_turn == 0 or (about_to_exit and not self.safety_turn):
            if about_to_exit:
                angle_pos = self.get_angle_pos()
                angle_to_turn = uniform(-pi, -pi/2)
                if angle_pos > last_angle_pos:
                    angle_to_turn *= -1
                k = HF(2.4 * 180 / pi)
                self.time_to_turn = abs(angle_to_turn) / self.velocity * k
                self.angle_to_turn = self.velocity * sign(angle_to_turn) / k
                self.time_to_hold_turning = 1800
                self.safety_turn = True
        else:
            self.time_to_turn = max(0, self.time_to_turn - dt)
            self.update_angle(self.angle_to_turn * dt)

        if self.time_to_hold_turning > 0:
            self.time_to_hold_turning -= dt
        elif self.time_to_turn == 0:
            if dt != 0 and uniform(0, 1000/dt) < 1:
                distance = uniform(-100, 100)
                k = HF(2.4)
                self.time_to_turn = abs(distance) / self.velocity * k
                self.angle_to_turn = self.velocity * sign(distance) / k * pi/180
                self.safety_turn = False
        self.weapons.update_pos()

    def update_shape(self, dt):
        if self.is_on_screen:
            self.body.update_shape(dt)
            self.weapons.update_shape(dt)
            self.infection_effect_time += dt
            self.infection_effect_time %= 320

    def update_shooting(self, dt):
        if not self.stunned:
            self.weapons.update_shooting(dt)

    def receive_damage(self, damage, play_sound=True):
        super().receive_damage(damage)
        for event in self.events:
            if self.health <= event.trigger_value and not event.hit or event.trigger_value == -1:
                event.hit = True
                event.action()
        if self.killed:
            self.game.sound_player.play_sound(ENEMY_DEATH)
            self.game.pause_menu.update_counter(0, 1)
        elif play_sound:
            self.game.sound_player.play_sound(ENEMY_HIT)

    def update(self, dt):
        self.update_sticky_state(dt)
        self.update_stunned_state(dt)
        self.update_infected_state(dt)
        self.update_pos(dt)
        self.update_shape(dt)
        self.update_shooting(dt)

    def draw_sticky(self, screen, dx, dy):
        x = self.x - dx - sticky_w/2
        y = self.y - dy - sticky_h/2
        screen.blit(sticky_image, (x, y))

    def draw_infected(self, screen, dx, dy):
        index = int(17 * self.infection_effect_time/320)
        if 9 <= index <= 15:
            surface = infection_surfaces[index - 9]
            x = self.x - dx - surface.get_width()/2
            y = self.y - dy - surface.get_height()/2
            screen.blit(surface, (x, y))

    def draw(self, screen, dx=0, dy=0):
        if self.is_on_screen:
            self.body.draw(screen, dx, dy)
            self.weapons.draw(screen, dx, dy)
            if self.sticky:
                self.draw_sticky(screen, dx, dy)
            if self.infected:
                self.draw_infected(screen, dx, dy)


class BossHead(Enemy):
    def __init__(self, game, name):
        super().__init__(game, name)
        self.body.angle = -0.5 * pi
        self.delta_angle = 0
        self.target = game.player
        self.rect_offset = HF(192.575)

    @staticmethod
    def start_pos():
        return SCR_W2, -HF(480)

    def collide_bullet(self, bul_x, bul_y, bul_r) -> bool:
        return circle_collidepoint(*self.rect.center, self.radius + bul_r, bul_x, bul_y)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.centerx = self.x + self.rect_offset * cos(self.body.angle)
        self.rect.centery = self.y - self.rect_offset * sin(self.body.angle)

    def update_pos(self, dt):
        if self.sticky or self.stunned:
            return
        angle = calculate_angle(self.x, self.y, self.target.x, self.target.y) + 0.5 * pi
        if angle > pi:
            angle = -angle + 0.5 * pi
        if angle > self.delta_angle:
            self.delta_angle = min(angle, self.delta_angle + 0.00072 * dt, 0.23 * pi)
        else:
            self.delta_angle = max(angle, self.delta_angle - 0.00072 * dt, -0.23 * pi)
        self.body.angle = -0.5 * pi + self.delta_angle
        self.rect.centerx = self.x + self.rect_offset * cos(self.body.angle)
        self.rect.centery = self.y - self.rect_offset * sin(self.body.angle)
        self.weapons.update_pos()


class BossLeg(Enemy):
    def __init__(self, game, name):
        super().__init__(game, name)
        self.body.angle = 0.5 * pi
        self.rect_offset = HF(124.374)
        self.rect.centerx = self.x + self.rect_offset * cos(self.body.angle)
        self.rect.centery = self.y - self.rect_offset * sin(self.body.angle)
        self.weapons.update_pos()

    @staticmethod
    def start_pos():
        return SCR_W2, HF(1280)

    def collide_bullet(self, bul_x, bul_y, bul_r) -> bool:
        return circle_collidepoint(*self.rect.center, self.radius + bul_r, bul_x, bul_y)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.centerx = self.x + self.rect_offset * cos(self.body.angle)
        self.rect.centery = self.y - self.rect_offset * sin(self.body.angle)
        self.weapons.update_pos()

    def update_pos(self, dt):
        pass


class BossHand(Enemy):
    def __init__(self, game, name):
        super().__init__(game, name)
        if self.name == "BossLeftHand":
            self.body.angle = -0.2 * pi
        else:
            self.body.angle = -0.8 * pi

    def start_pos(self):
        if self.name == "BossLeftHand":
            return SCR_W2 - HF(600), -HF(80)
        return SCR_W2 + HF(600), -HF(80)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.center = self.x, self.y
        self.weapons.update_pos()

    def update_pos(self, dt):
        self.weapons.update_pos()


def make_enemy(game, name):
    if name == "BossHead":
        return BossHead(game, name)
    if name == "BossLeg":
        return BossLeg(game, name)
    if name in ("BossLeftHand", "BossRightHand"):
        return BossHand(game, name)
    return Enemy(game, name)


__all__ = ["Enemy", "make_enemy"]

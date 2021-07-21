from math import cos, sin, pi, hypot
from random import uniform
import pygame as pg
from itertools import chain

from assets.paths import ENEMY_DEATH
from data.constants import *
from data.bullets import BULLETS
from components.special_effects import add_effect
from components.simple_body import Body
from components.utils import *
from components.special_effects import sapper_surfaces


class Bullet:
    """ a parent class for all bullets classes """
    def __init__(self, name, screen_rect, x, y, damage, vel, angle):
        self.x = x
        self.y = y

        self.angle = angle
        self.radius = BULLETS[name]["radius"]

        rect_size = BULLETS[name]["size"]
        self.rect = pg.Rect(0, 0, rect_size, rect_size)
        self.rect.center = x, y
        self.screen_rect = screen_rect

        self.VELOCITY = vel
        self.vel_x = vel * cos(angle)
        self.vel_y = -vel * sin(angle)

        self.damage = damage
        self.hit_effect = BULLETS[name]["hit effect"]
        self.killed = False

        body_data = BULLETS[name]["circles"]
        if isinstance(body_data, pg.Surface):
            self.body = body_data
        else:
            self.body = Body(self, screen_rect, body_data)

    @property
    def is_outside(self):
        return not circle_collidepoint(SCR_W2, SCR_H2, ROOM_RADIUS, self.x, self.y)

    @property
    def is_on_screen(self):
        return self.rect.colliderect(self.screen_rect)

    def update_vel(self, angle):
        self.vel_x = self.VELOCITY * cos(angle)
        self.vel_y = -self.VELOCITY * sin(angle)

    def update_pos(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.rect.center = self.x, self.y
        if self.is_outside:
            self.killed = True

    def update_body(self, dt):
        if self.is_on_screen:
            self.body.update_shape(dt)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.center = self.x, self.y

    def draw(self, surface, dx, dy):
        if self.is_on_screen:
            self.body.draw(surface, dx, dy)


class RegularBullet(Bullet):
    """ A bullet with uniform rectilinear motion """
    def __init__(self, name, screen_rect, x, y, damage, vel, angle):
        super().__init__(name, screen_rect, x, y, damage, vel, angle)

    def update_color(self, dt):
        pass

    def update(self, dt):
        self.update_pos(dt)
        self.update_body(dt)


class ExplodingBullet(RegularBullet):
    """
     Bullet moves evenly and rectilinearly and explodes
     from contact with the enemy, damaging others.

    """
    def __init__(self, screen_rect, x, y, angle):
        super().__init__("big light red", screen_rect, x, y, -21, HF(1.1), angle)
        self.hit_effect = 'DamageBurstLarge'
        self.colors = {1: LIGHT_RED, -1: LIGHT_RED_2}
        self.color_switch = 1
        self.T = 80
        self.color_time = 0
        self.explosion_radius = H(600)

    def change_color(self):
        self.color_switch *= -1
        self.body.circles[0].color = self.colors[self.color_switch]

    def update(self, dt):
        super().update(dt)
        self.color_time += dt
        if self.color_time >= 0.75 * self.T and self.color_switch == 1:
            self.change_color()
        elif self.color_time >= self.T and self.color_switch == -1:
            self.change_color()
            self.color_time -= self.T


class Mine(Bullet):
    """Mine doesn't move and deals damage to a tank that moved too close. """
    def __init__(self, name, screen_rect, x, y, damage, vel, angle):
        super().__init__(name, screen_rect, x, y, damage, vel, angle)

        self.body.rotate(uniform(0, 2 * pi))
        self.body.update_shape(0)
        self.colors = {1: self.body.circles[0].color, -1: LIGHT_RED_2}
        self.color_switch = 1
        self.T = 240
        self.color_time = uniform(0, self.T)

    def update_body(self, dt):
        self.color_time += dt
        if self.color_time >= 0.75 * self.T and self.color_switch == 1:
            self.change_color()
        elif self.color_time >= self.T and self.color_switch == -1:
            self.change_color()
            self.color_time = 0

    def change_color(self):
        self.color_switch *= -1
        self.body.circles[0].color = self.colors[self.color_switch]

    def update(self, dt):
        self.update_body(dt)


class AllyOrbitalSeeker(Bullet):
    """
    Bullet has two states: 'orbiting', when it rotates around the player;
                           'not orbiting', when it moves as a regular bullet.
    Initially bullet is orbiting. If some target intersects with bullet's searching area,
    bullet starts moving evenly and rectilinearly to a target's position.

    """
    def __init__(self, game, screen_rect, x, y):
        super().__init__("orbital seeker", screen_rect, x, y, -5, HF(1.68), 0)
        self.game = game
        self.owner = game.player
        self.orbiting = True
        self.orbiting_radius = HF(128)
        self.orbiting_angle = 0
        self.search_radius = HF(260)

    def update_pos(self, dt):
        if self.orbiting:
            self.orbiting_angle -= 0.006 * dt
            self.x = self.owner.x + self.orbiting_radius * cos(self.orbiting_angle)
            self.y = self.owner.y - self.orbiting_radius * sin(self.orbiting_angle)
            self.rect.center = self.x, self.y
        else:
            super().update_pos(dt)

    def check_targets(self):
        for enemy in chain(self.game.room.mobs, self.game.room.seekers):
            if enemy.collide_bullet(self.x, self.y, self.search_radius):
                self.orbiting = False
                predicted_time = hypot(self.x - enemy.x, self.y - enemy.y) / self.VELOCITY
                x = enemy.x + enemy.vel_x * predicted_time
                y = enemy.y + enemy.vel_y * predicted_time
                angle = calculate_angle(self.x, self.y, x, y)
                self.update_vel(angle)
                self.owner.bullets.append(self)
                break

    def update(self, dt):
        self.update_pos(dt)
        self.update_body(dt)
        if self.orbiting:
            self.check_targets()


class Seeker(Bullet):
    """ A bullet which moves with constant velocity and follows a moving target.
        Therefore, the x- and y-components of velocity are changing. """
    def __init__(self, game, name, screen_rect, x, y, start_angle, rotation_speed, damage, vel):
        super().__init__(name, screen_rect, x, y, damage, vel, start_angle)
        self.game = game
        self.rotation_speed = rotation_speed
        self.target = None

    def collide_bullet(self, bul_x, bul_y, bul_r):
        return circle_collidepoint(self.x, self.y, self.radius + bul_r, bul_x, bul_y)

    def receive_damage(self, damage):
        self.killed = True

    def closest_target(self, targets):
        return min(targets, key=lambda t: hypot(self.x - t.x, self.y - t.y))

    def update_angle(self, dt):
        if self.target is None:
            return
        angle_to_target = calculate_angle(self.x, self.y, self.target.x, self.target.y)
        if abs(angle_to_target - self.angle) > pi:
            if angle_to_target > self.angle:
                rotation = -self.rotation_speed * dt
            else:
                rotation = self.rotation_speed * dt
        else:
            if angle_to_target > self.angle:
                rotation = min(angle_to_target - self.angle, self.rotation_speed*dt)
            else:
                rotation = max(angle_to_target - self.angle, -self.rotation_speed*dt)
        self.angle += rotation
        self.angle = (self.angle + pi) % (2*pi) - pi
        self.body.angle = self.angle

    def update_target(self):
        if self.target is None or self.target.killed:
            if self.game.room.mobs or self.game.room.seekers:
                self.target = self.closest_target(chain(self.game.room.mobs, self.game.room.seekers))
            else:
                self.killed = True
                add_effect(self.hit_effect, self.game.room.top_effects, self.x, self.y)

    def update_pos(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.rect.center = self.x, self.y

    def update(self, dt):
        self.update_target()
        if self.killed:
            return
        self.update_angle(dt)
        self.update_vel(self.angle)
        self.update_pos(dt)
        self.update_body(dt)


class EnemySeeker(Seeker):
    def __init__(self, game, name, screen_rect, x, y, start_angle, rotation_speed, damage, vel):
        super().__init__(game, name, screen_rect, x, y, start_angle, rotation_speed, damage, vel)
        self.target = game.player
        self.sticky = False
        self.stunned = False

    @property
    def no_target(self):
        return False

    def update_target(self):
        pass

    def receive_damage(self, damage):
        self.killed = True
        self.game.sound_player.play_sound(ENEMY_DEATH)


class EnemyOrbitalSeeker(EnemySeeker):
    def __init__(self, owner, name, screen_rect, x, y,
                 start_angle, maneuvering_angle, damage):
        super().__init__(owner.game, name, screen_rect, x, y, start_angle,
                         maneuvering_angle, damage, HF(0.42))
        self.owner = owner
        self.orbiting = True
        self.orbiting_radius = owner.rect.width
        self.orbiting_angle = start_angle
        self.action_radius = HF(160) + self.target.radius

    def update(self, dt):
        if self.owner.killed and self.orbiting:
            self.killed = True
            return
        if self.orbiting:
            self.orbiting_angle -= 0.008 * dt
            angle = self.orbiting_angle + self.owner.body.angle
            self.x = self.owner.x + self.orbiting_radius * cos(angle)
            self.y = self.owner.y - self.orbiting_radius * sin(angle)
            self.rect.center = self.x, self.y
            self.angle = angle - 0.5 * pi
            if hypot(self.x - self.target.x, self.y - self.target.y) <= self.action_radius:
                self.orbiting = False
                self.angle = calculate_angle(self.x, self.y, SCR_W2, SCR_H2)
            self.body.angle = self.angle
            self.update_body(dt)
        else:
            super().update(dt)


class AllyInfector(Seeker):
    def __init__(self, game, screen_rect, x, y, start_angle):
        super().__init__(game, "ally infector", screen_rect, x, y, start_angle, 0.0072,  -1, HF(0.6))

    def eval_enemy(self, enemy):
        if not enemy.infected:
            if not enemy.chasing_infectors:
                return hypot(self.x - enemy.x, self.y - enemy.y)
            return hypot(self.x - enemy.x, self.y - enemy.y) + 100000
        return hypot(self.x - enemy.x, self.y - enemy.y) + 200000

    def update_target(self):
        if self.target is None or self.target.killed:
            if self.game.room.mobs:
                self.target = min(self.game.room.mobs, key=self.eval_enemy)
                self.target.chasing_infectors.add(self)
            elif self.game.room.seekers:
                self.target = self.closest_target(self.game.room.seekers)
            else:
                self.killed = True
                add_effect(self.hit_effect, self.game.room.top_effects, self.x, self.y)


class EnemyLeecher(EnemySeeker):
    def __init__(self, player, name, screen_rect, x, y, start_angle, rotation_speed, damage, vel):
        super().__init__(player.game, name, screen_rect, x, y, start_angle, rotation_speed, damage, vel)
        self.leeching = False
        self.leech_time = 0
        self.leech_cooldown = 450

    def update(self, dt):
        if self.leeching:
            self.angle = calculate_angle(self.x, self.y, self.target.x, self.target.y)
            self.leech_time += dt
            if self.leech_time >= self.leech_cooldown:
                self.leech_time = 0
                self.target.receive_damage(-1, play_sound=False)
            self.body.angle = self.angle
            self.update_body(dt)
        else:
            super().update(dt)

    def draw(self, surface, dx, dy):
        if self.leeching:
            start_pos = (SCR_W2, SCR_H2)
            end_pos = (round(self.x - dx), round(self.y - dy))
            pg.draw.line(surface, PINK, start_pos, end_pos, H(10))
            pg.draw.line(surface, RED, start_pos, end_pos, H(4))
        super().draw(surface, dx, dy)


class EnemySapper(EnemySeeker):
    def __init__(self, owner, game, name, screen_rect, x, y, start_angle, rotation_speed, damage, vel):
        super().__init__(game, name, screen_rect, x, y, start_angle, rotation_speed, damage, vel)
        self.owner = owner
        self.player = game.player
        self.going_to_player = True
        self.halo_time = 0
        self.time_to_hold_attack = 0

    def return_to_enemy(self):
        self.going_to_player = False
        self.target = self.owner

    @property
    def can_attack(self):
        return self.going_to_player and self.time_to_hold_attack == 0

    def update(self, dt):
        super().update(dt)
        if self.owner.killed:
            self.killed = True
        elif self.going_to_player:
            self.time_to_hold_attack = max(0, self.time_to_hold_attack - dt)
        elif self.owner.collide_bullet(self.x, self.y, self.radius):
            self.owner.update_health(3)
            self.going_to_player = True
            self.target = self.player
            self.time_to_hold_attack = 500

    def update_body(self, dt):
        if self.is_on_screen:
            self.body.update_shape(dt)
            self.halo_time = (self.halo_time + dt) % 540

    def draw(self, surface, dx, dy):
        if self.is_on_screen:
            self.body.draw(surface, dx, dy)
            if not self.going_to_player:
                index = int(18 * self.halo_time / 540)
                pos = self.body.circles[0].x - dx - H(27.5), self.body.circles[0].y - dy - H(27.5)
                surface.blit(sapper_surfaces[index], pos)


class LeecherBullet(Bullet):
    def __init__(self, screen_rect, x, y, damage, vel, angle):
        super().__init__("leecher bullet", screen_rect, x, y, damage, vel, angle)
        self.body.angle = angle

    def update(self, dt):
        self.update_pos(dt)
        self.update_body(dt)


class Drone(Bullet):
    def __init__(self, name, screen_rect, x, y, damage, vel, angle, player):
        super().__init__(name, screen_rect, x, y, damage, vel, angle)
        self.player = player
        self.name = name
        self.time = 0
        self.mitosis_time = 300
        self.angle = angle

    def divide(self):
        self.killed = True
        if self.name == "tiny drone":
            seeker = Seeker(self.player.game, "tiny drone", self.screen_rect,
                            self.x, self.y, self.angle, 0.009, -7, HF(0.9))
            seeker.update(0)
            self.player.seekers.append(seeker)
        else:
            if self.name == "big drone":
                child_name = "medium drone"
            elif self.name == "medium drone":
                child_name = "small drone"
            else:
                child_name = "tiny drone"
            for k in (-1, 1):
                angle = self.angle + k * uniform(0.2*pi, 0.8*pi)
                drone = Drone(child_name, self.screen_rect,
                              self.x, self.y, 0, HF(0.6), angle, self.player)
                drone.update(0)
                self.player.drones.append(drone)

    def update_body(self, dt):
        if self.is_on_screen:
            self.body.update_shape(dt)

    def update(self, dt):
        self.update_pos(dt)
        self.update_body(dt)
        self.time += dt
        if self.time >= self.mitosis_time:
            self.divide()


class PierceShot(Bullet):
    """ A bullet that can pass through many enemies. """
    def __init__(self, screen_rect, x, y, damage, vel, angle):
        super().__init__("sniper bullet", screen_rect, x, y, damage, vel, angle)
        self.body = pg.transform.rotate(self.body, angle * 180 / pi)
        self.x = x - self.body.get_width() / 2
        self.y = y - self.body.get_height() / 2
        self.attacked_mobs = []

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update_body(self, dt):
        pass

    def update(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.rect.center = self.x, self.y
        if self.is_outside:
            self.killed = True

    def draw(self, surface, dx, dy):
        if self.is_on_screen:
            surface.blit(self.body, (int(self.x - dx), int(self.y - dy)))


class ExplosivePierceShot(PierceShot):
    def __init__(self, screen_rect, x, y, damage, vel, angle):
        super().__init__(screen_rect, x, y, damage, vel, angle)
        self.hit_effect = 'DamageBurst'
        self.explosion_radius = H(130)


class FrangibleBullet(Bullet):
    """Bullet moves evenly and rectilinearly until its timer achieves fragmentation time.
     After this bullet explodes to form fragments scattering in all directions.
     If bullet collides with an object before fragmentation_time, it deals
     damage as a regular bullet and then disappears.
    """
    def __init__(self, player, screen_rect, x, y, angle):
        super().__init__("big light red", screen_rect, x, y, -20, HF(0.8), angle)
        self.time = 0
        self.fragmentation_time = 1000
        self.player = player

    def update(self, dt):
        self.update_pos(dt)
        self.update_body(dt)
        self.time = min(self.fragmentation_time, self.time + dt)
        if self.time == self.fragmentation_time:
            self.killed = True
            for i in range(0, 360, 12):
                fragment = PierceShot(self.screen_rect, self.x, self.y, -8, HF(2.1), i * pi / 180)
                self.player.bullets.append(fragment)


class BulletBuster(RegularBullet):
    def __init__(self, name, screen_rect, x, y, damage, vel, angle):
        super().__init__(name, screen_rect, x, y, damage, vel, angle)

    def collide_bullet(self, bul_x, bul_y, bul_r):
        return circle_collidepoint(self.x, self.y, self.radius + bul_r, bul_x, bul_y)


def get_bullet_type(bullet_type: str):
    if bullet_type == "regular bullet":
        return RegularBullet
    if bullet_type == "mine":
        return Mine
    if bullet_type == "pierce shot":
        return PierceShot
    if bullet_type == "explosive pierce shot":
        return ExplosivePierceShot
    if bullet_type == "leecher bullet":
        return LeecherBullet
    if bullet_type == "drone":
        return Drone
    if bullet_type == "seeker":
        return Seeker
    if bullet_type == "enemy seeker":
        return EnemySeeker
    if bullet_type == "enemy leecher":
        return EnemyLeecher
    if bullet_type == "enemy orbital seeker":
        return EnemyOrbitalSeeker
    if bullet_type == "enemy sapper":
        return EnemySapper
    if bullet_type == "bullet buster":
        return BulletBuster


__all__ = [

    "RegularBullet",
    "ExplodingBullet",
    "Mine",
    "AllyOrbitalSeeker",
    "Seeker",
    "LeecherBullet",
    "EnemySeeker",
    "EnemyLeecher",
    "EnemySapper",
    "PierceShot",
    "ExplosivePierceShot",
    "FrangibleBullet",
    "BulletBuster",
    "Drone",
    "EnemyOrbitalSeeker",
    "AllyInfector",
    "get_bullet_type"

]

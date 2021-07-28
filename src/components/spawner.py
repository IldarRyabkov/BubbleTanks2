from math import cos, sin, pi
from random import uniform
import pygame as pg

from assets.paths import ENEMY_DEATH
from data.shapes import SHAPES

from components.bullets import EnemySeeker
from components.circle import make_circle
from components.special_effects import add_effect
from components.utils import *


class Spawner:
    def __init__(self, owner, game, data):
        self.owner = owner
        self.game = game
        self.screen_rect = game.rect
        self.distance = data["distance"]
        self.angle = data["angle"]
        self.x = 0
        self.y = 0
        self.circle = make_circle(SHAPES["spawner"], screen_rect=game.rect)
        self.radius = self.circle.max_radius
        rect_size = round(2 * self.radius)
        self.rect = pg.Rect(0, 0, rect_size, rect_size)
        self.killed = False

    @property
    def is_on_screen(self):
        return self.rect.colliderect(self.screen_rect)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.center = self.x, self.y
        self.circle.update(self.x, self.y, 0, self.angle + self.owner.body.angle)

    def collide_bullet(self, bullet) -> bool:
        return (self.rect.colliderect(bullet.rect) and
                circle_collidepoint(*self.rect.center, self.radius + bullet.radius, bullet.x, bullet.y))

    def receive_damage(self, damage):
        for _ in range(8):
            offset = uniform(0, self.radius)
            angle = uniform(0, 2 * pi)
            x = self.x + offset * cos(angle)
            y = self.y - offset * sin(angle)
            seeker = EnemySeeker(self.game, "enemy seeker", self.game.rect, x, y, angle, 0.009, -5, 0.3)
            seeker.update(0)
            self.game.room.seekers.append(seeker)

        add_effect("SpawnerBurst", self.game.room.top_effects, self.x, self.y)
        self.killed = True
        self.game.sound_player.play_sound(ENEMY_DEATH)

    def update_shape(self, dt):
        self.circle.update(self.x, self.y, dt, self.angle + self.owner.body.angle)

    def update(self, dt):
        if self.owner.health <= 0:
            self.killed = True
        angle = self.angle + self.owner.body.angle
        self.x = self.owner.x + self.distance * cos(angle)
        self.y = self.owner.y - self.distance * sin(angle)
        self.rect.center = self.x, self.y
        self.circle.update(self.x, self.y, dt, angle)

    def draw(self, screen, dx=0, dy=0):
        if self.is_on_screen:
            self.circle.draw(screen, dx, dy)


__all__ = ["Spawner"]

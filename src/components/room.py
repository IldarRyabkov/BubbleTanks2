from math import pi
from random import uniform, randint

from data.constants import *

from components.bubble import Bubble
from components.utils import HF
from components.enemy import make_enemy
from components.spawner import Spawner
from components.bullets import AllyInfector


class Room:
    """Stores, updates and draws all objects in the room, such as:
        - enemies;
        - spawners;
        - enemy bullets;
        - enemy mines;
        - enemy seekers;
        - bubbles to collect;
        - special effects.
    It also stores radius of player's gravitational field,
    in which bubbles are attracted to the player.
    """
    gravitation_radius = HF(1.5 * 160)
    bullets = []
    mines = []
    seekers = []
    bubbles = []
    bottom_effects = []
    top_effects = []
    mobs = []
    spawners = []

    # temporary lists that store enemies and spawners of the next room during transportation of player
    new_mobs = []
    new_spawners = []

    def __init__(self, game):
        self.game = game
        self.player = game.player

    @property
    def no_enemies(self) -> bool:
        return not self.mobs and not self.seekers

    def set_save_data(self, enemies_dict):
        for obj in (self.bubbles, self.bullets, self.mines, self.seekers,
                    self.spawners, self.top_effects, self.bottom_effects,
                    self.mobs, self.new_mobs):
            obj.clear()
        for name, n in enemies_dict.items():
            for _ in range(n):
                enemy = make_enemy(self.game, name)
                self.mobs.append(enemy)
        for enemy in self.mobs:
            self.add_spawners(self.spawners, enemy, enemy.spawners_data)

    def set_new_enemies(self, enemies_dict: dict):
        self.new_mobs.clear()
        for name, n in enemies_dict.items():
            for _ in range(n):
                enemy = make_enemy(self.game, name)
                self.new_mobs.append(enemy)
        for enemy in self.new_mobs:
            self.add_spawners(self.new_spawners, enemy, enemy.spawners_data)

    def move_new_enemies(self, dx, dy):
        for mob in self.new_mobs:
            mob.move(dx, dy)

    def move_new_spawners(self, dx, dy):
        for spawner in self.new_spawners:
            spawner.move(dx, dy)

    def add_spawners(self, spawners: list, enemy, spawners_data: list):
        for data in spawners_data:
            spawners.append(Spawner(enemy, self.game, data))

    def spawn_enemy(self, name, x, y, angle=None):
        enemy = make_enemy(self.game, name)
        enemy.set_pos(x, y)
        if angle is not None:
            enemy.body.angle = angle
            enemy.set_velocity()
        self.mobs.append(enemy)

    def spawn_leeched_bubble(self, x, y):
        bubble = Bubble(self.game.rect, x, y, gravitation_radius=2*ROOM_RADIUS)
        bubble.vel = 0
        self.bubbles.append(bubble)

    def set_params_after_transportation(self):
        self.mobs.clear()
        self.spawners.clear()
        for enemy in self.new_mobs:
            self.mobs.append(enemy)
        for spawner in self.new_spawners:
            self.spawners.append(spawner)
        for obj in (self.bubbles, self.bullets, self.mines,
                    self.seekers, self.new_spawners, self.top_effects,
                    self.bottom_effects, self.new_mobs):
            obj.clear()
        for enemy in self.mobs:
            enemy.weapons.update_pos()
            enemy.update_shape(0)
        for spawner in self.spawners:
            spawner.update_shape(0)

    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.update(dt)
        self.bullets = list(filter(lambda b: not b.killed, self.bullets))

    def update_mines(self, dt):
        for mine in self.mines:
            mine.update(dt)
        self.mines = list(filter(lambda m: not m.killed, self.mines))[-50:]

    def update_seekers(self, dt):
        for seeker in self.seekers:
            seeker.update(dt)
        self.seekers = list(filter(lambda s: not s.killed, self.seekers))

    def update_bubbles(self, dt):
        x, y = self.player.x, self.player.y
        for bubble in self.bubbles:
            bubble.update(x, y, dt)
        self.bubbles = list(filter(lambda b: not b.is_outside, self.bubbles))
        if self.no_enemies:
            for bubble in self.bubbles:
                bubble.maximize_gravity()

    def update_spawners(self, dt):
        for spawner in self.spawners:
            spawner.update(dt)
        self.spawners = list(filter(lambda s: not s.killed, self.spawners))

    def update_new_spawners(self, dt):
        for spawner in self.new_spawners:
            spawner.update(dt)

    def update_effects(self, dt):
        for effect in self.top_effects:
            effect.update(dt)
        for effect in self.bottom_effects:
            effect.update(dt)
        self.top_effects = list(filter(lambda e: e.running, self.top_effects))
        self.bottom_effects = list(filter(lambda e: e.running, self.bottom_effects))

    def set_gravity_radius(self):
        radius = 1.5 * self.game.player.bg_radius
        if not self.no_enemies:
            self.gravitation_radius = radius
            for bubble in self.bubbles:
                bubble.gravitation_radius = radius

    def spawn_infectors(self, x, y):
        for _ in range(randint(1, 3)):
            infector = AllyInfector(self.game, self.game.rect, x, y, uniform(0, 2*pi))
            infector.update(0)
            self.player.seekers.append(infector)

    def update_enemies(self, dt):
        for enemy in self.mobs:
            enemy.update(dt)
            if enemy.killed:
                self.add_bubbles(enemy)
                if enemy.infected:
                    self.spawn_infectors(enemy.x, enemy.y)
        self.mobs = list(filter(lambda m: not m.killed, self.mobs))

    def update_new_enemies(self, dt):
        for mob in self.new_mobs:
            mob.update(dt)

    def update(self, dt):
        self.update_enemies(dt)
        self.update_new_enemies(dt)
        self.update_spawners(dt)
        self.update_new_spawners(dt)
        self.update_bubbles(dt)
        self.update_bullets(dt)
        self.update_mines(dt)
        self.update_seekers(dt)
        self.update_effects(dt)

    def add_bubbles(self, enemy):
        """Method is called when an object is killed.
        Adds new bubbles to the list of bubbles.
        """
        for bubble_name, n in enemy.death_award.items():
            for i in range(n):
                bubble = Bubble(self.game.rect, enemy.x, enemy.y,
                                uniform(0, 2 * pi),
                                self.gravitation_radius, bubble_name)
                self.bubbles.append(bubble)

    def draw_bubbles(self, surface, dx, dy):
        for bubble in self.bubbles:
            bubble.draw(surface, dx, dy)

    def draw_enemies(self, surface, dx, dy):
        for enemy in self.mobs:
            enemy.draw(surface, dx, dy)

    def draw_new_enemies(self, surface, dx, dy):
        for enemy in self.new_mobs:
            enemy.draw(surface, dx, dy)

    def draw_mines(self, surface, dx, dy):
        for mine in self.mines:
            mine.draw(surface, dx, dy)

    def draw_bullets(self, surface, dx, dy):
        for bullet in self.bullets:
            bullet.draw(surface, dx, dy)
        for bullet in self.seekers:
            bullet.draw(surface, dx, dy)

    def draw_spawners(self, surface, dx, dy):
        for spawner in self.spawners:
            spawner.draw(surface, dx, dy)

    def draw_new_spawners(self, surface, dx, dy):
        for spawner in self.new_spawners:
            spawner.draw(surface, dx, dy)

    def draw_top_effects(self, surface, dx, dy):
        for effect in self.top_effects:
            effect.draw(surface, dx, dy)

    def draw_bottom_effects(self, surface, dx, dy):
        for effect in self.bottom_effects:
            effect.draw(surface, dx, dy)


__all__ = ["Room"]

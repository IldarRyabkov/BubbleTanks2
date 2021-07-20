from math import pi
from random import uniform, randint

from data.constants import *

from components.bubble import Bubble
from components.utils import HF
from components.enemy import Enemy
from components.spawner import Spawner
from components.bullets import AllyInfector


class Room:
    """Class that stores, updates and draws all objects in the room, such as:

        - mobs;
        - bullets of mobs;
        - mines of mobs;
        - seekers of mobs;
        - bubbles;
        - special effects.

    It also stores some parameters of the room such as:

        - radius of player's gravitational field, in which bubbles are attracted to the player;
        - screen offset according to player's position, which is used to check if a mob should be drawn or not

    """
    bullets = []
    mines = []
    seekers = []
    bubbles = []

    # Bottom/top effects are drawn before/after player, mobs, bullets and bubbles are drawn.
    bottom_effects = []
    top_effects = []

    mobs = []
    spawners = []
    new_mobs = []
    new_spawners = []

    gravitation_radius = HF(1.5 * 160)  # radius of player's gravitational field

    def __init__(self, game):
        self.game = game
        self.player = game.player

    @property
    def no_enemies(self) -> bool:
        return not self.mobs and not self.seekers

    def boss_defeated(self, boss_disposition) -> bool:
        return boss_disposition == BOSS_IN_CURRENT_ROOM and not self.mobs

    def set_data(self, mobs_dict):
        for obj in (self.bubbles, self.bullets, self.mines, self.seekers,
                    self.spawners, self.top_effects, self.bottom_effects,
                    self.mobs, self.new_mobs):
            obj.clear()
        self.load_mobs_from_dict(self.mobs, mobs_dict)
        for enemy in self.mobs:
            self.add_spawners(self.spawners, enemy, enemy.spawners_data)

    def load_new_mobs(self, mobs_dict):
        self.load_mobs_from_dict(self.new_mobs, mobs_dict)
        for enemy in self.new_mobs:
            self.add_spawners(self.new_spawners, enemy, enemy.spawners_data)

    def load_mobs_from_dict(self, mobs: list, mobs_dict):
        mobs.clear()
        for name, n in mobs_dict.items():
            for _ in range(n):
                enemy = Enemy(self.game, name)
                mobs.append(enemy)

    def move_new_mobs(self, dx, dy):
        for mob in self.new_mobs:
            mob.move(dx, dy)

    def move_new_spawners(self, dx, dy):
        for spawner in self.new_spawners:
            spawner.move(dx, dy)

    def add_spawners(self, spawners: list, enemy, spawners_data: list):
        for data in spawners_data:
            spawners.append(Spawner(enemy, self.game, data))

    def spawn_enemy(self, name, x, y, angle=None):
        enemy = Enemy(self.game, name)
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
            spawner.update_body(0)

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
        """ Updates all spawners in the room player is being transported to. """
        for spawner in self.new_spawners:
            spawner.update(dt)

    def update_effects(self, dt):
        for effect in self.top_effects:
            effect.update(dt)
        for effect in self.bottom_effects:
            effect.update(dt)
        self.top_effects = list(filter(lambda e: e.running, self.top_effects))
        self.bottom_effects = list(filter(lambda e: e.running, self.bottom_effects))

    def set_gravity_radius(self, gravitation_radius):
        """Method is called when the player is being upgraded.
        Sets the new radius of player's gravitational field.
        """
        if not self.no_enemies:
            self.gravitation_radius = gravitation_radius

            for bubble in self.bubbles:
                bubble.gravitation_radius = gravitation_radius

    def spawn_infectors(self, x, y):
        for _ in range(randint(1, 3)):
            infector = AllyInfector(self.game, self.game.rect, x, y, uniform(0, 2*pi))
            infector.update(0)
            self.player.seekers.append(infector)

    def update_mobs(self, dt):
        """Updates all mobs in the room. If some mobs are killed,
        removes them from the list and adds bubbles.
        """
        for enemy in self.mobs:
            enemy.update(dt)
            if enemy.killed:
                self.add_bubbles(enemy)
                if enemy.infected:
                    self.spawn_infectors(enemy.x, enemy.y)
        self.mobs = list(filter(lambda m: not m.killed, self.mobs))

    def update_new_mobs(self, dt):
        """ Updates all mobs in the room player is being transported to. """
        for mob in self.new_mobs:
            mob.update(dt)

    def update_screen_rect(self):
        """Sets the center of room screen-rectangle equal to the player's new pos. """
        self.game.rect.center = self.player.x, self.player.y

    def update(self, dt):
        """Updates all objects in the room and room parameters. """
        self.update_screen_rect()
        self.update_mobs(dt)
        self.update_new_mobs(dt)
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
                bubble = Bubble(self.game.rect, enemy.x, enemy.y, uniform(0, 2 * pi), self.gravitation_radius, bubble_name)
                self.bubbles.append(bubble)

    def draw_bubbles(self, surface, dx, dy):
        for bubble in self.bubbles:
            bubble.draw(surface, dx, dy)

    def draw_mobs(self, surface, dx, dy):
        for mob in self.mobs:
            mob.draw(surface, dx, dy)

    def draw_new_mobs(self, surface, dx, dy):
        for mob in self.new_mobs:
            mob.draw(surface, dx, dy)

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

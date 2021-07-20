import pygame as pg
import sys
from itertools import chain
from math import hypot

from assets.paths import *
from data.scripts import *
from data.constants import *

from menus.upgrade_menu import UpgradeMenu
from menus.victory_menu import VictoryMenu
from menus.main_menu import MainMenu
from menus.pause_menu import PauseMenu

from gui.widgets.health_window import HealthWindow
from gui.widgets.cooldown_window import CooldownWindow

from components.player import Player
from components.enemy import Enemy
from components.bullets import *
from components.background_environment import BackgroundEnvironment
from components.camera import Camera
from components.room import Room
from components.sound_player import SoundPlayer
from components.bubble_tanks_world import BubbleTanksWorld
from components.fps_manager import FPSManager
from components.superpowers import Disassemble
from components.special_effects import *
from components.utils import *


class Game:
    """The main class, which is the core of the game and manages all game objects."""
    def __init__(self, screen):
        self.screen = screen
        self.rect = pg.Rect(0, 0, SCR_W, SCR_H)
        self.language = load_language()

        self.screen_mode = WINDOWED_MODE
        self.set_screen_mode(load_screen_mode())

        self.running = True
        self.pause = False
        self.transportation = False

        self.fps_manager = FPSManager()

        self.sound_player = SoundPlayer()
        self.clock = pg.time.Clock()
        self.bg_environment = BackgroundEnvironment(self)
        self.camera = Camera()
        self.player = Player(self)
        self.world = BubbleTanksWorld(self.player)
        self.room = Room(self)

        self.main_menu = MainMenu(self)
        self.upgrade_menu = UpgradeMenu(self)
        self.victory_menu = VictoryMenu(self)
        self.pause_menu = PauseMenu(self)

        self.health_window = HealthWindow(self)
        self.cooldown_window = CooldownWindow(self)

    def set_screen_mode(self, screen_mode):
        if screen_mode == self.screen_mode:
            return

        if screen_mode == FULLSCREEN_MODE:
            pg.display.toggle_fullscreen()

        elif screen_mode == WINDOWED_MODE:
            if self.screen_mode == FULLSCREEN_MODE:
                pg.display.toggle_fullscreen()
            pg.display.set_mode(SCR_SIZE, flags=0)

        elif screen_mode == BORDERLESS_MODE:
            if self.screen_mode == FULLSCREEN_MODE:
                pg.display.toggle_fullscreen()
            pg.display.set_mode(SCR_SIZE, flags=pg.NOFRAME)

        self.screen_mode = screen_mode

    def update_save_data(self):
        self.world.save_enemies(self.room.mobs)
        tank = self.player.tank
        tank_history = self.player.tanks_history
        health = self.player.health
        max_cumulative_health = self.player.max_cumulative_health
        enemies_killed = self.pause_menu.stats_counters[0].text
        bubbles_collected = self.pause_menu.stats_counters[1].text
        visited_rooms = self.pause_menu.map_button.graph
        enemies = self.world.enemies_dict
        current_room = self.world.cur_room
        boss_generated = self.world.boss_generated
        boss_disposition = self.bg_environment.boss_disposition
        boss_position = self.bg_environment.boss_pos
        hints_history = self.bg_environment.hints_history
        save_name = self.main_menu.current_save
        update_save_file(save_name, tank, tank_history, health,
                         max_cumulative_health, enemies_killed, bubbles_collected,
                         visited_rooms, enemies, current_room,
                         boss_generated, boss_disposition, boss_position,
                         hints_history)

    def set_save_data(self, save_data: dict):
        self.player.set_save_data(save_data)
        self.world.load_save(save_data)
        self.bg_environment.set_data(save_data)
        self.health_window.set_data()
        self.cooldown_window.set_data()
        self.room.set_data(self.world.current_enemies)
        self.pause_menu.set_data(save_data)
        self.camera.stop_shaking()
        self.running = True
        self.pause = False
        self.transportation = False
        self.clock.tick()
        self.set_language(self.language)

    def set_language(self, lang):
        self.bg_environment.set_language(lang)
        self.upgrade_menu.set_language(lang)
        self.victory_menu.set_language(lang)
        self.pause_menu.set_language(lang)
        self.cooldown_window.set_language(lang)

    def set_windows(self):
        self.health_window.set()
        self.cooldown_window.set()

    def quit(self):
        self.update_save_data()
        pg.quit()
        sys.exit()

    def handle(self, e_type, e_key):
        if e_type == pg.KEYDOWN and e_key in [pg.K_p, pg.K_ESCAPE] and not self.transportation:
            self.pause = True
        else:
            self.player.handle(e_type, e_key)

    def handle_events(self):
        """Main events handler that handles pygame events
        during the actual game.
        """
        for event in pg.event.get():
            if event.type in [pg.KEYDOWN, pg.KEYUP]:
                self.handle(event.type, event.key)
            elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
                self.handle(event.type, event.button)
            elif event.type == pg.QUIT:
                self.quit()

    def handle_bubble_eating(self):
        eaten_bubbles = 0
        for i, bubble in enumerate(self.room.bubbles):
            if self.player.collide_bubble(bubble.x, bubble.y):
                self.player.update_health(bubble.health)
                self.health_window.activate()
                self.room.bubbles[i] = None
                eaten_bubbles += 1
        if eaten_bubbles:
            self.pause_menu.update_counter(1, eaten_bubbles)
            self.room.bubbles = list(filter(lambda b: b is not None, self.room.bubbles))
            self.sound_player.play_sound(COLLECT_BUBBLE)

    def downgrade_player(self):
        self.player.downgrade()
        self.set_windows()
        self.pause_menu.update_tank_description()
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.room.set_gravity_radius(1.3 * self.player.bg_radius)

    def upgrade_player(self):
        if self.player.last_tank_in_history:
            self.upgrade_menu.run()
            if not self.running:
                return
            self.player.upgrade(True, self.upgrade_menu.chosen_tank)
        else:
            self.player.upgrade(False)

        self.set_windows()
        self.pause_menu.update_tank_description()
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.room.set_gravity_radius(1.3 * self.player.bg_radius)

    def add_effect(self, entity):
        add_effect(entity.hit_effect, self.room.top_effects, entity.x, entity.y)

    def handle_damage_to_player(self, bullet):
        """Handles damage to player made by enemy's bullet. """
        if isinstance(bullet, EnemyLeecher):
            if bullet.leeching:
                return
            if self.player.shield_on:
                bullet.killed = True
                self.add_effect(bullet)
            else:
                bullet.leeching = True
                self.player.receive_damage(bullet.damage, play_sound=False)
        elif isinstance(bullet, EnemySapper):
            if bullet.can_attack:
                self.player.receive_damage(bullet.damage, play_sound=False)
                bullet.return_to_enemy()
                add_effect("SapperAttack", self.room.top_effects)
        else:
            self.player.receive_damage(bullet.damage)
            bullet.killed = True
            self.add_effect(bullet)

    def handle_bullet_explosion(self, bullet):
        x, y, radius = bullet.x, bullet.y, bullet.explosion_radius
        for enemy in chain(self.room.mobs, self.room.seekers, self.room.spawners):
            if enemy.collide_bullet(x, y, radius):
                enemy.receive_damage(bullet.damage)
        bullet.killed = True
        self.add_effect(bullet)
        add_effect('Flash', self.room.top_effects)
        self.camera.start_shaking(200)

    def handle_sniper_bullet_explosion(self, bullet):
        x, y, radius = bullet.x, bullet.y, bullet.explosion_radius
        for enemy in chain(self.room.mobs, self.room.seekers, self.room.spawners):
            if enemy not in bullet.attacked_mobs and enemy.collide_bullet(x, y, radius):
                enemy.receive_damage(bullet.damage)
                bullet.attacked_mobs.append(enemy)
        self.add_effect(bullet)
        for _ in range(3):
            add_effect('SmallHitLines', self.room.top_effects, bullet.x, bullet.y)
        add_effect('BigHitLines', self.room.top_effects, bullet.x, bullet.y)
        add_effect('Flash', self.room.top_effects)
        self.camera.start_shaking(200)

    def handle_enemy_collision(self, enemy, bullet):
        """Handles collision between enemy and player's bullet. """
        if isinstance(bullet, ExplodingBullet):
            self.handle_bullet_explosion(bullet)
        elif isinstance(bullet, ExplosivePierceShot):
            if enemy not in bullet.attacked_mobs:
                self.handle_sniper_bullet_explosion(bullet)
        else:
            enemy.receive_damage(bullet.damage)
            bullet.killed = True
            self.add_effect(bullet)
            if isinstance(bullet, LeecherBullet):
                self.room.spawn_leeched_bubble(enemy.x, enemy.y)
            elif isinstance(bullet, AllyInfector):
                if bullet in enemy.chasing_infectors:
                    enemy.chasing_infectors.remove(bullet)
                if isinstance(enemy, Enemy):
                    enemy.become_infected()

    def handle_enemies_collisions(self):
        """Handles collisions between enemies and player's bullets. """
        for bullet in chain(self.player.bullets, self.player.mines, self.player.seekers):
            if isinstance(bullet, BulletBuster):
                continue
            for enemy in chain(self.room.mobs, self.room.seekers, self.room.spawners):
                if enemy.collide_bullet(bullet.x, bullet.y, bullet.radius):
                    self.handle_enemy_collision(enemy, bullet)
                    if not isinstance(bullet, PierceShot):
                        break

    def handle_allys_collisions(self):
        """Handles collisions between player's tank/seekers and all bullets of enemies. """
        if self.player.disassembled:
            return
        for bullet in chain(self.room.bullets, self.room.mines, self.room.seekers):
            if self.player.collide_bullet(bullet.x, bullet.y, bullet.radius):
                self.handle_damage_to_player(bullet)
        for bullet in chain(self.room.bullets, self.room.mines):
            for seeker in self.player.seekers:
                if seeker.collide_bullet(bullet.x, bullet.y, bullet.radius):
                    seeker.killed = True
                    bullet.killed = True
                    self.add_effect(seeker)
                    self.add_effect(bullet)
                    if isinstance(seeker, AllyInfector) and seeker in seeker.target.chasing_infectors:
                        seeker.target.chasing_infectors.remove(seeker)

    def update_transportation(self, dt):
        """ Update all objects during transportation. """
        self.player.update(dt)
        self.room.update(dt)
        self.health_window.update(dt)
        self.cooldown_window.update(dt)

    def draw_transportation(self, time, dx, dy):
        """ Draw all objects during transportation. """
        offset_old = self.camera.offset
        offset_new = self.camera.dx + dx, self.camera.dy + dy

        self.bg_environment.draw_bg(self.screen)
        self.bg_environment.draw_room_bg(self.screen, *offset_new)
        self.bg_environment.draw_room_bg(self.screen, *offset_old)
        self.bg_environment.draw_hint(self.screen, *offset_old)
        self.bg_environment.draw_new_hint(self.screen, *offset_new)
        self.bg_environment.draw_destination_circle(self.screen, *offset_old)
        self.bg_environment.draw_player_trace(self.screen, *offset_old, time)
        self.bg_environment.draw_player_halo(self.screen, offset_old, offset_new)
        self.bg_environment.draw_boss_skeleton(self.screen, *offset_new, True)

        self.room.draw_bottom_effects(self.screen, *offset_old)
        self.room.draw_bubbles(self.screen, *offset_old)
        self.room.draw_mines(self.screen, *offset_old)

        self.player.draw(self.screen, *offset_old)

        self.room.draw_mobs(self.screen, *offset_old)
        self.room.draw_spawners(self.screen, *offset_old)
        self.room.draw_bullets(self.screen, *offset_old)
        self.room.draw_new_mobs(self.screen, *offset_old)
        self.room.draw_new_spawners(self.screen, *offset_old)

        self.bg_environment.draw_room_glares(self.screen, *offset_new)
        self.bg_environment.draw_room_glares(self.screen, *offset_old)

        self.room.draw_top_effects(self.screen, *offset_old)

        self.health_window.draw(self.screen)
        self.cooldown_window.draw(self.screen)

    def run_transportation(self, dx, dy):
        self.sound_player.play_sound(WATER_SPLASH)
        time = dt = 0
        while time < TRANSPORTATION_TIME and self.running:
            self.sound_player.reset()
            self.handle_events()
            self.update_transportation(dt)
            self.draw_transportation(time, dx, dy)
            pg.display.update()
            dt = self.clock.tick()
            self.fps_manager.update(dt)
            time += dt

    def get_destination_pos(self, dx, dy):
        """Method returns player's destination point during transportation. """
        distance = DIST_BETWEEN_ROOMS - (ROOM_RADIUS - self.player.bg_radius - H(40))
        return SCR_W2 + dx * distance, SCR_H2 + dy * distance

    def manage_transportation(self, dx, dy):
        self.transportation = True

        offset = -DIST_BETWEEN_ROOMS * dx, -DIST_BETWEEN_ROOMS * dy

        self.room.move_new_mobs(-offset[0], -offset[1])
        self.room.move_new_spawners(-offset[0], -offset[1])

        self.bg_environment.set_new_boss_disposition(self.world.cur_room,
                                                     self.room.new_mobs)
        self.pause_menu.map_button.update_data(self.world.cur_room,
                                               self.bg_environment.new_boss_disposition)
        self.bg_environment.set_next_hint()

        end_x, end_y = self.get_destination_pos(dx, dy)
        distance = hypot(self.player.x - end_x, self.player.y - end_y)
        angle = calculate_angle(self.player.x, self.player.y, end_x, end_y)
        self.player.set_transportation_vel(angle, distance / TRANSPORTATION_TIME)

        self.bg_environment.set_player_trace(self.player.x, self.player.y, distance, angle)
        self.bg_environment.set_destination_circle(end_x, end_y)

        self.run_transportation(*offset)

        self.player.move(*offset)
        self.room.update_screen_rect()
        self.player.update_shape(0)

        self.room.move_new_mobs(*offset)
        self.room.move_new_spawners(*offset)
        self.room.set_params_after_transportation()

        self.player.set_params_after_transportation()
        self.bg_environment.set_params_after_transportation()

        self.update_save_data()

        self.transportation = False
        self.clock.tick()

    def get_direction(self):
        player_offset = hypot(*self.camera.offset)
        if player_offset == 0:
            return [-1, 0]
        if (self.camera.dx / player_offset) ** 2 <= 0.5:
            return [0, -1] if self.camera.dy < 0 else [0, 1]
        return [1, 0] if self.camera.dx > 0 else [-1, 0]

    def eject_player(self):
        easy_room_created = False
        min_difficulty = 999999
        direction = -1, 0
        enemies = dict()
        directions = (-1, 0), (1, 0), (0, -1), (0, 1)

        for dx, dy in directions:
            if self.world.room_exists(dx, dy):
                difficulty = self.world.estimate_difficulty(dx=dx, dy=dy)
            else:
                if easy_room_created:
                    continue
                enemies = self.world.create_easy_enemies()
                difficulty = self.world.estimate_difficulty(enemies=enemies)
                easy_room_created = True

            if difficulty < min_difficulty:
                min_difficulty = difficulty
                direction = dx, dy

        if easy_room_created:
            self.world.confirm_enemies(enemies, *direction)

        self.world.move(*direction)
        self.room.load_new_mobs(self.world.current_enemies)
        self.manage_transportation(*direction)

    def transport_player(self):
        direction = self.get_direction()
        self.world.save_enemies(self.room.mobs)
        self.world.create_enemies(*direction)
        self.world.move(*direction)
        self.room.load_new_mobs(self.world.current_enemies)
        self.manage_transportation(*direction)

    def check_player_state(self):
        """Checks if player should upgrade or downgrade.
        If so, upgrades/downgrades player's tank state
        """
        if self.player.has_to_upgrade:
            self.upgrade_player()
        elif self.player.has_to_downgrade:
            self.downgrade_player()

    def update(self, dt):
        if self.pause:
            self.run_pause_menu()
            return

        self.handle_bubble_eating()
        self.handle_enemies_collisions()
        self.handle_allys_collisions()
        self.check_player_state()
        self.player.update(dt)
        self.room.update(dt)

        if self.room.boss_defeated(self.bg_environment.boss_disposition):
            self.victory_menu.run()
        if not self.running:
            return

        self.health_window.update(dt)
        self.cooldown_window.update(dt)

        if self.player.cumulative_health < 0:
            self.eject_player()
        elif self.player.is_outside:
            self.transport_player()

    def draw_background(self, surface):
        """Draw all entities that should be drawn below player, mobs, bullets etc. """
        self.bg_environment.draw_bg(surface)
        self.bg_environment.draw_room_bg(surface, *self.camera.offset)
        self.bg_environment.draw_player_halo(surface, self.camera.offset)
        self.bg_environment.draw_hint(surface, *self.camera.offset)
        self.bg_environment.draw_boss_skeleton(surface, *self.camera.offset)

    def draw_foreground(self):
        """Foreground includes player, mobs, bullets,
        bubbles, popup windows and effects.
        """
        self.room.draw_bottom_effects(self.screen, *self.camera.offset)
        self.room.draw_bubbles(self.screen, *self.camera.offset)
        self.room.draw_mines(self.screen, *self.camera.offset)
        self.player.draw(self.screen, *self.camera.offset)
        self.room.draw_mobs(self.screen, *self.camera.offset)
        self.room.draw_spawners(self.screen, *self.camera.offset)
        self.room.draw_bullets(self.screen, *self.camera.offset)
        self.bg_environment.draw_room_glares(self.screen, *self.camera.offset)
        self.room.draw_top_effects(self.screen, *self.camera.offset)
        self.health_window.draw(self.screen)
        self.cooldown_window.draw(self.screen)

    def update_scaling_objects(self, dt):
        """Method is called when Pause menu/Victory menu is running.
        It updates the sizes of mobs, player, bullets, etc.,
        animating them in the background in the Pause menu/Victory menu.
        """
        if isinstance(self.player.superpower, Disassemble):
            self.player.superpower.update_body()
        self.player.update_shape(dt)
        for enemy in self.room.mobs:
            enemy.update_shape(dt)

        for obj in chain(self.player.mines, self.player.bullets,
                         self.player.seekers, self.player.orbital_seekers,
                         self.room.spawners, self.room.seekers,
                         self.room.bubbles, self.room.mines, self.room.bullets):
            obj.update_body(dt)

        for seeker in self.player.orbital_seekers:
            if seeker.orbiting:
                seeker.update_pos(dt)

        self.room.update_effects(dt)
        self.camera.update(self.player.x, self.player.y, dt)

    def run_pause_menu(self):
        self.draw_background(self.pause_menu.bg_surface)
        self.pause_menu.run()
        self.pause = False

    @set_cursor_grab(True)
    def run_game(self):
        """ Game loop that starts when the main menu is closed. """
        self.clock.tick()
        dt = 0
        while self.running:
            self.sound_player.reset()
            self.update(dt)
            if self.running:
                self.draw_background(self.screen)
                self.draw_foreground()
                pg.display.update()
            self.handle_events()
            dt = self.clock.tick()
            self.fps_manager.update(dt)

    def run(self):
        """Main game loop. """
        while True:
            self.main_menu.run()
            self.run_game()


__all__ = ["Game"]

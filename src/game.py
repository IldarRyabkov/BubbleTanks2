import pygame as pg
import sys
import numpy as np
from math import hypot
from collections import defaultdict
import ctypes
import platform


from data.paths import (GAME_MUSIC, START_MUSIC, PLAYER_BULLET_HIT,
                        MOB_DEATH, BUBBLE_DEATH, PLAYER_INJURE)
from data.config import *
from background_environment import BackgroundEnvironment
from objects.player import Player
from objects.mob import Mob
from objects.bullets import DrillingBullet, ExplodingBullet
from camera import Camera
from room import Room
from sound_player import SoundPlayer
from room_generator import RoomGenerator
from fps_manager import FPSManager
from menus.upgrade_menu import UpgradeMenu
from menus.victory_menu import VictoryMenu
from menus.start_menu import StartMenu
from menus.pause_menu import PauseMenu
from gui.health_window import HealthWindow
from gui.cooldown_window import CooldownWindow
from special_effects import add_effect
from superpowers import Ghost
from utils import calculate_angle
from data.cursor import CURSOR


class Game:
    """The core of the game. """
    def __init__(self):
        pg.init()
        cursor = pg.cursors.compile(CURSOR, black='.', white='X')
        pg.mouse.set_cursor((32, 32), (0, 0), *cursor)
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP,
                              pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP])

        # Make sure the game will display correctly on high DPI monitors on Windows
        if platform.system() == 'Windows':
            ctypes.windll.user32.SetProcessDPIAware()

        self.screen = pg.display.set_mode(SCR_SIZE)
        self.sound_player = SoundPlayer()
        self.running = True
        self.transportation = False
        self.dt = 0
        self.fps_manager = FPSManager()
        self.clock = pg.time.Clock()
        self.bg_environment = BackgroundEnvironment()
        self.player = Player()
        self.key_handlers = defaultdict(list)
        self.camera = Camera()
        self.room = Room()
        self.room_generator = RoomGenerator()
        self.start_menu = StartMenu()
        self.upgrade_menu = UpgradeMenu()
        self.victory_menu = VictoryMenu()
        self.pause_menu = PauseMenu(self.sound_player.sounds)
        self.health_window = HealthWindow()
        self.cooldown_window = CooldownWindow()
        self.init_key_handlers()

    def reset_data(self):
        self.running = True
        self.transportation = False
        self.player = Player()
        self.room_generator.reset()
        self.room.reset()
        self.room.set_hint_text(self.room_generator.get_room_text(0))
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.pause_menu.reset()
        self.cooldown_window.reset()
        self.health_window.reset()
        self.set_windows()
        self.dt = 0
        self.clock.tick()

    def set_language(self, language):
        self.room_generator.set_language(language)
        self.upgrade_menu.set_language(language)
        self.victory_menu.set_language(language)
        self.pause_menu.set_language(language)
        self.health_window.set_language(language)
        self.cooldown_window.set_language(language)

    def set_windows(self):
        self.health_window.set(self.player.state,
                               self.player.health,
                               self.player.max_health)
        self.cooldown_window.set(self.player.gun.cooldown_time,
                                 self.player.superpower.cooldown_time)

    def update_windows(self, dt):
        self.health_window.update(dt)
        self.cooldown_window.update(dt, self.player, self.transportation)

    def handle(self, e_type, e_key):
        if e_key == pg.K_a:
            self.player.moving_left = (e_type == pg.KEYDOWN)
        elif e_key == pg.K_d:
            self.player.moving_right = (e_type == pg.KEYDOWN)
        elif e_key == pg.K_w:
            self.player.moving_up = (e_type == pg.KEYDOWN)
        elif e_key == pg.K_s:
            self.player.moving_down = (e_type == pg.KEYDOWN)
        elif e_key == pg.BUTTON_LEFT:
            self.player.shooting = (e_type == pg.MOUSEBUTTONDOWN)
        elif e_key == pg.K_SPACE:
            self.player.superpower.on = (e_type == pg.KEYDOWN)
        if (e_type == pg.KEYDOWN and
                e_key in [pg.K_p, pg.K_ESCAPE]
                and not self.transportation):
            self.run_pause_menu()

    def init_key_handlers(self):
        self.key_handlers[pg.K_a].append(self.handle)
        self.key_handlers[pg.K_d].append(self.handle)
        self.key_handlers[pg.K_w].append(self.handle)
        self.key_handlers[pg.K_s].append(self.handle)
        self.key_handlers[pg.BUTTON_LEFT].append(self.handle)
        self.key_handlers[pg.K_SPACE].append(self.handle)
        self.key_handlers[pg.K_p].append(self.handle)
        self.key_handlers[pg.K_ESCAPE].append(self.handle)

    def handle_events(self):
        """Main events handler that handles pygame events
        during the actual game.
        """
        old_time = pg.time.get_ticks()

        for event in pg.event.get():
            if event.type in [pg.KEYDOWN, pg.KEYUP]:
                for handler in self.key_handlers[event.key]:
                    handler(event.type, event.key)
            elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
                for handler in self.key_handlers[event.button]:
                    handler(event.type, event.button)
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        # Usually handle_events method takes 0-2 milliseconds to execute,
        # but if the execution time was more than 10 milliseconds, that means
        # that most likely the display was inactive for some time.
        # In that case we don't want this time to be taken into account for
        # updating game objects, so additional clock.tick() method is called.
        if pg.time.get_ticks() - old_time > 10:
            self.clock.tick()

    def handle_bubble_eating(self):
        self.sound_player.reset()
        for i, bubble in enumerate(self.room.bubbles):
            if self.player.collide_bubble(bubble.x, bubble.y):
                self.player.handle_bubble_eating(bubble.health)
                self.health_window.activate(self.player.health, self.player.state)
                self.room.bubbles[i] = None
                self.sound_player.play_sound(BUBBLE_DEATH)
        self.room.bubbles = list(filter(lambda b: b is not None, self.room.bubbles))
        if self.player.is_ready_to_upgrade:
            self.handle_player_upgrade()

    def handle_player_downgrade(self):
        self.player.downgrade()
        self.set_windows()
        self.pause_menu.set_stats_window(self.player.state)
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.room.set_gravity_radius(self.player.bg_radius)

    def handle_player_upgrade(self):
        if self.player.in_latest_state:
            self.upgrade_menu.run(self.player.get_next_states(), self.screen)
            self.clock.tick()
            self.player.upgrade(True, self.upgrade_menu.chosen_state)
        else:
            self.player.upgrade(False)

        self.set_windows()
        self.pause_menu.set_stats_window(self.player.state)
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.room.set_gravity_radius(self.player.bg_radius)

    def handle_enemy_injure(self, mob, bullet):
        """
        Method updates bullet's hit-flag, updates enemy's state according to damage,
        adds a hit-effect to the list of effects and plays an appropriate sound.

        """
        if isinstance(bullet, DrillingBullet):
            if mob in bullet.attacked_mobs:
                return
            bullet.attacked_mobs.append(mob)
        else:
            bullet.hit_the_target = True

        mob.handle_injure(bullet.damage)

        add_effect(bullet.hit_effect, self.room.top_effects, bullet.x, bullet.y)

        if isinstance(bullet, ExplodingBullet):
            self.room.handle_bullet_explosion(bullet.x, bullet.y)
            self.camera.start_shaking(250)

        sound = PLAYER_BULLET_HIT if mob.health > 0 else MOB_DEATH
        self.sound_player.play_sound(sound)

    def handle_mobs_collisions(self):
        """
        Handles collisions between objects:
            mobs and player's bullets;
            mobs and player's shurikens;
            mobs and player's homing bullets;
            mobs' homing bullets and player's bullets.

        """
        self.sound_player.reset()

        mob_collide_bullet = Mob.collide_bullet
        for b in self.player.bullets:
            for mob in self.room.mobs:
                if mob_collide_bullet(mob, b.x, b.y, b.radius) and mob.health > 0:
                    self.handle_enemy_injure(mob, b)
                    break

            if not b.hit_the_target:
                for h_b in self.room.homing_bullets:
                    if h_b.collide_bullet(b.x, b.y, b.radius) and h_b.health > 0:
                        self.handle_enemy_injure(h_b, b)
                        break

        for s in self.player.shurikens:
            for mob in self.room.mobs:
                if mob_collide_bullet(mob, s.x, s.y, s.radius) and mob.health > 0:
                    self.handle_enemy_injure(mob, s)
                    break

        for b in self.player.homing_bullets:
            for mob in self.room.mobs:
                if mob_collide_bullet(mob, b.x, b.y, b.radius) and mob.health > 0:
                    self.handle_enemy_injure(mob, b)
                    break

    def handle_player_injure(self, bullet):
        """
        Method updates bullet's hit-flag, updates player's state according to damage,
        Adds a hit-effect to the list of effects and plays an appropriate sound.

        """
        bullet.hit_the_target = True

        self.player.handle_injure(bullet.damage)

        add_effect(bullet.hit_effect, self.room.top_effects, bullet.x, bullet.y)

        if not self.player.armor_on:
            self.sound_player.play_sound(PLAYER_INJURE)

    def handle_player_collisions(self):
        """
        Handles collisions between objects:
            player and mobs' bullets;
            player and mobs' homing bullets.
            player's homing bullets and mobs' bullets.

        If player's health becomes < 0, calls a 'downgrade_player' method.

        """
        self.sound_player.reset()

        player_collide_bullet = Player.collide_bullet
        for b in self.room.bullets:
            if (not self.player.invisible and
                    player_collide_bullet(self.player, b.x, b.y, b.radius)):
                self.handle_player_injure(b)
                break

            if not b.hit_the_target:
                for h_b in self.player.homing_bullets:
                    if h_b.collide_bullet(b.x, b.y, b.radius) and h_b.health > 0:
                        self.handle_enemy_injure(h_b, b)
                        break

        for b in self.room.homing_bullets:
            if (not self.player.invisible and
                    player_collide_bullet(self.player, b.x, b.y, b.radius)):
                self.handle_player_injure(b)
                break

        if self.player.health < 0 and self.player.level > 0:
            self.handle_player_downgrade()

    def update_transportation(self, dt):
        """ Update all objects during transportation. """
        self.player.move(self.player.vel_x * dt, self.player.vel_y * dt)
        self.player.update_body(dt)
        self.player.update_shurikens(dt, [])
        self.player.update_frozen_state(dt)
        self.player.gun.update_time(dt)
        self.player.superpower.update_time(dt)
        self.camera.update(*self.player.pos, dt)
        self.room.set_screen_rect(self.player.pos)
        self.room.update_new_mobs(*self.player.pos, dt)
        self.update_windows(dt)

    def draw_transportation(self, time, dx, dy):
        """ Draw all objects during transportation. """
        offset_new = self.camera.offset
        offset_old = (self.camera.dx - dx, self.camera.dy - dy)

        self.bg_environment.draw_transportation(self.screen, offset_new,
                                                offset_old, time)
        self.room.draw_boss_skeleton(self.screen, *offset_new)
        self.room.draw_hint_text(self.screen, *offset_new)
        self.room.draw_bubbles(self.screen, *offset_new)
        self.room.draw_bombs(self.screen, *offset_new)
        self.player.draw(self.screen, *offset_new)
        self.room.draw_mobs(self.screen, *offset_new)
        self.room.draw_new_mobs(self.screen, *offset_new)
        self.room.draw_bullets(self.screen, *offset_new)

        self.bg_environment.draw_room_glares(self.screen, *offset_new)
        self.bg_environment.draw_room_glares(self.screen, *offset_old)

        self.health_window.draw(self.screen)
        self.cooldown_window.draw(self.screen)

    def run_transportation(self, dx, dy):
        time = dt = 0
        while time < TRANSPORTATION_TIME and self.running:
            self.handle_events()
            self.update_transportation(dt)
            self.draw_transportation(time, dx, dy)
            pg.display.update()
            dt = self.clock.tick()
            self.fps_manager.update(dt)
            time += dt

    def get_offset_and_destination(self, direction):
        """
        Method returns offset of all objects in previous room
        and the player's destination during transportation.

        """
        radius = ROOM_RADIUS - self.player.radius - 1/4 * SCR_H

        if direction == 'UP':
            offset = (0, DIST_BETWEEN_ROOMS)
            destination = np.array([SCR_W2, SCR_H2 + radius])
        elif direction == 'DOWN':
            offset = (0, -DIST_BETWEEN_ROOMS)
            destination = np.array([SCR_W2, SCR_H2 - radius])
        elif direction == 'LEFT':
            offset = (DIST_BETWEEN_ROOMS, 0)
            destination = np.array([SCR_W2 + radius, SCR_H2])
        else:
            offset = (-DIST_BETWEEN_ROOMS, 0)
            destination = np.array([SCR_W2 - radius, SCR_H2])

        return offset, destination

    def transport_player(self, direction):
        self.transportation = True

        self.room_generator.save(self.room.mobs)
        self.room_generator.update(direction, self.player)

        self.room.set_hint_text(self.room_generator.get_room_text(self.player.level))
        self.room.new_mobs = self.room_generator.get_mobs()
        self.room.update_boss_state()

        self.pause_menu.update_map_data(self.room_generator.cur_room,
                                        self.room.boss_state)

        offset, destination = self.get_offset_and_destination(direction)
        self.room.move_objects(offset)
        self.player.move(*offset)
        self.player.move_bullets(offset)
        self.camera.stop_shaking()
        self.camera.update(*self.player.pos, 0)

        distance = hypot(*(self.player.pos - destination))
        player_vel = distance / TRANSPORTATION_TIME
        angle = calculate_angle(*self.player.pos, *destination)

        self.player.set_transportation_vel(angle, player_vel)

        self.bg_environment.set_player_trace(*self.player.pos, distance, angle)
        self.bg_environment.set_destination_circle(destination)

        self.run_transportation(*offset)

        self.room.set_params_after_transportation()
        self.player.set_params_after_transportation()
        self.clock.tick()
        self.transportation = False

    def get_direction(self, offset):
        """
        :param offset: player's offset relative to the center of the room
        :return: direction of transportation
        """
        if offset == 0:
            direction = 'LEFT'
        elif (self.camera.dx / offset) ** 2 <= 0.5:
            direction = 'UP' if self.camera.dy < 0 else 'DOWN'
        else:
            direction = 'RIGHT' if self.camera.dx > 0 else 'LEFT'
        return direction

    def check_transportation(self):
        """Checks if player is defeated or outside the room.
        If yes, determines the direction of transportation
        and transports player to the next room.

        """
        offset = hypot(*self.camera.offset)
        if self.player.defeated or offset > ROOM_RADIUS:
            direction = self.get_direction(offset)
            self.transport_player(direction)

    def update(self):
        self.handle_bubble_eating()
        self.handle_mobs_collisions()
        self.handle_player_collisions()
        self.player.update(self.dt, self.room.mobs, self.room.top_effects,
                           self.room.bottom_effects, self.camera,
                           self.sound_player)
        self.camera.update(*self.player.pos, self.dt)
        self.room.update(self.player.pos,  self.dt)
        if self.room.boss_defeated:
            self.running = False
            self.run_victory_menu()
        else:
            self.update_windows(self.dt)
            self.check_transportation()

    def draw_background(self, surface):
        self.bg_environment.draw_bg(surface)
        self.bg_environment.draw_room_bg(surface, *self.camera.offset)
        self.bg_environment.draw_player_halo(surface, self.camera.offset)
        self.room.draw_boss_skeleton(surface, *self.camera.offset)
        self.room.draw_hint_text(surface, *self.camera.offset)
        self.room.draw_bottom_effects(surface, *self.camera.offset)

    def draw_foreground(self):
        self.room.draw_bubbles(self.screen, *self.camera.offset)
        self.room.draw_bombs(self.screen, *self.camera.offset)
        self.player.draw(self.screen, *self.camera.offset)
        self.room.draw_mobs(self.screen, *self.camera.offset)
        self.room.draw_bullets(self.screen, *self.camera.offset)
        self.room.draw_top_effects(self.screen, *self.camera.offset)
        self.bg_environment.draw_room_glares(self.screen, *self.camera.offset)
        self.health_window.draw(self.screen)
        self.cooldown_window.draw(self.screen)

    def draw(self):
        self.draw_background(self.screen)
        self.draw_foreground()
        pg.display.update()

    def run_game(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.dt = self.clock.tick()
            self.fps_manager.update(self.dt)

    def update_pause_menu(self):
        """Updates the background objects and all the pause menu items.
        Since the objects in the background do not move or
        interact with each other while the pause menu is running,
        only their bodies are updated.
        """
        if isinstance(self.player.superpower, Ghost):
            self.player.superpower.update_body(self.player.body)
        self.player.update_body(self.dt)
        for mob in self.room.mobs:
            mob.update_body(self.room.screen_rect, self.dt, self.player.pos)
        for bubble in self.room.bubbles:
            bubble.update_body(self.dt)
        for bullet in self.player.bullets:
            bullet.update_body(self.dt)
        for shuriken in self.player.shurikens:
            if shuriken.is_orbiting:
                shuriken.update_polar_coords(*self.player.pos, self.dt)
        for bullet in self.room.bullets:
            bullet.update_body(self.dt)
        self.pause_menu.update(self.dt)

    def update_victory_menu(self):
        if isinstance(self.player.superpower, Ghost):
            self.player.superpower.update_body(self.player.body)
            self.player.update_body(self.dt)
        for bubble in self.room.bubbles:
            bubble.update_body(self.dt)
        self.victory_menu.update(self.dt)

    def draw_pause_menu(self):
        """Draws all objects in the background and pause menu items. """
        self.screen.blit(self.pause_menu.bg_surface, (0, 0))
        self.draw_foreground()
        self.pause_menu.draw(self.screen)
        pg.display.update()

    def draw_victory_menu(self):
        """Draws all objects in the background and victory menu items. """
        self.screen.blit(self.victory_menu.bg_surface, (0, 0))
        self.draw_foreground()
        self.victory_menu.draw(self.screen)

    def run_start_menu(self):
        self.start_menu.run(self.screen, self.fps_manager)
        self.set_language(self.start_menu.language)

    def run_pause_menu(self):
        self.draw_background(self.pause_menu.bg_surface)
        self.player.stop_moving()
        self.pause_menu.set_params_before_running()
        while self.pause_menu.running:
            self.pause_menu.handle_events()
            self.clock.tick()
            self.update_pause_menu()
            self.draw_pause_menu()
            self.dt = self.clock.tick()
            self.fps_manager.update(self.dt)
        self.running = self.pause_menu.game_running

    def run_victory_menu(self):
        """Victory menu loop which starts after the Boss is defeated. """
        self.draw_background(self.victory_menu.bg_surface)
        self.victory_menu.running = True
        while self.victory_menu.running:
            self.victory_menu.handle_events()
            self.clock.tick()
            self.update_victory_menu()
            self.draw_victory_menu()
            self.dt = self.clock.tick()
            self.fps_manager.update(self.dt)
        self.running = False

    def run(self):
        """Main game loop. """
        while True:
            self.sound_player.play_music(START_MUSIC)
            self.run_start_menu()
            self.reset_data()
            self.sound_player.play_music(GAME_MUSIC)
            self.run_game()

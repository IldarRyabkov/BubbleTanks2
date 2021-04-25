import pygame as pg
import sys
import numpy as np
from math import hypot
from collections import defaultdict

from data.paths import (GAME_MUSIC, START_MUSIC, PLAYER_BULLET_HIT,
                        MOB_DEATH, BUBBLE_DEATH, PLAYER_INJURE)
from data.config import *
from background_environment import BackgroundEnvironment
from objects.player import Player
from camera import Camera
from room import Room
from sound_player import SoundPlayer
from level_generator import LevelGenerator
from menus.upgrade_menu import UpgradeMenu
from menus.victory_menu import VictoryMenu
from menus.start_menu import StartMenu
from menus.pause_menu import PauseMenu
from gui.health_window import HealthWindow
from gui.cooldown_window import CooldownWindow
from special_effects import add_effect
from utils import calculate_angle


class Game:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.sound_player = SoundPlayer()
        self.running = True
        self.transportation = False
        self.dt = 0
        self.clock = pg.time.Clock()
        self.bg_environment = BackgroundEnvironment()
        self.player = Player()
        self.key_handlers = None
        self.camera = Camera()
        self.room = Room()
        self.level_generator = LevelGenerator()
        self.start_menu = StartMenu()
        self.upgrade_menu = UpgradeMenu()
        self.victory_menu = VictoryMenu()
        self.pause_menu = PauseMenu()
        self.health_window = HealthWindow()
        self.cooldown_window = CooldownWindow()
        self.init_key_handlers()

    def show_fps(self):
        fps = str(int(self.clock.get_fps() / 2))
        pg.display.set_caption('FPS: %s' % fps)

    def reset_data(self):
        self.running = True
        self.transportation = False
        self.dt = 0
        self.player = Player()
        self.level_generator.reset()
        self.init_key_handlers()
        self.room.reset(new_game=True)
        self.room.set_text(self.level_generator.get_room_text())
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.pause_menu.reset()
        self.cooldown_window.reset()
        self.health_window.reset()
        self.set_windows()

    def set_windows(self):
        self.health_window.set(self.player.state,
                               self.player.health,
                               self.player.max_health)
        self.cooldown_window.set(self.player.gun.cooldown_time,
                                 self.player.superpower.cooldown_time)

    def update_windows(self, dt):
        self.health_window.update(dt)
        self.cooldown_window.update(dt, self.player)

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
            self.player.is_shooting = (e_type == pg.MOUSEBUTTONDOWN)
        elif e_key == pg.K_SPACE:
            self.player.superpower.on = (e_type == pg.KEYDOWN)
        if (e_type == pg.KEYDOWN and
                e_key in [pg.K_p, pg.K_ESCAPE]
                and not self.transportation):
            self.run_pause_menu()

    def init_key_handlers(self):
        self.key_handlers = defaultdict(list)
        self.key_handlers[pg.K_a].append(self.handle)
        self.key_handlers[pg.K_d].append(self.handle)
        self.key_handlers[pg.K_w].append(self.handle)
        self.key_handlers[pg.K_s].append(self.handle)
        self.key_handlers[pg.BUTTON_LEFT].append(self.handle)
        self.key_handlers[pg.K_SPACE].append(self.handle)
        self.key_handlers[pg.K_p].append(self.handle)
        self.key_handlers[pg.K_ESCAPE].append(self.handle)

    def handle_events(self):
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

    def handle_bubble_eating(self):
        self.sound_player.reset()
        eaten_bubbles = []
        for i, bubble in enumerate(self.room.bubbles):
            if self.player.collide_bubble(bubble.x, bubble.y):
                self.player.handle_bubble_eating(bubble.health)
                self.health_window.activate(self.player.health, self.player.state)
                eaten_bubbles.append(i)
                self.sound_player.play_sound(BUBBLE_DEATH)
        eaten_bubbles.reverse()
        for index in eaten_bubbles:
            self.room.bubbles.pop(index)
        if self.player.is_ready_to_upgrade():
            self.handle_player_upgrade()

    def handle_player_downgrade(self):
        self.player.downgrade()
        self.set_windows()
        self.pause_menu.set_stats_window(self.player.state)
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.room.set_gravity_radius(self.player.bg_radius)

    def handle_player_upgrade(self):
        if self.player.in_latest_state():
            self.upgrade_menu.run(self.player.get_next_states(), self.screen)
            self.clock.tick()
            self.player.upgrade(True, self.upgrade_menu.chosen_state)
        else:
            self.player.upgrade(False)

        self.set_windows()
        self.pause_menu.set_stats_window(self.player.state)
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.room.set_gravity_radius(self.player.bg_radius)

    def handle_mob_injure(self, mob, bullet):
        """
        Method updates bullet's hit-flag, updates mob's state according to damage,
        Adds a hit-effect to the list of effects and plays an appropriate sound.

        """
        bullet.hit_the_target = True

        mob.handle_injure(bullet.damage)

        add_effect(bullet.hit_effect, self.room.top_effects, bullet.x, bullet.y)

        if bullet.exploding:
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

        for b in self.player.bullets:
            for mob in self.room.mobs:
                if mob.collide_bullet(b.x, b.y) and mob.health > 0:
                    self.handle_mob_injure(mob, b)
                    break

            if not b.hit_the_target:
                for h_b in self.room.homing_bullets:
                    if h_b.collide_bullet(b.x, b.y) and h_b.health > 0:
                        self.handle_mob_injure(h_b, b)
                        break

        for s in self.player.shurikens:
            for mob in self.room.mobs:
                if mob.collide_bullet(s.x, s.y) and mob.health > 0:
                    self.handle_mob_injure(mob, s)
                    break

        for b in self.player.homing_bullets:
            for mob in self.room.mobs:
                if mob.collide_bullet(b.x, b.y) and mob.health > 0:
                    self.handle_mob_injure(mob, b)
                    break

    def handle_player_injure(self, bullet):
        """
        Method updates bullet's hit-flag, updates player's state according to damage,
        Adds a hit-effect to the list of effects and plays an appropriate sound.

        """
        bullet.hit_the_target = True

        self.player.handle_injure(bullet.damage)

        add_effect(bullet.hit_effect, self.room.top_effects, bullet.x, bullet.y)

        if not self.player.armor_on[0]:
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

        for b in self.room.bullets:
            if not self.player.invisible[0] and self.player.collide_bullet(b.x, b.y):
                self.handle_player_injure(b)
                break

            if not b.hit_the_target:
                for h_b in self.player.homing_bullets:
                    if h_b.collide_bullet(b.x, b.y) and h_b.health > 0:
                        self.handle_mob_injure(h_b, b)
                        break

        for b in self.room.homing_bullets:
            if not self.player.invisible[0] and self.player.collide_bullet(b.x, b.y):
                self.handle_player_injure(b)
                break

        if self.player.health < 0:
            self.handle_player_downgrade()

    def update_transportation(self, dt):
        """ Update all objects during transportation. """
        self.player.move(self.player.vel_x * dt, self.player.vel_y * dt)
        self.player.update(dt, self.room.mobs, self.room.top_effects,
                           self.room.bottom_effects, self.camera,
                           self.sound_player, transportation=True)
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
        self.room.draw_text(self.screen, *offset_new)
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
        time, dt = 0, 0
        while time < TRANSPORTATION_TIME and self.running:
            self.handle_events()
            self.clock.tick()

            self.update_transportation(dt)

            self.draw_transportation(time, dx, dy)

            pg.display.update()

            dt = self.clock.tick()
            time += dt
            self.show_fps()

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

        self.level_generator.update(self.room.encode_mobs(self.room.mobs),
                                    direction, self.player, self.pause_menu)
        self.level_generator.set_room(self.room)

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

        self.room.reset()
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
        if self.room.game_is_over():
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
        self.room.draw_text(surface, *self.camera.offset)
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
            self.clock.tick()
            self.update()
            self.draw()
            self.dt = self.clock.tick()
            self.show_fps()

    def run_start_menu(self):
        self.start_menu.run(self.screen)
        if self.start_menu.language_changed:
            self.level_generator.set_language(self.start_menu.language)
            self.upgrade_menu.set_language(self.start_menu.language)
            self.victory_menu.set_language(self.start_menu.language)
            self.pause_menu.set_language(self.start_menu.language)
            self.health_window.set_language(self.start_menu.language)
            self.cooldown_window.set_language(self.start_menu.language)

    def run_pause_menu(self):
        self.draw_background(self.pause_menu.bg_surface)
        self.player.stop_moving()
        self.pause_menu.run(self.screen, self.player,
                            self.room.bubbles, self.room.mobs,
                            self.room.bullets, self.draw_foreground,
                            self.sound_player.sounds)
        self.running = self.pause_menu.game_running
        self.clock.tick()

    def run_victory_menu(self):
        self.draw_background(self.victory_menu.bg_surface)
        self.victory_menu.run(self.screen, self.player,
                                self.room.bubbles, self.draw_foreground)
        self.running = False
        self.clock.tick()

    def run(self):
        while True:
            self.sound_player.play_music(START_MUSIC)
            self.run_start_menu()
            self.reset_data()
            self.sound_player.play_music(GAME_MUSIC)
            self.run_game()

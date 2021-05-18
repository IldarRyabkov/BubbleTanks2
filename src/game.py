import pygame as pg
import sys
import numpy as np
from math import hypot
from collections import defaultdict
import platform


from data.cursor import CURSOR
from data.paths import *
from data.scripts import load_language

from menus.upgrade_menu import UpgradeMenu
from menus.victory_menu import VictoryMenu
from menus.main_menu import MainMenu
from menus.pause_menu import PauseMenu

from gui.health_window import HealthWindow
from gui.cooldown_window import CooldownWindow

from player import Player
from bullets import *
from constants import *
from background_environment import BackgroundEnvironment
from camera import Camera
from room import Room
from sound_player import SoundPlayer
from mob_generator import MobGenerator
from fps_manager import FPSManager
from superpowers import Ghost
from special_effects import add_effect
from utils import calculate_angle, H



class Game:
    """The main class, which is the core of the game and manages all game objects."""
    def __init__(self):
        # Initialize all imported pygame modules.
        pg.init()

        # Set a custom mouse cursor that will be better seen on a blue background.
        cursor = pg.cursors.compile(CURSOR, black='.', white='X')
        pg.mouse.set_cursor((32, 32), (0, 0), *cursor)

        # Set the types of events that are allowed to appear in the event queue.
        # This will improve the performance of the game.
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP,
                              pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP])

        # Try to make sure the game will display correctly on high DPI monitors on Windows.
        if platform.system() == 'Windows':
            from ctypes import windll
            try:
                windll.user32.SetProcessDPIAware()
            except AttributeError:
                pass

        self.screen = pg.display.set_mode(SCR_SIZE, flags=pg.NOFRAME)

        self.running = True
        self.language = load_language()
        self.transportation = False

        self.sound_player = SoundPlayer()
        self.fps_manager = FPSManager()
        self.clock = pg.time.Clock()
        self.bg_environment = BackgroundEnvironment(self)
        self.camera = Camera()
        self.player = Player(self)
        self.room = Room()
        self.mob_generator = MobGenerator()

        self.main_menu = MainMenu(self)
        self.upgrade_menu = UpgradeMenu(self)
        self.victory_menu = VictoryMenu(self)
        self.pause_menu = PauseMenu(self)

        self.health_window = HealthWindow(self)
        self.cooldown_window = CooldownWindow()
        self.set_windows()

        self.key_handlers = defaultdict(list)
        self.init_key_handlers()

    def set_language(self, lang):
        self.bg_environment.set_language(lang)
        self.upgrade_menu.set_language(lang)
        self.victory_menu.set_language(lang)
        self.pause_menu.set_language(lang)
        self.cooldown_window.set_language(lang)

    def reset_data(self):
        """Method is called when the game has started. Resets
        all game objects and game parameters.
        """
        self.player.reset()
        self.mob_generator.reset()
        self.bg_environment.reset()
        self.health_window.reset()
        self.cooldown_window.reset()
        self.set_windows()
        self.room.reset()
        self.pause_menu.reset()
        self.victory_menu.reset()
        self.running = True
        self.transportation = False
        self.clock.tick()

        # Set the language for all game objects AFTER their parameters are reset
        self.set_language(self.language)

    def set_windows(self):
        self.health_window.set(self.player.tank,
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
        if e_type ==  pg.KEYDOWN and e_key in [pg.K_p, pg.K_ESCAPE]  and not self.transportation:
            self.pause_menu.run()

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
        eaten_bubbles = 0
        for i, bubble in enumerate(self.room.bubbles):
            if self.player.collide_bubble(bubble.x, bubble.y):
                self.player.handle_bubble_eating(bubble.health)
                self.health_window.activate(self.player.health, self.player.level)
                self.room.bubbles[i] = None
                eaten_bubbles += 1
        if eaten_bubbles:
            self.pause_menu.update_counter(1, eaten_bubbles)
            self.room.bubbles = list(filter(lambda b: b is not None, self.room.bubbles))
            self.sound_player.play_sound(BUBBLE_DEATH)
        if self.player.is_ready_to_upgrade:
            self.handle_player_upgrade()

    def handle_player_downgrade(self):
        self.player.downgrade()
        self.set_windows()
        self.pause_menu.set_tank_stats(self.player.tank)
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.room.set_gravity_radius(1.3 * self.player.bg_radius)

    def handle_player_upgrade(self):
        if self.player.last_tank_in_history:
            self.upgrade_menu.run()
            if self.running:
                self.player.upgrade(True, self.upgrade_menu.chosen_tank)
                if self.player.level == 2:
                    self.bg_environment.prepare_superpower_hint()
        else:
            self.player.upgrade(False)

        self.set_windows()
        self.pause_menu.set_tank_stats(self.player.tank)
        self.bg_environment.set_player_halo(self.player.bg_radius)
        self.room.set_gravity_radius(1.3 * self.player.bg_radius)

    def handle_enemy_injure(self, mob, bullet):
        """
        Method updates bullet's hit-flag, updates enemy's state according to damage,
        adds a hit-effect to the list of effects and plays an appropriate sound.

        """
        if isinstance(bullet, (DrillingBullet, AirBullet)):
            if mob in bullet.attacked_mobs:
                return
            bullet.attacked_mobs.append(mob)
            if isinstance(bullet, AirBullet):
                self.room.add_bubbles((bullet.x, bullet.y), bullet.bubbles)
        else:
            bullet.hit_the_target = True

        mob.handle_injure(bullet.damage)

        add_effect(bullet.hit_effect, self.room.top_effects, bullet.x, bullet.y)

        if isinstance(bullet, ExplodingBullet):
            self.room.handle_bullet_explosion(bullet.x, bullet.y)
            self.camera.start_shaking(250)

        if mob.health <= 0:
            self.pause_menu.update_counter(0, 1)
            if not isinstance(mob, HomingMissile):
                self.sound_player.play_sound(MOB_DEATH)
        else:
            self.sound_player.play_sound(PLAYER_BULLET_HIT, False)

    def handle_mobs_collisions(self):
        """
        Handles collisions between objects:
            mobs and player's bullets;
            mobs and player's shurikens;
            mobs and player's homing bullets;
            mobs' homing bullets and player's bullets.

        """
        self.sound_player.unlock()

        for b in self.player.bullets:
            for mob in self.room.mobs:
                if mob.collide_bullet(b.x, b.y, b.radius) and mob.health > 0:
                    self.handle_enemy_injure(mob, b)
                    break

            if not b.hit_the_target:
                for h_b in self.room.homing_bullets:
                    if h_b.collide_bullet(b.x, b.y, b.radius) and h_b.health > 0:
                        self.handle_enemy_injure(h_b, b)
                        break

        for s in self.player.shurikens:
            for mob in self.room.mobs:
                if mob.collide_bullet(s.x, s.y, s.radius) and mob.health > 0:
                    self.handle_enemy_injure(mob, s)
                    break

        for b in self.player.homing_bullets:
            for mob in self.room.mobs:
                if mob.collide_bullet(b.x, b.y, b.radius) and mob.health > 0:
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
            self.sound_player.play_sound(PLAYER_INJURE, False)

    def handle_player_collisions(self):
        """
        Handles collisions between objects:
            player and mobs' bullets;
            player and mobs' homing bullets.
            player's homing bullets and mobs' bullets.

        If player's health becomes < 0, calls a 'downgrade_player' method.

        """
        self.sound_player.unlock()

        for b in self.room.bullets:
            if (not self.player.invisible and
                    self.player.collide_bullet(b.x, b.y, b.radius)):
                self.handle_player_injure(b)
                break

            if not b.hit_the_target:
                for h_b in self.player.homing_bullets:
                    if h_b.collide_bullet(b.x, b.y, b.radius) and h_b.health > 0:
                        self.handle_enemy_injure(h_b, b)
                        break

        for b in self.room.homing_bullets:
            if (not self.player.invisible and
                    self.player.collide_bullet(b.x, b.y, b.radius)):
                self.handle_player_injure(b)
                break

        if self.player.health < 0 and self.player.level > 0:
            self.handle_player_downgrade()

    def update_transportation(self, dt):
        """ Update all objects during transportation. """
        self.player.update_during_transportation(dt)
        self.camera.update(*self.player.pos, dt)
        self.room.set_screen_rect(self.player.pos)
        self.room.update_new_mobs(*self.player.pos, dt)
        self.update_windows(dt)

    def draw_transportation(self, time, dist_between_rooms):
        """ Draw all objects during transportation. """
        offset_new = self.camera.offset
        offset_old = self.camera.offset - dist_between_rooms

        self.bg_environment.draw_bg(self.screen)
        self.bg_environment.draw_room_bg(self.screen, *offset_new)
        self.bg_environment.draw_room_bg(self.screen, *offset_old)
        self.bg_environment.draw_hint(self.screen, *offset_old)
        self.bg_environment.draw_new_hint(self.screen, *offset_new)
        self.bg_environment.draw_destination_circle(self.screen, *offset_new)
        self.bg_environment.draw_player_trace(self.screen, *offset_new, time)
        self.bg_environment.draw_player_halo(self.screen, offset_old, offset_new)
        self.bg_environment.draw_boss_skeleton(self.screen, *offset_new, True)
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

    def run_transportation(self, dist_between_rooms):
        self.sound_player.play_sound(WATER_SPLASH)
        time = dt = 0
        while time < TRANSPORTATION_TIME and self.running:
            self.handle_events()
            self.update_transportation(dt)
            self.draw_transportation(time, dist_between_rooms)
            pg.display.update()
            dt = self.clock.tick()
            self.fps_manager.update(dt)
            time += dt

    def get_destination_pos(self, direction):
        """Method returns player's destination point during transportation. """
        distance = ROOM_RADIUS - self.player.radius - H(240)  # distance from center of the next room to the player's destination point
        destination_pos = np.array([SCR_W2, SCR_H2]) - distance * direction
        return destination_pos

    def transport_player(self, direction):
        """Algorithm of transportation of the player. """
        self.transportation = True

        # Save mobs from previous room and generate mobs for the next room
        self.mob_generator.save_mobs(self.room.mobs)
        self.mob_generator.generate_mobs(direction, self.player)

        # Save new generated mobs
        self.room.new_mobs = self.mob_generator.load_mobs()

        # Set new boss disposition
        self.bg_environment.set_new_boss_disposition(self.mob_generator.cur_room,
                                                     self.room.new_mobs)
        # Update map in pause menu
        self.pause_menu.update_map_data(self.mob_generator.cur_room,
                                        self.bg_environment.new_boss_disposition)
        # Set new hint text for the player
        self.bg_environment.set_next_hint()

        # Now we want the coordinates of all objects to be calculated relative
        # to the center of the new room. Therefore, we calculate the distance
        # between the centers of the rooms and shift all objects by this distance.
        dist_between_rooms = -DIST_BETWEEN_ROOMS * direction
        self.player.move(*dist_between_rooms)
        self.player.move_bullets(dist_between_rooms)
        self.room.move_objects(dist_between_rooms)

        # Stabilize camera and adjust it to the new position of the player.
        self.camera.stop_shaking()
        self.camera.update(*self.player.pos, 0)

        # Now we want to calculate the coordinates of the player's destination in order to calculate
        # the angle and length of player's velocity vector during transportation.
        destination_pos = self.get_destination_pos(direction)

        # distance between player's pos and player's destination pos
        distance = hypot(*(self.player.pos - destination_pos))

        # Set player's velocity during transportation
        velocity = distance / TRANSPORTATION_TIME
        angle = calculate_angle(*self.player.pos, *destination_pos)
        self.player.set_transportation_vel(angle, velocity)

        # Set some background effects during transportation
        self.bg_environment.set_player_trace(*self.player.pos, distance, angle)
        self.bg_environment.set_destination_circle(destination_pos)

        # Run transportation loop
        self.run_transportation(dist_between_rooms)

        # After transportation is done some parameters need to be reset
        self.room.set_params_after_transportation()
        self.player.set_params_after_transportation()
        self.bg_environment.set_params_after_transportation()

        self.clock.tick()
        self.transportation = False

    def get_direction(self, offset):
        """ This method determines the direction of transportation
        of player so that he is transported to the nearest room.
        """
        if offset == 0:
            return np.array([-1, 0])

        if (self.camera.dx / offset) ** 2 <= 0.5:
            return np.array([0, -1] if self.camera.dy < 0 else [0, 1])

        return np.array([1, 0] if self.camera.dx > 0 else [-1, 0])

    def check_transportation(self):
        """Checks if player is defeated or outside the room.
        If yes, determines the direction of transportation
        and transports player to the next room.

        """
        player_offset = hypot(*self.camera.offset)
        if self.player.defeated or player_offset > ROOM_RADIUS:
            direction = self.get_direction(player_offset)
            self.transport_player(direction)

    def update(self, dt):
        self.handle_bubble_eating()
        self.handle_mobs_collisions()
        self.handle_player_collisions()
        self.player.update(dt)
        self.camera.update(*self.player.pos, dt)
        self.room.update(self.player.pos,  dt)
        if self.room.boss_defeated(self.bg_environment.boss_disposition):
            self.running = False
            self.victory_menu.run()
        else:
            self.update_windows(dt)
            self.check_transportation()

    def draw_background(self, surface):
        """Draw all entities that should be drawn below player, mobs, bullets etc. """
        self.bg_environment.draw_bg(surface)
        self.bg_environment.draw_room_bg(surface, *self.camera.offset)
        self.bg_environment.draw_player_halo(surface, self.camera.offset)
        self.bg_environment.draw_hint(surface, *self.camera.offset)
        self.bg_environment.draw_boss_skeleton(surface, *self.camera.offset)
        self.room.draw_bottom_effects(surface, *self.camera.offset)

    def draw_foreground(self):
        """Foreground includes player, mobs, bullets,
        bubbles, popup windows and some effects.
        """
        self.room.draw_bubbles(self.screen, *self.camera.offset)
        self.room.draw_bombs(self.screen, *self.camera.offset)
        self.player.draw(self.screen, *self.camera.offset)
        self.room.draw_mobs(self.screen, *self.camera.offset)
        self.room.draw_bullets(self.screen, *self.camera.offset)
        self.room.draw_top_effects(self.screen, *self.camera.offset)
        self.bg_environment.draw_room_glares(self.screen, *self.camera.offset)
        self.health_window.draw(self.screen)
        self.cooldown_window.draw(self.screen)

    def update_scaling_objects(self, dt):
        """Method is called when Pause menu/Victory menu is running.
        It updates the sizes of mobs, player, bullets, etc.,
        animating them in the background in the Pause menu/Victory menu.
        """
        if isinstance(self.player.superpower, Ghost):
            self.player.superpower.update_body(self.player.body)
        self.player.update_body(dt)
        for mob in self.room.mobs:
            mob.update_body(self.room.rect, dt, self.player.pos)
        for bubble in self.room.bubbles:
            bubble.update_body(dt)
        for bullet in self.player.bullets:
            bullet.update_body(dt)
        for shuriken in self.player.shurikens:
            if shuriken.is_orbiting:
                shuriken.update_polar_coords(*self.player.pos, dt)
        for bullet in self.room.bullets:
            bullet.update_body(dt)

    def run_game(self):
        """ Game loop that starts when the main menu is closed. """
        self.sound_player.play_music(GAME_MUSIC)
        self.clock.tick()
        while self.running:
            self.draw_background(self.screen)
            self.draw_foreground()
            pg.display.update()
            dt = self.clock.tick()
            self.fps_manager.update(dt)
            self.update(dt)
            self.handle_events()

    def run(self):
        """Main game loop. """
        while True:
            self.main_menu.run()
            self.reset_data()
            self.run_game()


__all__ = ["Game"]

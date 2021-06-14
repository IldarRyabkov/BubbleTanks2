import pygame as pg
import sys
import numpy as np
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

from .player import Player
from .bullets import *
from .background_environment import BackgroundEnvironment
from .camera import Camera
from .room import Room
from .sound_player import SoundPlayer
from .mob_generator import MobGenerator
from .fps_manager import FPSManager
from .superpowers import Ghost
from .bubble import Bubble
from .special_effects import *
from .utils import *


class Game:
    """The main class, which is the core of the game and manages all game objects."""
    def __init__(self, screen):
        self.screen = screen
        self.language = load_language()
        self.running = True
        self.pause = False
        self.transportation = False

        self.sound_player = SoundPlayer()
        self.fps_manager = FPSManager()
        self.clock = pg.time.Clock()
        self.bg_environment = BackgroundEnvironment(self)
        self.mob_generator = MobGenerator(self)
        self.player = Player(self)
        self.camera = Camera(self.player)
        self.room = Room(self)

        self.main_menu = MainMenu(self)
        self.upgrade_menu = UpgradeMenu(self)
        self.victory_menu = VictoryMenu(self)
        self.pause_menu = PauseMenu(self)

        self.health_window = HealthWindow(self)
        self.cooldown_window = CooldownWindow(self)

    def update_save_data(self):
        self.mob_generator.save_mobs(self.room.mobs)
        tank = self.player.tank
        tank_history = self.player.tanks_history
        health = self.player.health
        enemies_killed = self.pause_menu.stats_counters[0].text
        bubbles_collected = self.pause_menu.stats_counters[1].text
        visited_rooms = self.pause_menu.map_button.graph
        enemies = self.mob_generator.mobs_dict
        current_room = self.mob_generator.cur_room
        boss_generated = self.mob_generator.boss_generated
        boss_disposition = self.bg_environment.boss_disposition
        boss_position = self.bg_environment.boss_pos
        hints_history = self.bg_environment.hints_history
        save_name = self.main_menu.current_save
        update_save_file(save_name, tank, tank_history, health,
                         enemies_killed, bubbles_collected,
                         visited_rooms, enemies, current_room,
                         boss_generated, boss_disposition, boss_position,
                         hints_history)

    def set_data(self, data):
        self.player.set_data(data)
        self.mob_generator.set_data(data)
        self.bg_environment.set_data(data)
        self.health_window.set_data()
        self.cooldown_window.set_data()
        self.room.set_data(self.mob_generator.current_mobs)
        self.pause_menu.set_data(data)
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
                self.player.handle_bubble_eating(bubble.health)
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

    def handle_damage_to_enemy(self, enemy, bullet):
        enemy.handle_injure(bullet.damage)
        if enemy.health <= 0:
            self.pause_menu.update_counter(0, 1)
            self.sound_player.play_sound(ENEMY_DEATH)
        else:
            self.sound_player.play_sound(HIT, False)

    def handle_damage_to_ally(self, ally, bullet):
        """Handles damage to player's tank/seeker made by enemy's bullet. """
        bullet.hit_the_target = True
        ally.handle_injure(bullet.damage)
        add_effect(bullet.hit_effect, self.room.top_effects, bullet.x, bullet.y)

    def handle_bullet_explosion(self, bullet):
        """ Changes mobs' states according to their positions relative
        to the explosion, and adds some special effects.
        """
        x, y, radius = bullet.x, bullet.y, bullet.explosion_radius
        for enemy in chain(self.room.mobs, self.room.seekers):
            if enemy.collide_bullet(x, y, radius):
                self.handle_damage_to_enemy(enemy, bullet)

        add_effect(bullet.hit_effect, self.room.top_effects, bullet.x, bullet.y)
        add_effect('Flash', self.room.top_effects)
        if isinstance(bullet, ExplosivePierceBullet):
            for _ in range(3):
                add_effect('SmallHitLines', self.room.top_effects, bullet.x, bullet.y)
            add_effect('BigHitLines', self.room.top_effects, bullet.x, bullet.y)
        self.camera.start_shaking(200)

    def handle_enemy_collision(self, attacked_enemy, bullet):
        """Handles collision between enemy and player's bullet. """
        if isinstance(bullet, ExplodingBullet):
            self.handle_bullet_explosion(bullet)
            bullet.hit_the_target = True
        elif isinstance(bullet, ExplosivePierceBullet):
            if attacked_enemy not in bullet.attacked_mobs:
                bullet.attacked_mobs.append(attacked_enemy)
                self.handle_bullet_explosion(bullet)
        else:
            self.handle_damage_to_enemy(attacked_enemy, bullet)
            bullet.hit_the_target = True
            add_effect(bullet.hit_effect, self.room.top_effects, bullet.x, bullet.y)
            if isinstance(bullet, LeecherBullet):
                bubble = Bubble(bullet.x, bullet.y, gravitation_radius=2*ROOM_RADIUS)
                bubble.vel = 0
                self.room.bubbles.append(bubble)
            elif (isinstance(bullet, PlayerVirus) and
                  not isinstance(attacked_enemy, Seeker) and
                  not attacked_enemy.is_infected):
                attacked_enemy.become_infected()

    def handle_enemies_collisions(self):
        """Handles collisions between enemies player bullets. """
        self.sound_player.unlock()
        bullets = chain(self.player.bullets, self.player.mines,
                        self.player.seekers, self.player.orbital_seekers)
        for bullet in bullets:
            if isinstance(bullet, AirBullet):
                continue
            for enemy in chain(self.room.mobs, self.room.seekers):
                if enemy.collide_bullet(bullet.x, bullet.y, bullet.radius):
                    self.handle_enemy_collision(enemy, bullet)

    def handle_player_collisions(self):
        """Handles collisions between player's tank/seekers and all bullets of enemies. """
        self.sound_player.unlock()
        bullets = chain(self.room.bullets, self.room.mines, self.room.seekers)
        seekers = self.player.seekers
        allies = seekers if self.player.disassembled else seekers + [self.player]
        for b in bullets:
            for ally in allies:
                if ally.collide_bullet(b.x, b.y, b.radius):
                    self.handle_damage_to_ally(ally, b)
                    break

    def update_transportation(self, dt):
        """ Update all objects during transportation. """
        self.player.update(dt)
        self.camera.update(dt)
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
        self.room.draw_bullets(self.screen, *offset_old)
        self.room.draw_new_mobs(self.screen, *offset_old)

        self.bg_environment.draw_room_glares(self.screen, *offset_new)
        self.bg_environment.draw_room_glares(self.screen, *offset_old)

        self.room.draw_top_effects(self.screen, *offset_old)

        self.health_window.draw(self.screen)
        self.cooldown_window.draw(self.screen)

    def run_transportation(self, dx, dy):
        self.sound_player.play_sound(WATER_SPLASH)
        time = dt = 0
        while time < TRANSPORTATION_TIME and self.running:
            self.handle_events()
            self.update_transportation(dt)
            self.draw_transportation(time, dx, dy)
            pg.display.update()
            dt = self.clock.tick()
            self.fps_manager.update(dt)
            time += dt

    def get_destination_pos(self, direction):
        """Method returns player's destination point during transportation. """
        distance = DIST_BETWEEN_ROOMS - (ROOM_RADIUS - self.player.bg_radius - H(40))
        destination_pos = np.array([SCR_W2, SCR_H2]) + direction * distance
        return destination_pos

    def transport_player(self, direction):
        """Algorithm of transportation of the player. """
        self.transportation = True

        offset = -DIST_BETWEEN_ROOMS * direction
        player_pos = np.array([self.player.x, self.player.y], dtype=float)

        # Save mobs from previous room and generate mobs for the next room
        self.mob_generator.save_mobs(self.room.mobs)
        self.mob_generator.generate_mobs(direction, self.player)
        self.room.save_new_mobs(self.mob_generator.current_mobs)
        self.room.move_new_mobs(*-offset)

        # Set new boss disposition
        self.bg_environment.set_new_boss_disposition(self.mob_generator.cur_room,
                                                     self.room.new_mobs)
        # Update map in pause menu
        self.pause_menu.map_button.update_data(self.mob_generator.cur_room,
                                               self.bg_environment.new_boss_disposition)
        # Set new hint text for the player
        self.bg_environment.set_next_hint()

        destination_pos = self.get_destination_pos(direction)
        distance = hypot(*(player_pos - destination_pos))
        velocity = distance / TRANSPORTATION_TIME
        angle = calculate_angle(*player_pos, *destination_pos)
        self.player.set_transportation_vel(angle, velocity)

        self.bg_environment.set_player_trace(*player_pos, distance, angle)
        self.bg_environment.set_destination_circle(destination_pos)

        self.run_transportation(*offset)

        self.player.move(*offset)
        self.player.body.update_pos(0)
        self.camera.update(0)
        self.room.update_screen_rect()

        self.room.move_new_mobs(*offset)
        self.room.set_params_after_transportation()
        self.player.set_params_after_transportation()
        self.bg_environment.set_params_after_transportation()

        self.update_save_data()

        self.transportation = False
        self.clock.tick()

    def get_direction(self, offset):
        """ This method determines the direction of transportation
        of player so that he is transported to the nearest room.
        """
        if offset == 0:
            return np.array([-1, 0])

        if (self.camera.offset[0] / offset) ** 2 <= 0.5:
            return np.array([0, -1] if self.camera.offset[1] < 0 else [0, 1])

        return np.array([1, 0] if self.camera.offset[0] > 0 else [-1, 0])

    def check_transportation(self):
        """Checks if player is defeated or outside the room.
        If yes, determines the direction of transportation
        and transports player to the next room.
        """
        player_offset = hypot(*self.camera.offset)
        if self.player.defeated or player_offset > ROOM_RADIUS:
            direction = self.get_direction(player_offset)
            self.transport_player(direction)

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
        self.handle_player_collisions()
        self.check_player_state()
        self.player.update(dt)
        self.camera.update(dt)
        self.room.update(dt)

        if self.room.boss_defeated(self.bg_environment.boss_disposition):
            self.victory_menu.run()
        if not self.running:
            return

        self.health_window.update(dt)
        self.cooldown_window.update(dt)
        self.check_transportation()

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
        if isinstance(self.player.superpower, Ghost):
            self.player.superpower.update_body()
        self.player.body.update_pos(dt)

        for obj in chain(self.player.mines, self.player.bullets, self.room.mobs,
                         self.room.bubbles, self.room.mines, self.room.bullets):
            obj.update_body(dt)

        for seeker in self.player.orbital_seekers:
            if seeker.is_orbiting:
                seeker.update_polar_coords(self.player.x, self.player.y, dt)

        self.room.update_effects(dt)

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

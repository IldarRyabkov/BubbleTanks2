from math import cos, sin, pi, hypot
from random import uniform, choice

from data.guns import GUNS
from data.constants import *

from components.utils import *
from components.bullets import *
from components.circle import make_circles_list


class EnemyWeapons:
    def __init__(self, owner, game, data):
        self.game = game
        self.state = 0
        self.all_guns = [self.make_gun(owner, gun_data) for gun_data in data["guns"]]
        self.guns = dict()
        self.init_guns(data)
        self.machine_gun_time = 0
        self.machine_gun_on = False

    def machine_gun_delay(self, dt):
        self.machine_gun_time += dt
        if self.machine_gun_time < 3000:
            self.machine_gun_on = False
        elif self.machine_gun_time < 5000:
            self.machine_gun_on = True
        else:
            self.machine_gun_on = False
            self.machine_gun_time = 0

    def update_state(self, state):
        self.state = state
        for gun in self.current_guns:
            gun.update_shape(0)

    @property
    def current_guns(self):
        return self.guns[self.state]

    def init_guns(self, data):
        self.guns = dict()
        for (left, right), indexes in data["guns states"].items():
            for state in range(left, right + 1):
                self.guns[state] = [self.all_guns[i] for i in indexes]

    def make_gun(self, owner, data):
        gun_params = GUNS[data["name"]]
        distance = HF(data["distance"])
        angle = data["angle"]
        emitter_offset = HF(gun_params["emitter offset"])
        circles_data = gun_params["circles"]
        rotation_type = data["rotation type"]
        rotation_angle = data["rotation angle"]
        shooting_type = data["shooting type"]
        cooldown_min = data["cooldown min"]
        cooldown_max = data["cooldown max"]
        delay = data["delay"]
        bullet_type = gun_params["bullet type"]
        bullet_name = data["bullet name"]
        bullet_vel = HF(data["bullet velocity"])
        bullet_dmg = data["bullet damage"]
        scale = data["scale"]
        return Gun(owner, self.game, self.game.rect, distance, angle, emitter_offset,
                   circles_data, rotation_type, rotation_angle, shooting_type, cooldown_min,
                   cooldown_max, delay, bullet_type, bullet_name, bullet_vel, bullet_dmg, scale)

    def become_infected(self):
        for gun in self.all_guns:
            gun.become_infected()

    def update_pos(self):
        for gun in self.current_guns:
            gun.update_pos()

    def update_shape(self, dt):
        for gun in self.current_guns:
            gun.update_shape(dt)

    def update_shooting(self, dt):
        self.machine_gun_delay(dt)
        for gun in self.current_guns:
            gun.update_shooting(dt)

    def draw(self, screen, dx=0, dy=0):
        for gun in self.current_guns:
            gun.draw(screen, dx, dy)


class Gun:
    def __init__(self, owner, game, screen_rect, distance, angle,
                 emitter_offset, circles_data, rotation_type, rotation_angle,
                 shooting_type, cooldown_min, cooldown_max, delay,
                 bullet_type, bullet_name, bullet_vel, bullet_dmg, scale):

        self.owner = owner
        self.game = game
        self.player = game.player
        self.screen_rect = screen_rect
        self.spawned_enemy = None
        self.spawned_seeker = None
        self.x = 0
        self.y = 0
        self.distance = distance
        self.angle = angle
        self.angle_to_target = 0
        self.emitter_offset = emitter_offset * scale
        self.cooldown_min = cooldown_min
        self.cooldown_max = cooldown_max
        self.cooldown = (cooldown_max + cooldown_min) / 2
        self.time = self.cooldown - delay

        self.circles = make_circles_list(self.screen_rect, circles_data, scale)
        self.rotation_type = rotation_type
        self.rotation_angle = rotation_angle
        self.shoot = self.get_shooting_func(shooting_type)

        self.bullet = get_bullet_type(bullet_type)
        self.bullet_name = bullet_name
        self.bullet_vel = bullet_vel
        self.bullet_dmg = bullet_dmg

    def become_infected(self):
        for circle in self.circles:
            circle.become_infected()

    def update_pos(self):
        body_angle = self.owner.body.angle
        x = self.owner.x + self.distance * cos(self.angle + body_angle)
        y = self.owner.y - self.distance * sin(self.angle + body_angle)
        self.x, self.y = x, y
        if self.rotation_type == FIXED_GUN:
            self.angle_to_target = body_angle + self.rotation_angle
        elif self.rotation_type == ROTATING_GUN:
            self.angle_to_target = calculate_angle(x, y, self.player.x, self.player.y)

    def update_shape(self, dt):
        x, y, angle_to_target = self.x, self.y, self.angle_to_target
        for circle in self.circles:
            circle.update_pos(x, y, dt, angle_to_target)

    def update_shooting(self, dt):
        self.time += dt
        if self.time >= self.cooldown:
            self.shoot()

    def get_shooting_func(self, shooting_type):
        if shooting_type == "single":
            return self.shoot_single
        if shooting_type == "3 parallel":
            return self.shoot_3_parallel
        if shooting_type == "5 parallel":
            return self.shoot_5_parallel
        if shooting_type == "3 spread":
            return self.shoot_3_spread
        if shooting_type == "5 spread":
            return self.shoot_5_spread
        if shooting_type == "10 spread":
            return self.shoot_10_spread
        if shooting_type == "spawn enemy":
            self.spawned_enemy = choice(["Gull", "Bug", "Scarab"])
            return self.spawn_enemy
        if shooting_type == "spawn bubble bomber":
            self.spawned_enemy = "BubbleBomber"
            return self.spawn_enemy
        if shooting_type == "spawn seeker":
            return self.spawn_seeker
        if shooting_type == "spawn leecher":
            return self.spawn_leecher
        if shooting_type == "spawn sapper":
            return self.spawn_sapper
        if shooting_type == "spawn orbital seeker":
            return self.spawn_orbital_seeker
        if shooting_type == "machine gun 360":
            return self.shoot_mg_360
        if shooting_type == "machine gun 360 fast":
            return self.shoot_mg_360_fast
        if shooting_type == "machine gun":
            return self.shoot_mg
        if shooting_type == "mines":
            return self.shoot_mine
        if shooting_type == "sting":
            return self.sting
        return lambda: None

    def make_bullet(self, x, y, angle):
        return self.bullet(self.bullet_name, self.screen_rect, x, y,
                           self.bullet_dmg, self.bullet_vel, angle)

    def shoot_single(self):
        x = self.x + self.emitter_offset * cos(self.angle_to_target)
        y = self.y - self.emitter_offset * sin(self.angle_to_target)
        bullet = self.make_bullet(x, y, self.angle_to_target)
        self.game.room.bullets.append(bullet)
        self.time = 0
        self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def shoot_3_parallel(self):
        angle = self.angle_to_target
        sina, cosa = sin(angle), cos(angle)
        x = self.x + self.emitter_offset * cosa
        y = self.y - self.emitter_offset * sina
        dx = HF(19) * sina
        dy = HF(19) * cosa
        for k in (-1, 0, 1):
            bullet = self.make_bullet(x + k * dx, y + k * dy, angle)
            self.game.room.bullets.append(bullet)
        self.time = 0
        self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def shoot_5_parallel(self):
        angle = self.angle_to_target
        sina, cosa = sin(angle), cos(angle)
        x = self.x + self.emitter_offset * cosa
        y = self.y - self.emitter_offset * sina
        dx1, dy1 = HF(23) * sina, HF(23) * cosa
        dx2, dy2 = HF(42) * sina, HF(42) * cosa
        dx3, dy3 = HF(15) * cosa, HF(15) * sina
        for dx, dy in (0, 0), (dx1, dy1), (-dx1, -dy1), (dx2-dx3, dy2+dy3), (-dx2-dx3, -dy2+dy3):
            bullet = self.make_bullet(x + dx, y + dy, angle)
            self.game.room.bullets.append(bullet)
        self.time = 0
        self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def shoot_mine(self):
        x = self.x + self.emitter_offset * cos(self.angle_to_target)
        y = self.y - self.emitter_offset * sin(self.angle_to_target)
        mine = self.make_bullet(x, y, self.angle_to_target)
        self.game.room.mines.append(mine)
        self.time = 0
        self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def shoot_mg_360(self):
        if not self.owner.weapons.machine_gun_on:
            return
        self.angle_to_target -= pi/36
        self.shoot_single()

    def shoot_mg_360_fast(self):
        if not self.owner.weapons.machine_gun_on:
            return
        self.angle_to_target -= 0.075 * pi
        self.shoot_single()

    def shoot_mg(self):
        if not self.owner.weapons.machine_gun_on:
            return
        self.shoot_single()

    def sting(self):
        distance = hypot(self.owner.x - self.player.x, self.owner.y - self.player.y)
        if distance <= self.owner.rect.width/2 + self.player.radius:
            self.player.receive_damage(self.bullet_dmg, play_sound=True)
            self.time = 0
            self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def shoot_3_spread(self):
        angle = self.angle_to_target
        dx = HF(28.843) * sin(angle)
        dy = HF(28.843) * cos(angle)
        x = self.x + self.emitter_offset * cos(angle)
        y = self.y - self.emitter_offset * sin(angle)
        for k in (-1, 0, 1):
            bullet = self.make_bullet(x - k * dx, y - k * dy, angle + k * pi/6)
            self.game.room.bullets.append(bullet)
        self.time = 0
        self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def shoot_5_spread(self):
        for k in (-2, -1, 0, 1, 2):
            angle = self.angle_to_target + k * pi/6
            x = self.x + self.emitter_offset * cos(angle)
            y = self.y - self.emitter_offset * sin(angle)
            bullet = self.make_bullet(x, y, angle)
            self.game.room.bullets.append(bullet)
        self.time = 0
        self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def shoot_10_spread(self):
        x = self.x + self.emitter_offset * cos(self.angle_to_target)
        y = self.y - self.emitter_offset * sin(self.angle_to_target)
        for k in range(10):
            angle = self.angle_to_target + k * 0.2 * pi
            bullet = self.make_bullet(x, y, angle)
            self.game.room.bullets.append(bullet)
        self.time = 0
        self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def spawn_enemy(self):
        self.game.room.spawn_enemy(self.spawned_enemy, self.x, self.y)
        self.time = 0
        self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def spawn_seeker(self):
        x = self.x + self.emitter_offset * cos(self.angle_to_target)
        y = self.y - self.emitter_offset * sin(self.angle_to_target)
        seeker = self.bullet(self.game, self.bullet_name, self.screen_rect,
                             x, y, self.angle_to_target, 0.018,
                             self.bullet_dmg, self.bullet_vel)
        seeker.update(0)
        self.game.room.seekers.append(seeker)
        self.time = 0
        self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def spawn_leecher(self):
        if self.spawned_seeker is None or self.spawned_seeker.killed:
            x = self.x + self.emitter_offset * cos(self.angle_to_target)
            y = self.y - self.emitter_offset * sin(self.angle_to_target)
            leecher = self.bullet(self.player, self.bullet_name, self.screen_rect, x, y,
                                  self.angle_to_target, 0.018, self.bullet_dmg, self.bullet_vel)
            self.spawned_seeker = leecher
            self.game.room.seekers.append(leecher)
            self.time = 0
            self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def spawn_sapper(self):
        if self.spawned_seeker is None or self.spawned_seeker.killed:
            x = self.x + self.emitter_offset * cos(self.angle_to_target)
            y = self.y - self.emitter_offset * sin(self.angle_to_target)
            sapper = self.bullet(self.owner, self.game, self.bullet_name, self.screen_rect,
                                 x, y, self.angle_to_target, 0.02,
                                 self.bullet_dmg, self.bullet_vel)
            self.spawned_seeker = sapper
            self.game.room.seekers.append(sapper)
            self.time = 0
            self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def spawn_orbital_seeker(self):
        if self.spawned_seeker is None or self.spawned_seeker.killed:
            x = self.x + self.emitter_offset * cos(self.angle_to_target)
            y = self.y - self.emitter_offset * sin(self.angle_to_target)
            seeker = EnemyOrbitalSeeker(self.owner, self.bullet_name, self.screen_rect,
                                        x, y, self.angle_to_target, 0.018, self.bullet_dmg)
            self.spawned_seeker = seeker
            self.game.room.seekers.append(seeker)
            self.time = 0
            self.cooldown = uniform(self.cooldown_min, self.cooldown_max)

    def draw(self, screen, dx=0, dy=0):
        for circle in self.circles:
            if circle.is_on_screen:
                circle.update_glares(self.angle_to_target)
                circle.draw(screen, dx, dy)


__all__ = ["EnemyWeapons"]

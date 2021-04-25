from math import sin, cos

from data.config import SCR_H
from objects.body import Body
from utils import circle_collidepoint, calculate_angle
from objects.mob_guns import get_gun as get_mob_gun
from objects.player_guns import get_gun as get_player_gun


class Mob:
    def __init__(self,
                 name,
                 x,
                 y,
                 health,
                 health_states,
                 bubbles,
                 radius,
                 body,
                 gun_type='PeacefulGun',
                 time=0.0,
                 w=0.0,
                 body_rect=None):

        self.gun = get_player_gun(gun_type) if name == 'Player' else get_mob_gun(gun_type)
        self.name = name
        self.xo = x
        self.yo = y
        self.x = x
        self.y = y
        self.time = time
        self.w = w
        self.speed = [0, 0]
        self.max_health = health
        self.health = health
        self.health_states = health_states
        self.bubbles = bubbles
        self.radius = radius
        self.body = Body(body)
        self.body_rect = body_rect
        self.is_paralysed = False
        self.paralysed_time = 0
        self.gamma = 0
        self.is_frozen = False
        self.frost_time = 0

    def trajectory(self, t):
        return self.xo, self.yo

    def rose_curve_1(self, t):
        dist = 170 * SCR_H/600
        x = self.xo + dist * (cos(9*t/4) + 7/3) * cos(t)
        y = self.yo + dist * (cos(9*t/4) + 7/3) * sin(t)
        return x, y

    def rose_curve_2(self, t):
        dist = 500 * SCR_H/600
        x = self.xo + dist * sin(3/4 * t) * cos(t)
        y = self.yo - dist * sin(3/4 * t) * sin(t)
        return x, y

    def rose_curve_3(self, t):
        dist = 375 * SCR_H/600
        x = self.xo + dist * cos(t) + 30 * cos(5 * t)
        y = self.yo + dist * sin(t) + 30 * sin(5 * t)
        return x, y

    def rose_curve_4(self, t):
        dist = 250 * SCR_H / 600
        x = self.xo + dist * sin(2/3 * t) * cos(t)
        y = self.yo - dist * sin(2/3 * t) * sin(t)
        return x, y

    def epicycloid(self, t):
        dist = 250 * SCR_H / 600
        x = self.xo + dist * cos(t) + 20 * cos(5 * t)
        y = self.yo + dist * sin(t) + 20 * sin(5 * t)
        return x, y

    def collide_bullet(self, x, y):
        return circle_collidepoint(self.x, self.y, self.radius, x, y)

    def update_body_look(self):
        for circle in self.body.circles:
            circle.visible = True
        k = 0
        for i in range(len(self.health_states)):
            if self.health <= self.health_states[i][0]:
                k = i
        for i in range(1, len(self.health_states[k])):
            for j in range(self.health_states[k][i][0], self.health_states[k][i][1]):
                self.body.circles[j].visible = False

        if self.is_frozen:
            self.make_body_frozen()
        else:
            self.make_body_unfrozen()

    def handle_injure(self, damage):
        if damage:
            self.health += damage
            self.update_body_look()
        else:
            self.make_frozen()

    def count_gamma(self):
        dt = 0.01 if self.w > 0 else -0.01
        x, y = self.trajectory(self.time + dt)
        return calculate_angle(self.x, self.y, x, y)

    def move(self, dx, dy):
        self.body.move(dx, dy)
        self.body_rect = self.body_rect.move(dx, dy)

    def update_pos(self, dt, generated_mobs=list()):
        self.time += dt/1000 * self.w
        self.x, self.y = self.trajectory(self.time)
        self.body_rect.center = (self.x, self.y)

    def update_body(self, dt, target=(0, 0)):
        self.body.update(self.x, self.y, dt, target, self.gamma)

    def make_paralysed(self):
        self.is_paralysed = True
        self.paralysed_time = 0

    def make_body_frozen(self):
        for i in range(-10, 0):
            self.body.circles[i].visible = True

    def make_body_unfrozen(self):
        for i in range(-10, 0):
            self.body.circles[i].visible = False

    def make_unfrozen(self):
        self.is_frozen = False
        self.frost_time = 0
        self.make_body_unfrozen()

    def make_frozen(self):
        self.is_frozen = True
        self.frost_time = 0
        self.make_body_frozen()

    def update_paralysed_state(self, dt):
        if self.is_paralysed:
            self.paralysed_time += dt
            if self.paralysed_time >= 2000:
                self.paralysed_time = 0
                self.is_paralysed = False

    def update_frozen_state(self, dt):
        if self.is_frozen:
            self.frost_time += dt
            if self.frost_time >= 3000:
                self.make_unfrozen()

    def update(self, target, bullets, homing_bullets,
               generated_mobs, screen_rect, dt):
        if not self.is_paralysed:
            if not self.is_frozen:
                self.update_pos(dt, generated_mobs)

            self.gun.update_time(dt)
            self.gamma = self.count_gamma()
            new_bullets = homing_bullets if self.gun.shooting_homing_bullets else bullets
            self.gun.append_bullets(self.x, self.y, target, new_bullets, self.gamma)

        if self.body_rect.colliderect(screen_rect):
            self.update_body(dt, target)

        self.update_paralysed_state(dt)
        self.update_frozen_state(dt)
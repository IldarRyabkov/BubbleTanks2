from random import choice, uniform
from math import pi, cos, sin

from data.mobs import *

from .mob import Mob
from .bubble import Bubble
from .utils import *


#_________________________________________________________________________________________________

class Infusoria(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *INFUSORIA_PARAMS.values())

    def handle_injure(self, damage):
        super().handle_injure(damage)
        if damage and self.health == 1:
            bubble = Bubble(self.x, self.y)
            bubble.gravity_radius = 1.3 * self.player.bg_radius
            bubble.vel = 0
            self.game.room.bubbles.append(bubble)

#_________________________________________________________________________________________________


class Ameba(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *AMEBA_PARAMS.values())

#_________________________________________________________________________________________________

class Cell(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *CELL_PARAMS.values())

#_________________________________________________________________________________________________

class Baby(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BABY_PARAMS.values())

#_________________________________________________________________________________________________

class Turtle(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *TURTLE_PARAMS.values(), random_shift=320)

#_________________________________________________________________________________________________

class TurtleDamaging(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *TURTLE_DAMAGING_PARAMS.values(), random_shift=320)

#_________________________________________________________________________________________________

class Bug(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BUG_PARAMS.values())

#_________________________________________________________________________________________________

class Scarab(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *SCARAB_PARAMS.values())

#_________________________________________________________________________________________________

class Gull(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *GULL_PARAMS.values())

#_________________________________________________________________________________________________

class Ant(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *ANT_PARAMS.values(), random_shift=400)

#_________________________________________________________________________________________________

class Spreader(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *SPREADER_PARAMS.values())

#_________________________________________________________________________________________________

class BigEgg(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BIGEGG_PARAMS.values())

#_________________________________________________________________________________________________

class BossHead(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BOSS_HEAD_PARAMS.values())
        self.y_offset = H(213)
        self.body_rect.w = H(620)
        self.body.angle = -0.5 * pi

    def update_pos(self, dt):
        self.body_rect.center = self.x, self.y + self.y_offset

    def update_body_angle(self, dt):
        angle = calculate_angle(self.x, self.y, self.player.x, self.player.y)
        if angle > 0.5 * pi:
            angle -= 2 * pi
        min_angle = -0.7 * pi
        max_angle = -0.3 * pi
        if min_angle <= angle <= max_angle:
            min_angle = max_angle = angle

        if self.body.angle < angle:
            self.body.angle = min(self.body.angle + 0.0003*pi * dt, max_angle)
        else:
            self.body.angle = max(self.body.angle - 0.0003*pi * dt, min_angle)

    def collide_bullet(self, bul_x, bul_y, bul_r):
        return circle_collidepoint(self.x, self.y + self.y_offset, self.radius + bul_r, bul_x, bul_y)

    def update_body(self, dt):
        turret_target = self.gun.turret_target
        player_pos = self.player.x, self.player.y
        body_angle = self.body.angle
        if self.body_rect.colliderect(self.screen_rect):
            for i, circle in enumerate(self.body.circles):
                if circle.is_visible:
                    target = turret_target if 16 <= i < 24 else player_pos
                    circle.update(self.x, self.y, dt, *target, 0, body_angle)
        self.body.update_frozen_state(dt)

#_________________________________________________________________________________________________

class BossHandLeft(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BOSS_HAND_LEFT_PARAMS.values())

#_________________________________________________________________________________________________

class BossHandRight(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BOSS_HAND_RIGHT_PARAMS.values())

#_________________________________________________________________________________________________

class BossLeg(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BOSS_LEG_PARAMS.values())

#_________________________________________________________________________________________________

class Terrorist(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *TERRORIST_PARAMS.values())


#_________________________________________________________________________________________________

class BenLaden(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BENLADEN_PARAMS.values())

#_________________________________________________________________________________________________

class BomberShooter(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BOMBERSHOOTER_PARAMS.values())

#_________________________________________________________________________________________________

class Mother(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *MOTHER_PARAMS.values())
        self.generation_time = 6000
        self.generation_cooldown = 7000
        self.child_params = choice([GULL_PARAMS, BUG_PARAMS, SCARAB_PARAMS])

    def update(self, dt):
        super().update(dt)
        if not self.is_paralyzed:
            self.generation_time += dt
            if self.generation_time >= self.generation_cooldown:
                self.generation_time = 0
                self.generate_mob()

    def generate_mob(self):
        mob = Mob(self.game, self.screen_rect, *self.child_params.values())
        mob.xo = self.xo
        mob.yo = self.yo
        mob.x = self.x
        mob.y = self.y
        mob.polar_angle = self.polar_angle
        mob.body.update(mob.x, mob.y, 0)
        self.game.room.mobs.append(mob)

#_________________________________________________________________________________________________

class Cockroach(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *COCKROACH_PARAMS.values(), random_shift=400)


#_________________________________________________________________________________________________

class Beetle(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *BEETLE_PARAMS.values())

#_________________________________________________________________________________________________

class Spider(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *SPIDER_PARAMS.values())

#_________________________________________________________________________________________________

class Turret(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *TURRET_PARAMS.values())
        random_offset = uniform(0, 800)
        random_angle = uniform(0, 2*pi)
        dx = random_offset * cos(random_angle)
        dy = random_offset * sin(random_angle)
        self.move(dx, dy)
        self.gun.set_turret_target()
        self.body.update(self.x, self.y, 0, *self.gun.turret_target)

    def update_body(self, dt):
        if self.body_rect.colliderect(self.screen_rect):
            self.body.update(self.x, self.y, dt, *self.gun.turret_target)
        self.body.update_frozen_state(dt)

#_________________________________________________________________________________________________

class MachineGunner(Mob):
    def __init__(self, game, screen_rect):
        super().__init__(game, screen_rect, *MACHINEGUNNER_PARAMS.values())

#_________________________________________________________________________________________________


mobs = {
    "BossHead": BossHead,
    "BossHandLeft": BossHandLeft,
    "BossHandRight": BossHandRight,
    "BossLeg": BossLeg,
    "Gull": Gull,
    "Bug": Bug,
    "Scarab": Scarab,
    "Ant": Ant,
    "Cockroach": Cockroach,
    "Mother": Mother,
    "Beetle": Beetle,
    "Spider": Spider,
    "Spreader": Spreader,
    "Infusoria": Infusoria,
    "Baby": Baby,
    "Cell": Cell,
    "Ameba": Ameba,
    "Turtle": Turtle,
    "TurtleDamaging": TurtleDamaging,
    "MachineGunner": MachineGunner,
    "Turret": Turret,
    "Terrorist": Terrorist,
    "BenLaden": BenLaden,
    "BomberShooter": BomberShooter,
    "BigEgg": BigEgg,
}


def get_mob(name, game, screen_rect):
    return mobs[name](game, screen_rect)


__all__ = ["get_mob"]
from numpy import array
from random import uniform, choice
from math import cos, sin, pi

from objects.mob import Mob
from utils import circle_collidepoint, HF
from entities.mob_guns import get_gun
from data.mobs import *


class BossHead(Mob):
    def __init__(self):
        super().__init__(*BOSS_HEAD_PARAMS.values())
        self.rect_dy = HF(213)


    def update_pos(self, dt):
        super().update_pos(dt)
        self.body_rect.y += self.rect_dy

    def collide_bullet(self, x, y, r):
        return circle_collidepoint(self.pos[0], self.pos[1] + self.rect_dy, self.radius + r, x, y)

    def update_body(self, screen_rect, dt, player_pos=(0, 0)):
        if self.body_rect.colliderect(screen_rect):
            for i, circle in enumerate(self.body.circles):
                if circle.visible:
                    target = self.gun.target if 16 <= i < 24 else player_pos
                    circle.update(*self.pos, dt, target, 0, -0.5 * pi)


class MobTerrorist(Mob):
    def __init__(self):
        super().__init__(*TERRORIST_PARAMS.values())

    def update_body_look(self):
        super().update_body_look()
        if self.health <= 4:
            self.gun = get_gun('GunPeaceful')


class Mother(Mob):
    def __init__(self):
        super().__init__(*MOTHER_PARAMS.values())
        self.generation_time = 5000
        self.generation_cooldown = 7000
        self.child_params = choice([GULL_PARAMS, BUG_PARAMS, SCARAB_PARAMS])

    def generate_mob(self, dt):
        self.generation_time += dt
        if self.generation_time >= self.generation_cooldown:
            self.generation_time -= self.generation_cooldown
            mob = Mob(*self.child_params.values())
            mob.pos_0 = self.pos_0.copy()
            mob.pos = self.pos.copy()
            mob.polar_angle = self.polar_angle
            mob.body.update(*mob.pos, 0)
            return [mob]
        return []


class Cockroach(Mob):
    def __init__(self):
        super().__init__(*COCKROACH_PARAMS.values(), random_shift=400)

    def update_body_look(self):
        super().update_body_look()
        if self.health <= 3:
            self.gun = get_gun('GunPeaceful')


class Beetle(Mob):
    def __init__(self):
        super().__init__(*BEETLE_PARAMS.values())

    def update_body_look(self):
        super().update_body_look()
        if self.health <= 6 and self.gun.cooldown_time == 450:
            self.gun = get_gun('GunBeetleReserve')


class Spider(Mob):
    def __init__(self):
        super().__init__(*SPIDER_PARAMS.values())

    def update_body_look(self):
        super().update_body_look()
        if self.health <= 70:
            self.gun.small_gun_is_alive = False


class Turret(Mob):
    def __init__(self):
        super().__init__(*TURRET_PARAMS.values())
        r, fi = uniform(0, HF(800)), uniform(0, 2 * pi)
        d_pos = array([r * cos(fi), -r * sin(fi)])
        self.pos += d_pos
        self.pos_0 += d_pos

    def update_body(self, screen_rect, dt, target=(0, 0)):
        if self.body_rect.colliderect(screen_rect):
            self.body.update(*self.pos, dt, self.gun.target, 0)


def get_mob(name):
    if name == "BossHead":      return BossHead()
    if name == "Terrorist":     return MobTerrorist()
    if name == "Cockroach":     return Cockroach()
    if name == "Mother":        return Mother()
    if name == "Beetle":        return Beetle()
    if name == "Spider":        return Spider()
    if name == "Turret":        return Turret()
    if name == "BossHandLeft":  return Mob(*BOSS_HAND_LEFT_PARAMS.values())
    if name == "BossHandRight": return Mob(*BOSS_HAND_RIGHT_PARAMS.values())
    if name == "BossLeg":       return Mob(*BOSS_LEG_PARAMS.values())
    if name == "Ameba":         return Mob(*AMEBA_PARAMS.values())
    if name == "Cell":          return Mob(*CELL_PARAMS.values())
    if name == "Baby":          return Mob(*BABY_PARAMS.values())
    if name == "Infusoria":     return Mob(*INFUSORIA_PARAMS.values())
    if name == "BenLaden":      return Mob(*BENLADEN_PARAMS.values())
    if name == "Bug":           return Mob(*BUG_PARAMS.values())
    if name == "Scarab":        return Mob(*SCARAB_PARAMS.values())
    if name == "Gull":          return Mob(*GULL_PARAMS.values())
    if name == "BomberShooter": return Mob(*BOMBERSHOOTER_PARAMS.values())
    if name == "Spreader":      return Mob(*SPREADER_PARAMS.values())
    if name == "BigEgg":        return Mob(*BIGEGG_PARAMS.values())
    if name == "MachineGunner": return Mob(*MACHINEGUNNER_PARAMS.values())
    if name == "Turtle":        return Mob(*TURTLE_PARAMS.values(), random_shift=320)
    if name == "Turtle_dmg":    return Mob(*TURTLE_DAMAGING_PARAMS.values(), random_shift=320)
    if name == "Ant":           return Mob(*ANT_PARAMS.values(), random_shift=400)

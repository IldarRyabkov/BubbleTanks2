import pygame as pg
from math import sin, cos
from random import uniform, choice

from objects.mob import Mob
from data.config import SCR_W2, SCR_H2, SCR_W
from utils import circle_collidepoint
from objects.mob_guns import get_gun
from data.mobs import *


class MobBossHead(Mob):
    def __init__(self):
        Mob.__init__(self,
                     name='BossHead',
                     x=SCR_W2,
                     y=SCR_H2 - 1000,
                     health=150,
                     health_states=BOSS_HEAD_HEALTH_STATES,
                     bubbles={"small": 0, "medium": 5, "big": 3},
                     radius=131,
                     body=BOSS_HEAD_BODY,
                     gun_type='GunBossHead',
                     time=0,
                     w=0,
                     body_rect=pg.Rect(0, 0, 464, 448))

    def update_pos(self, dt, generated_mobs=list()):
        super().update_pos(dt, generated_mobs)
        self.body_rect.y += 240

    def collide_bullet(self, x, y):
        return circle_collidepoint(self.x, self.y + 160, self.radius, x, y)

    def update_body(self, dt, player_pos=(0, 0)):
        for i, circle in enumerate(self.body.circles):
            if circle.visible:
                target = self.gun.target if 16 <= i < 24 else player_pos
                circle.update(self.x, self.y, dt, target, 0, -0.5 * pi)


class MobBossHand(Mob):
    def __init__(self, side):
        name = 'BossHandLeft' if side == 'left' else 'BossHandRight'
        x = -18 if side == 'left' else SCR_W + 18

        Mob.__init__(self,
                     name=name,
                     x=x,
                     y=-158,
                     health=150,
                     health_states=BOSS_HAND_HEALTH_STATES,
                     bubbles={"small": 0, "medium": 5, "big": 3},
                     radius=120,
                     body=BOSS_HAND_BODY,
                     gun_type='GunBossHand',
                     time=0,
                     w=0,
                     body_rect=pg.Rect(0, 0, 416, 416))

        if side == 'left':
            for circle in self.body.circles:
                circle.angle *= -1


class MobBossLeg(Mob):
    def __init__(self):
        Mob.__init__(self,
                     name='BossLeg',
                     x=SCR_W2,
                     y=SCR_H2 + 832,
                     health=150,
                     health_states=BOSS_LEG_HEALTH_STATES,
                     bubbles={"small": 0, "medium": 5, "big": 3},
                     radius=120,
                     body=BOSS_LEG_BODY,
                     gun_type='GunBossLeg',
                     time=0,
                     w=0,
                     body_rect=pg.Rect(0, 0, 400, 560))

        for circle in self.body.circles:
            circle.angle += pi


class MobBossSkeleton(Mob):
    def __init__(self):
        Mob.__init__(self,
                     name='BossSkeleton',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=1,
                     health_states=tuple(),
                     bubbles={"small": 0, "medium": 0, "big": 0},
                     radius=0,
                     body=BOSS_SKELETON_BODY,
                     gun_type='GunPeaceful',
                     time=0,
                     w=0,
                     body_rect=pg.Rect(0, 0, 2000, 2000))

        for circle in self.body.circles:
            circle.angle += pi

    def update(self, target, bullets, homing_bullets,
               generated_mobs, screen_rect, dt):
        pass


class MobAmeba(Mob):
    def __init__(self):
        Mob.__init__(self,
                     name='Ameba',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=4,
                     health_states=AMEBA_HEALTH_STATES,
                     bubbles={"small": 2, "medium": 0, "big": 0},
                     radius=40,
                     body=AMEBA_BODY,
                     gun_type='GunPeaceful',
                     time=uniform(0, 1000),
                     w=choice([-0.2, 0.2]),
                     body_rect=pg.Rect(0, 0, 90, 90))

        self.trajectory = self.rose_curve_1


class MobCell(Mob):
    def __init__(self):
        Mob.__init__(self,
                     name='Cell',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=4,
                     health_states=CELL_HEALTH_STATES,
                     bubbles={"small": 3, "medium": 0, "big": 0},
                     radius=24,
                     body=CELL_BODY,
                     gun_type='GunPeaceful',
                     time=uniform(0, 1000),
                     w=choice([-0.65, 0.65]),
                     body_rect=pg.Rect(0, 0, 80, 80))

        self.trajectory = self.rose_curve_1


class MobInfusoria(Mob):
    def __init__(self):
        Mob.__init__(self,
                     name='Infusoria',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=2,
                     health_states=INFUSORIA_HEALTH_STATES,
                     bubbles={"small": 7, "medium": 0, "big": 0},
                     radius=40,
                     body=INFUSORIA_BODY,
                     gun_type='GunPeaceful',
                     time=uniform(0, 1000),
                     w=choice([-0.45, 0.45]),
                     body_rect=pg.Rect(0, 0, 112, 112))

        self.trajectory = self.rose_curve_1


class MobBaby(Mob):
    def __init__(self):
        Mob.__init__(self,
                     name='Baby',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=1,
                     health_states=BABY_HEALTH_STATES,
                     bubbles={"small": 1, "medium": 0, "big": 0},
                     radius=24,
                     body=BABY_BODY,
                     gun_type='GunPeaceful',
                     time=uniform(0, 1000),
                     w=choice([-0.3, 0.3]),
                     body_rect=pg.Rect(0, 0, 64, 64))

        self.trajectory = self.rose_curve_1


class MobTurtle(Mob):
    def __init__(self, damaging):
        if damaging:
            name = 'Turtle_dmg' if damaging else 'Turtle'
            bubbles = {"small": 3, "medium": 1, "big": 0}
            gun_type = 'GunTurtleDMG'
        else:
            name = 'Turtle'
            bubbles = {"small": 6, "medium": 0, "big": 0}
            gun_type = 'GunTurtle'
        Mob.__init__(self,
                     name=name,
                     x=SCR_W2 + choice([-320, 320]),
                     y=SCR_H2 + choice([-320, 320]),
                     health=21,
                     health_states=TURTLE_HEALTH_STATES,
                     bubbles=bubbles,
                     radius=86,
                     body=TURTLE_BODY,
                     gun_type=gun_type,
                     time=uniform(0, 1000),
                     w=choice([-0.5, 0.5]),
                     body_rect=pg.Rect(0, 0, 240, 240))
        self.trajectory = self.epicycloid
        if damaging:
            for i in range(-18, -14):
                self.body.circles.pop(i)


class MobTerrorist(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='Terrorist',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=18,
                     health_states=TERRORIST_HEALTH_STATES,
                     bubbles={"small": 9, "medium": 0, "big": 0},
                     radius=112,
                     body=TERRORIST_BODY,
                     gun_type='GunTerrorist',
                     time=uniform(0, 1000),
                     w=choice([-0.15, 0.15]),
                     body_rect=pg.Rect(0, 0, 336, 336))

        self.trajectory = self.rose_curve_2

    def update_body_look(self):
        super().update_body_look()
        if self.health <= 4:
            self.gun = get_gun('GunPeaceful')


class MobBenLaden(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='BenLaden',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=50,
                     health_states=BENLADEN_HEALTH_STATES,
                     bubbles={"small": 20, "medium": 0, "big": 0},
                     radius=144,
                     body=BENLADEN_BODY,
                     gun_type='GunBenLaden',
                     time=uniform(0, 1000),
                     w=choice([-0.18, 0.18]),
                     body_rect=pg.Rect(0, 0, 464, 464))

        self.trajectory = self.rose_curve_3


class MobBug(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='Bug',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=5,
                     health_states=BUG_HEALTH_STATES,
                     bubbles={"small": 3, "medium": 0, "big": 0},
                     radius=32,
                     body=BUG_BODY,
                     gun_type='GunBug',
                     time=uniform(0, 1000),
                     w=choice([-0.7, 0.7]),
                     body_rect=pg.Rect(0, 0, 136, 136))

        self.trajectory = self.rose_curve_1


class MobAnt(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='Ant',
                     x=SCR_W2 + choice([-400, 400]),
                     y=SCR_H2 + choice([-400, 400]),
                     health=4,
                     health_states=ANT_HEALTH_STATES,
                     bubbles={"small": 2, "medium": 0, "big": 0},
                     radius=40,
                     body=ANT_BODY,
                     gun_type='GunAnt',
                     time=uniform(0, 1000),
                     w=choice([-1.3, 1.3]),
                     body_rect=pg.Rect(0, 0, 152, 152))

        self.trajectory = self.rose_curve_4


class MobScarab(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='Scarab',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=6,
                     health_states=SCARAB_HEALTH_STATES,
                     bubbles={"small": 6, "medium": 0, "big": 0},
                     radius=42,
                     body=SCARAB_BODY,
                     gun_type='GunScarab',
                     time=uniform(0, 1000),
                     w=choice([-0.7, 0.7]),
                     body_rect=pg.Rect(0, 0, 144, 144))

        self.trajectory = self.rose_curve_1


class MobGull(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='Gull',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=5,
                     health_states=GULL_HEALTH_STATES,
                     bubbles={"small": 6, "medium": 0, "big": 0},
                     radius=56,
                     body=GULL_BODY,
                     gun_type='GunGull',
                     time=uniform(0, 1000),
                     w=choice([-0.7, 0.7]),
                     body_rect=pg.Rect(0, 0, 192, 192))

        self.trajectory = self.rose_curve_1


class MobMother(Mob):
    def __init__(self, name):
        Mob.__init__(self,
                     name=name,
                     x=SCR_W2,
                     y=SCR_H2,
                     health=90,
                     health_states=MOTHER_HEALTH_STATES,
                     bubbles={"small": 5, "medium": 0, "big": 1},
                     radius=152,
                     body=MOTHER_BODY,
                     gun_type='GunPeaceful',
                     time=uniform(0, 1000),
                     w=choice([-0.15, 0.15]),
                     body_rect=pg.Rect(0, 0, 416, 416))

        self.trajectory = self.rose_curve_1
        self.generation_time = 5000
        self.generation_cooldown = 7000

    def __mob_factory(self):
        if self.name == 'GullMother':
            return MobGull()
        if self.name == 'BugMother':
            return MobBug()
        if self.name == 'ScarabMother':
            return MobScarab()

    def generate_child(self, dt):
        child = []
        self.generation_time += dt
        if self.generation_time >= self.generation_cooldown:
            self.generation_time -= self.generation_cooldown
            mob = self.__mob_factory()
            mob.xo = self.xo
            mob.yo = self.yo
            mob.x = self.x
            mob.y = self.y
            mob.time = self.time
            mob.body.update(mob.x, mob.y, 0)
            child = [mob]
        return child

    def update_pos(self, dt, generated_mobs=list()):
        super().update_pos(dt, generated_mobs)
        generated_mobs.extend(self.generate_child(dt))


class MobGullMother(MobMother):
    def __init__(self):
        MobMother.__init__(self, name='GullMother')


class MobBugMother(MobMother):
    def __init__(self):
        MobMother.__init__(self, name='BugMother')


class MobScarabMother(MobMother):
    def __init__(self):
        MobMother.__init__(self, name='ScarabMother')


class MobCockroach(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='Cockroach',
                     x=SCR_W2 + choice([-400, 400]),
                     y=SCR_H2 + choice([-400, 400]),
                     health=10,
                     health_states=COCKROACH_HEALTH_STATES,
                     bubbles={"small": 5, "medium": 0, "big": 0},
                     radius=72,
                     body=COCKROACH_BODY,
                     gun_type='GunCockroach',
                     time=uniform(0, 1000),
                     w=choice([-1.3, 1.3]),
                     body_rect=pg.Rect(0, 0, 176, 176))

        self.trajectory = self.rose_curve_4

    def update_body_look(self):
        super().update_body_look()
        if self.health <= 3:
            self.gun = get_gun('GunPeaceful')


class MobBomberShooter(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='BomberShooter',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=27,
                     health_states=BOMBERSHOOTER_HEALTH_STATES,
                     bubbles={"small": 11, "medium": 0, "big": 0},
                     radius=120,
                     body=BOMBERSHOOTER_BODY,
                     gun_type='GunBomberShooter',
                     time=uniform(0, 1000),
                     w=choice([-0.45, 0.45]),
                     body_rect=pg.Rect(0, 0, 320, 320))

        self.trajectory = self.rose_curve_1


class MobBeetle(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='Beetle',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=30,
                     health_states=BEETLE_HEALTH_STATES,
                     bubbles={"small": 9, "medium": 0, "big": 0},
                     radius=112,
                     body=BEETLE_BODY,
                     gun_type='GunBeetle',
                     time=uniform(0, 1000),
                     w=choice([-0.45, 0.45]),
                     body_rect=pg.Rect(0, 0, 368, 368))

        self.trajectory = self.rose_curve_1

    def update_body_look(self):
        super().update_body_look()
        if self.health <= 6 and self.gun.cooldown_time == 450:
            self.gun = get_gun('GunBeetleReserve')


class MobSpreader(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='Spreader',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=18,
                     health_states=SPREADER_HEALTH_STATES,
                     bubbles={"small": 15, "medium": 0, "big": 0},
                     radius=83,
                     body=SPREADER_BODY,
                     gun_type='GunSpreader',
                     time=uniform(0, 1000),
                     w=choice([-0.15, 0.15]),
                     body_rect=pg.Rect(0, 0, 176, 176))

        self.trajectory = self.rose_curve_1


class MobBigEgg(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='BigEgg',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=50,
                     health_states=BIGEGG_HEALTH_STATES,
                     bubbles={"small": 15, "medium": 0, "big": 0},
                     radius=120,
                     body=BIGEGG_BODY,
                     gun_type='GunBigEgg',
                     time=uniform(0, 1000),
                     w=choice([-0.6, 0.6, -0.55, 0.55]),
                     body_rect=pg.Rect(0, 0, 240, 240))

        self.trajectory = self.rose_curve_2


class MobSpider(Mob):
    def __init__(self):
        Mob.__init__(self,
                     name='Spider',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=130,
                     health_states=SPIDER_HEALTH_STATES,
                     bubbles={"small": 12, "medium": 0, "big": 0},
                     radius=152,
                     body=SPIDER_BODY,
                     gun_type='GunSpider',
                     time=uniform(0, 1000),
                     w=choice([-0.45, 0.45]),
                     body_rect=pg.Rect(0, 0, 368, 368))

        self.trajectory = self.rose_curve_2

    def update_body_look(self):
        super().update_body_look()
        if self.health <= 70:
            self.gun.small_gun_is_alive = False


class MobMachineGunner(Mob):
    def __init__(self):

        Mob.__init__(self,
                     name='MachineGunner',
                     x=SCR_W2,
                     y=SCR_H2,
                     health=50,
                     health_states=MACHINEGUNNER_HEALTH_STATES,
                     bubbles={"small": 8, "medium": 0, "big": 0},
                     radius=88,
                     body=MACHINEGUNNER_BODY,
                     gun_type='GunMachineGunner',
                     w=choice([-0.8, 0.8]),
                     body_rect=pg.Rect(0, 0, 208, 208))

        self.trajectory = self.rose_curve_2


class MobTurret(Mob):
    def __init__(self):
        r, fi = uniform(0, 800), uniform(0, 2*pi)

        Mob.__init__(self,
                     name='Turret',
                     x=SCR_W2 + r*cos(fi),
                     y=SCR_H2 - r*sin(fi),
                     health=55,
                     health_states=TURRET_HEALTH_STATES,
                     bubbles={"small": 18, "medium": 0, "big": 0},
                     radius=115,
                     body=TURRET_BODY,
                     gun_type='GunTurret',
                     time=uniform(0, 1000),
                     w=-1,
                     body_rect=pg.Rect(0, 0, 368, 368))

        self.update_body(0, (0, 0))

    def update_body(self, dt, target=(0, 0)):
        self.body.update(self.x, self.y, dt, self.gun.target, 0)


def get_mob(name):
    if name == 'BossSkeleton': return MobBossSkeleton()
    if name == 'BossLeg': return MobBossLeg()
    if name == 'BossHandLeft': return MobBossHand(side='left')
    if name == 'BossHandRight': return MobBossHand(side='right')
    if name == 'BossHead': return MobBossHead()
    if name == 'Infusoria': return MobInfusoria()
    if name == 'Cell': return MobCell()
    if name == 'Ameba': return MobAmeba()
    if name == 'Baby': return MobBaby()
    if name == 'Turtle': return MobTurtle(damaging=False)
    if name == 'Turtle_dmg': return MobTurtle(damaging=True)
    if name == 'Terrorist': return MobTerrorist()
    if name == 'Bug': return MobBug()
    if name == 'Ant': return MobAnt()
    if name == 'Scarab': return MobScarab()
    if name == 'Gull': return MobGull()
    if name == 'GullMother': return MobGullMother()
    if name == 'Cockroach': return MobCockroach()
    if name == 'BenLaden': return MobBenLaden()
    if name == 'BomberShooter': return MobBomberShooter()
    if name == 'Beetle': return MobBeetle()
    if name == 'Spreader': return MobSpreader()
    if name == 'BigEgg': return MobBigEgg()
    if name == 'Spider': return MobSpider()
    if name == 'MachineGunner': return MobMachineGunner()
    if name == 'Turret': return MobTurret()


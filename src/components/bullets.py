from math import cos, sin, pi, hypot
from random import uniform, choice
import pygame as pg

from data.constants import *
from data.bullets import *
from .body import Body
from .utils import *


class Bullet:
    """ a parent class for all bullets classes """
    def __init__(self, x, y, radius, damage, vel, angle, body, hit_effect=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.VELOCITY = vel
        self.vel_x = vel * cos(angle)
        self.vel_y = -vel * sin(angle)
        self.damage = damage
        self.hit_effect = self.set_hit_effect(hit_effect, damage)
        self.body = body if isinstance(body, pg.Surface) else Body(body)
        self.hit_the_target = False

    @property
    def is_outside(self):
        return not circle_collidepoint(SCR_W2, SCR_H2, ROOM_RADIUS, self.x, self.y)

    @property
    def killed(self):
        return self.hit_the_target or self.is_outside

    @staticmethod
    def set_hit_effect(hit_effect, damage):
        if hit_effect is not None:
            return hit_effect
        if damage <= -5: return 'BigHitLines'
        if damage: return 'SmallHitLines'
        return 'VioletHitCircle'

    def update_vel(self, angle):
        self.vel_x = self.VELOCITY * cos(angle)
        self.vel_y = -self.VELOCITY * sin(angle)

    def update_pos(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

    def update_body(self, dt):
        self.body.update(self.x, self.y, dt)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.body.move(dx, dy)

    def draw(self, surface, dx, dy):
        self.body.draw(surface, dx, dy)


class RegularBullet(Bullet):
    """ A bullet with uniform rectilinear motion """
    def __init__(self, x, y, damage, vel, angle, body, hit_effect=None):
        super().__init__(x, y, 0.8 * body[0][0], damage, vel,
                         angle, body, hit_effect=hit_effect)
        self.body.update(x, y, 0)

    def update_color(self, dt):
        pass

    def update(self, dt):
        self.update_pos(dt)
        self.update_body(dt)


class ExplodingBullet(RegularBullet):
    """
     Bullet moves evenly and rectilinearly and explodes
     from contact with the enemy, damaging others.

    """
    def __init__(self, x, y, angle):
        super().__init__(x, y, -21, HF(1.1), angle,
                         BULLET_BODIES["BigBullet_1"],
                         hit_effect='PowerfulExplosion')

        self.colors = {1: DARK_RED, -1: LIGHT_RED}
        self.color_switch = 1
        self.T = 80
        self.color_time = 0
        self.explosion_radius = H(600)

    def change_color(self):
        self.color_switch *= -1
        self.body.circles[0].color = self.colors[self.color_switch]

    def update(self, dt):
        super().update(dt)
        self.color_time += dt
        if self.color_time >= 0.75 * self.T and self.color_switch == 1:
            self.change_color()
        elif self.color_time >= self.T and self.color_switch == -1:
            self.change_color()
            self.color_time -= self.T


class Mine(Bullet):
    """Mine doesn't move and deals damage to a tank that moved too close. """
    def __init__(self, x, y, body):
        super().__init__(x, y, HF(18), -10, 0, 0, body, hit_effect='RedHitCircle')

        angle = uniform(0, 2 * pi)
        for circle in self.body.circles:
            circle.angle += angle
        self.body.update(x, y, 0)

        # bullet switches colors periodically
        self.colors = {1: self.body.circles[0].color, -1: LIGHT_RED}
        self.color_switch = 1
        self.T = 240
        self.color_time = uniform(0, self.T)

    def change_color(self):
        self.color_switch *= -1
        self.body.circles[3].color = self.colors[self.color_switch]

    def update_color(self, dt):
        self.color_time += dt
        if self.color_time >= 0.75 * self.T and self.color_switch == 1:
            self.change_color()
        elif self.color_time >= self.T and self.color_switch == -1:
            self.change_color()
            self.color_time -= self.T

    def update(self, dt):
        self.update_color(dt)


class OrbitalSeeker(Bullet):
    """
    Bullet has two states: 'orbiting', when it rotates around the player;
                           'not orbiting', when it moves as a regular bullet.
    Initially bullet is orbiting. If some target intersects with bullet's searching area,
    bullet starts moving evenly and rectilinearly to a target's position.

    """
    def __init__(self, x, y):
        super().__init__(x, y, HF(12), -7, HF(1.6), 0, BULLET_BODIES["Shuriken"])
        self.dist = HF(128)
        self.is_orbiting = True
        self.angle = 0
        self.angular_vel = -0.002 * pi
        self.health = 1
        self.search_area_rect = pg.Rect(x - H(150), y - H(150), H(300), H(300))
        self.update_polar_coords(x, y)
        self.hit_effect = 'RedHitCircle'

    @property
    def killed(self):
        return self.hit_the_target or (not self.is_orbiting and self.is_outside)

    def is_near_mob(self, mob):
        return self.search_area_rect.colliderect(mob.body_rect)

    def update_polar_coords(self, x, y, dt=0):
        self.angle += self.angular_vel * dt
        self.angle %= 2 * pi
        self.x = x + self.dist * cos(self.angle)
        self.y = y - self.dist * sin(self.angle)
        self.search_area_rect.center = self.x, self.y
        self.body.update(self.x, self.y, 0)

    def set_vel(self, mob):
        """
        Method is called when a target intersected with orbital seeker searching area.
        Sets x- and y- velocity components according to target position.

        """

        if mob.is_paralyzed or mob.body.is_frozen:
            angle = calculate_angle(self.x, self.y, mob.x, mob.y)
        else:
            dt = hypot(self.x - mob.x, self.y - mob.y) / self.VELOCITY
            angle = calculate_angle(self.x, self.y, *mob.shift(mob.angular_vel * dt))
        self.update_vel(angle)

    def update_pos(self, dt):
        super().update_pos(dt)
        self.search_area_rect.center = self.x, self.y
        self.body.update(self.x, self.y, 0)

    def check_targets(self, mobs):
        for mob in mobs:
            if self.is_near_mob(mob):
                self.is_orbiting = False
                self.set_vel(mob)
                break

    def update(self, dt, player_x, player_y, mobs):
        if self.is_orbiting:
            self.update_polar_coords(player_x, player_y, dt)
            self.check_targets(mobs)
        else:
            self.update_pos(dt)


class Seeker(Bullet):
    """ A bullet which moves with constant velocity and follows a moving target.
        Therefore, the x- and y-components of velocity are changing. """
    def __init__(self, x, y, start_angle, maneuvering_angle, radius, damage, vel, body):
        super().__init__(x, y, radius, damage, vel, 0, body)

        self.body.update(x, y, 0)
        self.update_vel(start_angle)
        self.rearrangement_angle = choice((-maneuvering_angle, maneuvering_angle))
        self.maneuvering_angle = maneuvering_angle
        self.health = 1
        self.hit_effect = 'RedHitCircle'
        self.target = None
        self.is_infected = False

    @property
    def killed(self) -> bool:
        return self.hit_the_target or self.health <= 0

    @property
    def no_target(self):
        return self.target is None or self.target.health <= 0

    def collide_bullet(self, bul_x, bul_y, bul_r):
        return circle_collidepoint(self.x, self.y, self.radius + bul_r, bul_x, bul_y)

    def handle_injure(self, damage):
        self.health += damage

    def set_target(self, targets):
        return min(targets, key=lambda t: hypot(self.x - t.x, self.y - t.y))

    def update(self, dt, targets):
        if self.no_target:
            self.target = self.set_target(targets)

        angle = calculate_angle(self.x, self.y, self.target.x, self.target.y)
        vel_angle = calculate_angle(0, 0, self.vel_x, self.vel_y)
        if abs(vel_angle - angle) > pi/2:
            self.update_vel(vel_angle - self.rearrangement_angle)
        elif vel_angle - angle > 0:
            self.update_vel(vel_angle - self.maneuvering_angle)
        else:
            self.update_vel(vel_angle + self.maneuvering_angle)
        self.update_pos(dt)
        self.body.update(self.x, self.y, dt, self.x + self.vel_x, self.y + self.vel_y)


class PlayerVirus(Seeker):
    def __init__(self, x, y, start_angle):
        super().__init__(x, y, start_angle, 0.04, HF(18), -1, 0.6, BULLET_BODIES['PlayerVirus'])

    @property
    def no_target(self):
        return super().no_target or self.target.is_infected

    def set_target(self, targets):
        current_target = None
        for target in targets:
            current_target = target
            if not target.is_infected:
                return target
        return current_target


class PlayerSeeker(Seeker):
    def __init__(self, x, y, start_angle, body="HomingMissile_1", vel=HF(0.75)):
        super().__init__(x, y, start_angle, 0.04, HF(10), -5, vel, BULLET_BODIES[body])


class LeecherBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 18, -7, HF(1.6), angle,
                         BULLET_BODIES['LeecherBullet'],
                         hit_effect='RedHitCircle')

    def update(self, dt):
        self.update_pos(dt)
        self.body.update(self.x, self.y, dt, self.x + self.vel_x, self.y + self.vel_y)


class Drone(Bullet):
    def __init__(self, x, y, angle, name, player):
        super().__init__(x, y, 0, 0, HF(0.7), angle, BULLET_BODIES[name])
        self.player = player
        self.name = name
        self.time = 0
        self.mitosis_time = 300
        self.is_divided = False
        self.angle = angle

    def divide(self):
        self.is_divided = True
        if self.name == "TinyDrone":
            self.player.seekers.append(Seeker(self.x, self.y, self.angle, 0.06, 0,
                                              -7, HF(1.1), BULLET_BODIES["TinyDrone"]))
        else:
            if self.name == "BigDrone": child_name = "MediumDrone"
            elif self.name == "MediumDrone": child_name = "SmallDrone"
            else: child_name = "TinyDrone"
            for k in (-1, 1):
                angle = self.angle + k * uniform(0.2*pi, 0.8*pi)
                self.player.drones.append(Drone(self.x, self.y, angle, child_name, self.player))

    def update(self, dt):
        self.update_pos(dt)
        self.body.update(self.x, self.y, dt, self.x + self.vel_x, self.y + self.vel_y)
        self.time += dt
        if self.time >= self.mitosis_time:
            self.divide()


class PierceBullet(Bullet):
    """ A bullet that can pass through many enemies. """
    def __init__(self, x, y, damage, vel, angle, body, hit_effect=None):
        super().__init__(x, y, HF(12), damage, vel, angle, body, hit_effect=hit_effect)
        self.body = pg.transform.rotate(body, angle * 180 / pi)
        self.x = x - self.body.get_width() / 2
        self.y = y - self.body.get_height() / 2
        self.attacked_mobs = []  # contains mobs attacked by this bullet

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update_body(self, dt):
        pass

    def update(self, dt):
        self.update_pos(dt)

    def draw(self, surface, dx, dy):
        surface.blit(self.body, (int(self.x - dx), int(self.y - dy)))


class ExplosivePierceBullet(PierceBullet):
    def __init__(self, *args):
        super().__init__(*args, hit_effect='SmallPowerfulExplosion')
        self.explosion_radius = H(130)


class FrangibleBullet(Bullet):
    """Bullet moves evenly and rectilinearly until its timer achieves fragmentation time.
     After this bullet explodes to form fragments scattering in all directions.
     If bullet collides with an object before fragmentation_time, it deals
     damage as a regular bullet and then disappears.
    """
    def __init__(self, x, y, angle, body):
        super().__init__(x, y, HF(20), -40, HF(0.8), angle, body)
        self.body.update(x, y, 0)
        self.time = 0
        self.fragmentation_time = 1000

    def update(self, dt, bullets):
        self.update_pos(dt)
        self.body.update(self.x, self.y, dt)
        self.time = min(self.fragmentation_time, self.time + dt)
        if self.time == self.fragmentation_time:
            self.hit_the_target = True
            fragments = [
                PierceBullet(self.x, self.y, -8, HF(2.1), i * pi / 180, BULLET_BODIES["SniperBullet"])
                for i in range(0, 360, 12)
            ]
            bullets.extend(fragments)


class AirBullet(RegularBullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, -1, HF(1.1), angle, BULLET_BODIES["AirBullet"])
        self.bubbles = {"small": 2}
        self.attacked_mobs = []


__all__ = [

    "RegularBullet",
    "ExplodingBullet",
    "Mine",
    "OrbitalSeeker",
    "Seeker",
    "PlayerSeeker",
    "LeecherBullet",
    "PierceBullet",
    "ExplosivePierceBullet",
    "FrangibleBullet",
    "AirBullet",
    "Drone",
    "PlayerVirus"

]

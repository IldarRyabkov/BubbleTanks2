from .utils import circle_collidepoint


class BaseMob:
    def __init__(self,
                 x,
                 y,
                 health,
                 max_health,
                 radius,
                 body,
                 weapons):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.radius = radius
        self.body = body
        self.weapons = weapons

        self.sticky = False
        self.sticky_time = 0
        self.sticky_cooldown = 2200

        self.stunned = False
        self.stunned_time = 0
        self.stunned_cooldown = 2000

    def become_sticky(self):
        self.sticky = True
        self.sticky_time = 0

    def stop_being_sticky(self):
        self.sticky = False
        self.sticky_time = 0

    def become_stunned(self):
        self.stunned = True
        self.stunned_time = 0

    def update_sticky_state(self, dt):
        if self.sticky:
            self.sticky_time += dt
            if self.sticky_time >= self.sticky_cooldown:
                self.stop_being_sticky()

    def update_stunned_state(self, dt):
        if self.stunned:
            self.stunned_time += dt
            if self.stunned_time >= self.stunned_cooldown:
                self.stunned_time = 0
                self.stunned = False

    def set_health(self, new_health: int):
        self.health = new_health
        self.update_component_states()

    def update_health(self, delta_health: int):
        pass

    def update_component_states(self):
        """ Method is called when mob's health has changed.
        Updates states of mobs's gun and superpower
        according to new mob's health.
        """
        state = max(0, self.health)
        self.body.update_state(state)
        self.weapons.update_state(state)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def collide_bullet(self, bul_x, bul_y, bul_r) -> bool:
        return circle_collidepoint(self.x, self.y, self.radius + bul_r, bul_x, bul_y)

    def receive_damage(self, damage, play_sound=True):
        if damage:
            self.update_health(delta_health=damage)
        else:
            self.become_sticky()

    def update(self, dt):
        pass

    def draw(self, screen, dx=0, dy=0):
        pass


__all__ = ["BaseMob"]

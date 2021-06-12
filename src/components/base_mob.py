from .utils import circle_collidepoint


class BaseMob:
    def __init__(self,
                 x,
                 y,
                 health,
                 max_health,
                 health_states,
                 radius,
                 body,
                 gun):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.health_states = health_states
        self.health_interval = None
        self.radius = radius
        self.body = body
        self.gun = gun

        self.is_infected = False
        self.infection_time = 0
        self.infection_cooldown_time = 170

    @property
    def body_look_changed(self):
        left, right = self.health_interval
        return not left < self.health <= right

    def update_body_look(self):
        for circle in self.body.circles:
            circle.is_visible = True
        k = 0
        for i in range(len(self.health_states)):
            if self.health <= self.health_states[i][0]:
                k = i
        if k == len(self.health_states) - 1:
            self.health_interval = (0, self.health_states[k][0])
        else:
            self.health_interval = (self.health_states[k + 1][0], self.health_states[k][0])
        self.body.set_visible_circles(self.health_states[k][1::])
        self.gun.update_params(self.health)

    def collide_bullet(self, bul_x, bul_y, bul_r) -> bool:
        return circle_collidepoint(self.x, self.y, self.radius + bul_r, bul_x, bul_y)

    def handle_injure(self, damage):
        if damage:
            self.health += damage
            if self.body_look_changed:
                self.update_body_look()
        else:
            self.body.make_frozen()


__all__ = ["BaseMob"]

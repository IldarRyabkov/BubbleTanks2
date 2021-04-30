from objects.body import Body


class BaseMob:
    def __init__(self,
                 health,
                 max_health,
                 health_states,
                 radius,
                 body):
        self.health = health
        self.max_health = max_health
        self.health_states = health_states
        self.radius = radius
        self.body = Body(body)
        self.is_frozen = False
        self.frost_time = 0

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
        self.make_body_frozen() if self.is_frozen else self.make_body_unfrozen()

    def handle_injure(self, damage):
        if damage:
            self.health += damage
            self.update_body_look()
        else:
            self.make_frozen()

    def make_body_frozen(self):
        pass

    def make_body_unfrozen(self):
        pass

    def make_unfrozen(self):
        self.is_frozen = False
        self.frost_time = 0
        self.make_body_unfrozen()

    def make_frozen(self):
        self.is_frozen = True
        self.frost_time = 0
        self.make_body_frozen()

    def update_frozen_state(self, dt):
        if self.is_frozen:
            self.frost_time += dt
            if self.frost_time >= 3000:
                self.make_unfrozen()

from body import Body


class BaseMob:
    def __init__(self,
                 health,
                 max_health,
                 health_states,
                 radius,
                 body,
                 frozen_body=()):
        self.health = health
        self.max_health = max_health
        self.health_states = health_states
        self.radius = radius
        self.body = Body(body, frozen_body)

    def update_body_look(self):
        for circle in self.body.circles:
            circle.is_visible = True
        k = 0
        for i in range(len(self.health_states)):
            if self.health <= self.health_states[i][0]:
                k = i
        for i in range(1, len(self.health_states[k])):
            for j in range(self.health_states[k][i][0], self.health_states[k][i][1]):
                self.body.circles[j].is_visible = False

    def handle_injure(self, damage):
        if damage:
            self.health += damage
            self.update_body_look()
        else:
            self.body.make_frozen()


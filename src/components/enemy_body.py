from components.circle import make_circles_list


class EnemyBody:
    def __init__(self, owner, screen_rect, data):
        self.owner = owner
        self.angle = 0
        self.state = 0
        self.all_circles = make_circles_list(screen_rect, data["circles"])
        self.circles = self.init_circles(data)

    @property
    def current_circles(self) -> list:
        return self.circles[self.state]

    def init_circles(self, data: dict) -> dict:
        circles = {}
        for (left, right), indexes in data["circles states"].items():
            for state in range(left, right + 1):
                circles[state] = [self.all_circles[i] for i in indexes]
        return circles

    def update_state(self, state):
        self.state = state
        self.update_shape(0)

    def become_infected(self):
        for circle in self.all_circles:
            circle.become_infected()

    def update_shape(self, dt):
        x, y, angle = self.owner.x, self.owner.y, self.angle
        for circle in self.current_circles:
            circle.update_pos(x, y, dt, angle)

    def draw(self, surface, dx=0, dy=0):
        for circle in self.current_circles:
            if circle.is_on_screen:
                circle.update_glares(self.angle)
                circle.draw(surface, dx, dy)


__all__ = ["EnemyBody"]

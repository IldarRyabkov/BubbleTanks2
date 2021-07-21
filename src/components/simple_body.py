from components.circle import make_circles_list


class Body:
    """Used for bullets and pickup-bubbles. """
    def __init__(self, owner, screen_rect, circles_data):
        self.owner = owner
        self.circles = make_circles_list(screen_rect, circles_data)
        self.angle = 0
        self.update_shape(0)

    def rotate(self, angle):
        for circle in self.circles:
            circle.angle += angle

    def update_shape(self, dt):
        x, y, angle = self.owner.x, self.owner.y, self.angle
        for circle in self.circles:
            circle.update_pos(x, y, dt, angle)

    def draw(self, surface, dx, dy):
        for circle in self.circles:
            circle.update_glares(self.angle)
            circle.draw(surface, dx, dy)


__all_ = ["Body"]

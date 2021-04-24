import pygame as pg

WINDOW_CLOSED = 0
WINDOW_OPENING = 1
WINDOW_CLOSING = 2
WINDOW_OPENED = 3


class PopupWindow:
    """Base class for cooldown window and health window. """
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 vel: float,
                 duration: int,
                 image: str):
        self.x = x
        self.y = y
        self.Y_CLOSED = y
        self.Y_OPENED = y + height + 16 if vel > 0 else y - height - 16
        self.width = width
        self.height = height
        self.time = 0
        self.vel = vel
        self.duration = duration
        self.state = WINDOW_CLOSED
        img = pg.image.load(image).convert_alpha()
        self.background = pg.transform.scale(img, (width, height))

    def activate(self, *args, **kwargs):
        if self.state != WINDOW_OPENED:
            self.state = WINDOW_OPENING
        self.time = 0

    def reset(self):
        self.state = WINDOW_CLOSED
        self.time = 0
        self.y = self.Y_CLOSED

    def update_state(self, dt):
        k = 1 if self.vel > 0 else -1
        if self.state == WINDOW_OPENING:
            self.y += self.vel * dt
            if k * self.y > k * self.Y_OPENED:
                self.state = WINDOW_OPENED
                self.y = self.Y_OPENED
        elif self.state == WINDOW_CLOSING:
            self.y -= self.vel * dt
            if k * self.y < k * self.Y_CLOSED:
                self.state = WINDOW_CLOSED
                self.y = self.Y_CLOSED
        elif self.state == WINDOW_OPENED:
            self.time += dt
            if self.time >= self.duration:
                self.state = WINDOW_CLOSING
                self.time = 0

    def is_on_screen(self):
        k = 1 if self.vel > 0 else -1
        return k * self.Y_CLOSED < k * self.y <= k * self.Y_OPENED
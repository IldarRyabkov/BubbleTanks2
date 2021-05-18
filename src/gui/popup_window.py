import pygame as pg
from utils import HF
from numpy import sign


class State:
    CLOSED = 0
    OPENING = 1
    CLOSING = 2
    OPENED = 3


class PopupWindow:
    """Base class for cooldown window and health window. """
    def __init__(self,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 vel: float,
                 duration: int,
                 image: str):
        self.x = x
        self.y = y
        self.Y_CLOSED = y
        self.Y_OPENED = y + sign(vel) * (h + HF(16))
        self.w = w
        self.h = h
        self.time = 0
        self.vel = vel
        self.duration = duration
        self.state = State.CLOSED
        img = pg.image.load(image).convert_alpha()
        self.background = pg.transform.scale(img, (round(w), round(h)))

    @property
    def on_screen(self):
        k = sign(self.vel)
        return k * self.Y_CLOSED < k * self.y <= k * self.Y_OPENED

    def reset(self):
        """Method is called when a new game is started.
        Resets popup window state and parameters.
        """
        self.state = State.CLOSED
        self.time = 0
        self.y = self.Y_CLOSED

    def set(self, *args, **kwargs):
        """Sets popup window parameters. """
        pass

    def activate(self, *args, **kwargs):
        if self.state != State.OPENED:
            self.state = State.OPENING
        self.time = 0

    def update_state(self, dt):
        k = sign(self.vel)
        if self.state == State.OPENING:
            self.y += self.vel * dt
            if k * self.y > k * self.Y_OPENED:
                self.state = State.OPENED
                self.y = self.Y_OPENED
        elif self.state == State.CLOSING:
            self.y -= self.vel * dt
            if k * self.y < k * self.Y_CLOSED:
                self.state = State.CLOSED
                self.y = self.Y_CLOSED
        elif self.state == State.OPENED:
            self.time += dt
            if self.time >= self.duration:
                self.state = State.CLOSING
                self.time = 0


__all__ = ["PopupWindow"]

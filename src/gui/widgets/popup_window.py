import pygame as pg

from data.states import PopupWindowStates as St
from data.constants import WAIT
from components.utils import HF, sign
from .widget import Widget


class PopupWindow(Widget):
    """Base class for cooldown window and health window. """
    def __init__(self,
                 game,
                 x: float,
                 y: float,
                 w: float,
                 h: float,
                 vel: float,
                 duration: int,
                 image: str):
        super().__init__()
        self.game = game
        self.player = self.game.player
        self.x = x
        self.y = y
        self.Y_CLOSED = y
        self.Y_OPENED = y + sign(vel) * (h + HF(16))
        self.w = w
        self.h = h
        self.time = 0
        self.vel = vel
        self.duration = duration
        self.state = St.CLOSED
        img = pg.image.load(image).convert_alpha()
        self.background = pg.transform.scale(img, (round(w), round(h)))
        self.widgets = []

    @property
    def on_screen(self):
        k = sign(self.vel)
        return k * self.Y_CLOSED < k * self.y <= k * self.Y_OPENED

    def reset(self):
        """Method is called when a new game is started.
        Resets popup window state and parameters.
        """
        self.state = St.CLOSED
        self.time = 0
        self.y = self.Y_CLOSED

    def set(self, *args, **kwargs):
        """Sets popup window parameters. """
        pass

    def set_data(self):
        self.reset()
        self.set()

    def activate(self):
        if self.state != St.OPENED:
            self.state = St.OPENING
        self.time = 0

    def update(self, dt):
        yo = self.y
        self.update_state(dt)
        dy = self.y - yo
        for widget in self.widgets:
            widget.move(0, dy)

    def update_state(self, dt):
        k = sign(self.vel)
        if self.state == St.OPENING:
            self.y += self.vel * dt
            if k * self.y > k * self.Y_OPENED:
                self.state = St.OPENED
                self.y = self.Y_OPENED
        elif self.state == St.CLOSING:
            self.y -= self.vel * dt
            if k * self.y < k * self.Y_CLOSED:
                self.state = St.CLOSED
                self.y = self.Y_CLOSED
        elif self.state == St.OPENED:
            self.time += dt
            if self.time >= self.duration:
                self.state = St.CLOSING
                self.time = 0

    def draw(self, screen, animation_state=WAIT):
        if self.state == St.CLOSED:
            return
        screen.blit(self.background, (round(self.x), round(self.y)))
        for widget in self.widgets:
            widget.draw(screen)


__all__ = ["PopupWindow"]

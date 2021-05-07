import pygame as pg

from utils import HF, H
from gui.text import Text
from data.paths import FONT_1, PLAY_BUTTON
from data.colors import WHITE
from data.gui_texts import PLAY_BUTTON_TEXTS as TEXTS
from data.config import SCR_H, SCR_W2,  CLOSE, OPEN, WAIT, MAIN_MENU_ANIMATION_TIME as TIME


class PlayButton:
    """Button that is used in the Main menu to start the game. """
    K = 1.75  # scaling factor
    D = 0.005  # delta factor
    VEL = HF(0.704)
    A_MIN = HF(72)
    B_MIN = HF(56)
    A_MAX = K * A_MIN
    B_MAX = K * B_MIN
    ALPHA_MIN = 210
    ALPHA_MAX = 255
    A_DELTA = D * (A_MAX - A_MIN)
    B_DELTA = D * (B_MAX - B_MIN)
    ALPHA_DELTA = D * (ALPHA_MAX - ALPHA_MIN)

    def __init__(self):
        self.visible = True  # flag used not to draw button during hide animation

        self.x = SCR_W2
        self.y = SCR_H + self.B_MIN

        self.a = self.A_MIN
        self.b = self.B_MIN

        self.label = Text(SCR_W2, HF(680), FONT_1, H(58), WHITE, True)
        self.label_alpha = 0

        self.image = pg.image.load(PLAY_BUTTON).convert_alpha()
        self.alpha = self.ALPHA_MIN
        self.surface = None
        self.scale_surface()

    @property
    def cursor_on_button(self) -> bool:
        x, y = pg.mouse.get_pos()
        return (self.x - x) * (self.x - x) / (self.a * self.a) + \
               (self.y - y) * (self.y - y) / (self.b * self.b) <= 1

    def set_language(self, language):
        """Sets label of the button based on input language. """
        self.label.set_text(TEXTS[language])
        self.label.set_alpha(self.label_alpha)

    def scale_surface(self):
        self.surface = pg.transform.scale(self.image, (round(2 * self.a), round(2 * self.b)))
        self.surface.set_alpha(self.alpha)

    def scale(self, dt: int, increasing: bool):
        """Updates the size of the play button and the alpha-value of label
        based on whether the cursor is on the button.
        """
        # do not scale button when it is already maximised/minimised (for better game performance)
        if ((increasing and self.a == self.A_MAX) or
                (not increasing and self.a == self.A_MIN)):
            return

        k = 1 if increasing else -1

        self.a += k * self.A_DELTA * dt
        self.b += k * self.B_DELTA * dt
        self.alpha += k * self.ALPHA_DELTA * dt
        self.label_alpha += k * self.D * 255 * dt

        if self.a > self.A_MAX:
            self.a = self.A_MAX
            self.b = self.B_MAX
            self.alpha = self.ALPHA_MAX
            self.label_alpha = 255

        elif self.a < self.A_MIN:
            self.a = self.A_MIN
            self.b = self.B_MIN
            self.alpha = self.ALPHA_MIN
            self.label_alpha = 0

        self.label.set_alpha(self.label_alpha)
        self.scale_surface()

    def move(self, dy):
        """ Method is called when the Main menu is showing or hiding.
        Moves the button by the input offset.
        """
        self.y += dy

    def update(self, dt, animation_time, state):
        """Updates size, position and visibility of the button
        based on the state of pause menu.
        """
        self.visible = True
        if state == WAIT:
            self.scale(dt, self.cursor_on_button)
        elif state == CLOSE:
            if animation_time <= 0.2 * TIME:
                self.visible = bool((animation_time // 50) % 2 != 0)
            elif animation_time < 0.5 * TIME:
                self.scale(dt, False)
            elif animation_time <= 0.7 * TIME:
                self.move(self.VEL * dt)
        elif state == OPEN and TIME * 5/6 <= animation_time <= TIME:
            self.move(-self.VEL * dt)

    def draw(self, screen):
        if self.visible:
            x = round(self.x - self.surface.get_width() / 2)
            y = round(self.y - self.surface.get_height() / 2)
            screen.blit(self.surface, (x, y))
        self.label.draw(screen)


__all__ = ["PlayButton"]

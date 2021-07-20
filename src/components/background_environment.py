import pygame as pg
from math import cos, sin, sqrt, ceil, pi, hypot

from assets.paths import *
from data.constants import *
from data.languages import TEXTS

from gui.widgets.text_widget import TextWidget

from components.bubble_tanks_world import BOSS_PIECES
from components.utils import *


def room_bg() -> list:
    """The background of the room is a very large surface with transparency.
    It takes a very long time to draw, so this surface is divided into many
    subsurfaces to draw only those that are currently on the screen.
    This significantly increases the FPS.

    The screen height MUST be a multiple of 6 for the subsurface
    dimensions to be calculated without mathematical errors!
    """
    img = pg.transform.scale(pg.image.load(ROOM_BG).convert_alpha(),
                             (2 * ROOM_RADIUS, 2 * ROOM_RADIUS))
    bg = []
    r = ROOM_RADIUS
    w = ROOM_RADIUS / 4
    step = ROOM_RADIUS / 28
    y = 0
    for i in range(7):
        d = sqrt(r * r - (r - y - step) * (r - y - step))
        rect_h = ceil(step) if int(y) < y else step
        bg.append(img.subsurface(pg.Rect(r - d, int(y), 2 * d, rect_h)))
        y += step

    for i in range(21):
        d1 = sqrt(r * r - (r - y - step) * (r - y - step))
        d2 = ceil(sqrt((r - w) * (r - w) - (r - y) * (r - y)))
        rect_h = ceil(step) if int(y) < y else step
        bg.append(img.subsurface(pg.Rect(r - d1, int(y), d1 - d2, rect_h)))
        bg.append(img.subsurface(pg.Rect(r + d2, int(y), d1 - d2, rect_h)))
        y += step

    for i in range(21):
        d1 = sqrt(r * r - (r - y) * (r - y))
        d2 = ceil(sqrt((r - w) * (r - w) - (r - y - step) * (r - y - step)))
        rect_h = ceil(step) if int(y) < y else step
        bg.append(img.subsurface(pg.Rect(r - d1, int(y), d1 - d2, rect_h)))
        bg.append(img.subsurface(pg.Rect(r + d2, int(y), d1 - d2, rect_h)))
        y += step

    for i in range(7):
        d = sqrt(r * r - (r - y) * (r - y))
        rect_h = ceil(step) if int(y) < y else step
        bg.append(img.subsurface(pg.Rect(r - d, int(y), 2 * d, rect_h)))
        y += step

    return bg


class RoomGlare:
    def __init__(self,
                 x: float,
                 y: float,
                 diam: float,
                 alpha: int):
        self.x = x - diam / 2
        self.y = y - diam / 2
        self.image = pg.image.load(ROOM_GLARE_BG).convert_alpha()
        self.image.set_alpha(alpha)
        self.surface = pg.transform.smoothscale(self.image, (round(diam), round(diam)))

    def draw(self, surface, dx, dy):
        surface.blit(self.surface, (round(self.x - dx), round(self.y - dy)))


class PlayerHalo:
    def __init__(self):
        self.x = None
        self.y = None
        self.radius = None
        self.surface = None
        self.set_size(HF(160))

    def set_size(self, radius: float):
        self.radius = radius
        self.x = SCR_W2 - radius
        self.y = SCR_H2 - radius
        self.surface = pg.Surface((round(2*radius), round(2*radius)))
        self.surface.set_colorkey(COLOR_KEY)

    def draw(self, surface, offset, offset_new):
        if hypot(*offset) > ROOM_RADIUS - self.radius - HF(24):
            self.surface.fill(COLOR_KEY)
            r = round(self.radius)
            pg.draw.circle(self.surface, WHITE, (r, r), r)
            pg.draw.circle(self.surface, PLAYER_BG_COLOR, (r, r),  round(self.radius - HF(8)))
            pg.draw.circle(self.surface, COLOR_KEY,
                           (round(self.radius - offset[0]), round(self.radius - offset[1])),
                           round(ROOM_RADIUS - HF(24)))

            if offset_new is not None:
                pg.draw.circle(self.surface, COLOR_KEY,
                               (round(self.radius - offset_new[0]), round(self.radius - offset_new[1])),
                               round(ROOM_RADIUS - HF(24)))

            surface.blit(self.surface, (round(self.x), round(self.y)))


class DestinationCircle:
    """Background effect which appears when player
    is being transported from one room to another.
    Draws a circle at player's destination point.
    """
    def __init__(self):
        self.x = 0
        self.y = 0

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, dx, dy):
        pos = (round(self.x - dx), round(self.y - dy))
        pg.draw.circle(screen, ROOM_COLOR, pos, H(18))
        pg.draw.circle(screen, WHITE, pos, H(12))


class PlayerTrace:
    """Background effect which appears when player
    is being transported from one room to another.
    Imitates trace of bubbles that player's tank leaves on its way.
    """
    coords = ()  # coordinates of circles that will be drawn

    def set_coords(self, x, y, dist, angle):
        self.coords = (
            (x + dist * cos(angle), y - dist * sin(angle)),

            (x + dist * cos(angle) + HF(96) * cos(angle + 0.15 * pi),
             y - dist * sin(angle) - HF(96) * sin(angle + 0.15 * pi)),

            (x + dist * cos(angle) + HF(64) * cos(angle - 0.25 * pi),
             y - dist * sin(angle) - HF(64) * sin(angle - 0.25 * pi))
        )

    def draw(self, screen, dx, dy):
        for i, (x, y) in enumerate(self.coords):
            radius = H(24) if i == 0 else H(16)
            pg.draw.circle(screen, WHITE, (round(x - dx), round(y - dy)), radius, H(4))


class BackgroundEnvironment:
    """Stores, updates and draws all background game objects"""
    def __init__(self, game):
        self.game = game

        self.bg = pg.transform.scale(pg.image.load(BG).convert(), SCR_SIZE)
        self.room_bg = room_bg()
        self.player_halo = PlayerHalo()
        self.destination_circle = DestinationCircle()
        self.player_trace = PlayerTrace()

        # Normally mobs in a neighbour rooms are not being drawn cause they cannot be seen from current room.
        # but Boss Skeleton is too large, so it is stored separately as a background environment object, to be drawn
        # when the Final Boss is in the current room, or if Boss skeleton is partly visible from the neighbour room.
        self.boss_skeleton = None

        # Boss disposition ('in current room', 'in neighbour room', 'far away')
        # is used to check if we should draw Boss skeleton or not.
        self.boss_disposition = BOSS_IS_FAR_AWAY
        self.boss_pos = None
        self.room_pos = (0, 0)

        # New boss disposition temporary stores the next boss disposition after transportation of the player.
        # It is used to check if we should draw boss skeleton during transportation or not.
        # When transportation is done, boss disposition is replaced with the new boss disposition.
        self.new_boss_disposition = None

        # New hint widget is a temporary text widget used to draw hint text
        # of the new room during player's transportation.
        # After transportation is done, hint widget is replaced with the new hint widget.
        self.hint_widget = TextWidget(WF(640), HF(170), FONT_1, H(75), WHITE, 1, H(890))
        self.new_hint_widget = TextWidget(WF(640), HF(170), FONT_1, H(75), WHITE, 1, H(890))

        self.room_glares = (
            RoomGlare(SCR_W2 - HF(550), SCR_H2 - HF(565), HF(380), 255),
            RoomGlare(SCR_W2 - HF(260), SCR_H2 - HF(810), HF(176), 255),
            RoomGlare(SCR_W2 + HF(550), SCR_H2 + HF(565), HF(380), 110),
            RoomGlare(SCR_W2 + HF(260), SCR_H2 + HF(810), HF(176), 110)
        )

        # Hints shown in visited rooms are stored in hints_history dictionary.
        # Key is room position, and value is hint text for this room.
        self.hints_history = dict()
        self.hint_texts = None
        self.hints_count = 0
        self.language = None

    @property
    def boss_offset(self):
        dx = (self.boss_pos[0] - self.room_pos[0]) * DIST_BETWEEN_ROOMS
        dy = (self.boss_pos[1] - self.room_pos[1]) * DIST_BETWEEN_ROOMS
        return dx, dy

    def set_data(self, data: dict):
        self.player_halo.set_size(self.game.player.bg_radius)
        self.boss_disposition = data["boss disposition"],
        self.boss_pos = data["boss position"]
        self.room_pos = tuple(data["current room"])
        self.hints_history.clear()
        for room, hint in data["hints history"].items():
            room = tuple(map(int, room.split()))
            self.hints_history[room] = hint

    def set_language(self, language):
        self.language = language
        self.hint_texts = TEXTS["room hints"][self.language]
        if self.room_pos in self.hints_history:
            text = self.hint_texts[self.hints_history[self.room_pos]]
            self.hint_widget.set_text(text)
        else:
            self.hint_widget.clear()

    def boss_visible_from_neighbour_room(self, player_dy):
        """Returns True, if Boss skeleton is partly visible from a neighbour room.
        It happens, if the room with Final Boss is located below or above the current room,
        and player is close enough to border of the room to see a part of Boss skeleton.
        """
        return (self.boss_pos[0] == self.room_pos[0] and
                abs(self.boss_offset[1] - player_dy) <= ROOM_RADIUS + SCR_W2 + HF(360))

    def set_new_boss_disposition(self, new_room_pos: tuple, new_mobs: list):
        """Sets the new boss disposition due to transportation of the player to the next room.
        If the new boss disposition becomes equal to "far away",
        updates Boss skeleton position to draw it properly.
        """
        self.room_pos = new_room_pos
        x, y = new_room_pos

        if any(mob.name in BOSS_PIECES for mob in new_mobs):
            self.new_boss_disposition = BOSS_IN_CURRENT_ROOM
            self.boss_pos = new_room_pos

        elif (self.boss_disposition == BOSS_IN_CURRENT_ROOM or
              (self.boss_pos is not None and
               hypot(x - self.boss_pos[0], y - self.boss_pos[1]) == 1)):
            self.new_boss_disposition = BOSS_IN_NEIGHBOUR_ROOM

        else:
            self.new_boss_disposition = BOSS_IS_FAR_AWAY

        if self.new_boss_disposition != BOSS_IS_FAR_AWAY:
            dx, dy = self.boss_offset
            self.boss_skeleton.move_to(SCR_W2 + dx, SCR_H2 + dy)

    def set_params_after_transportation(self):
        """Replaces hint widget of the old room with a hint widget of the next room.
        and old boss disposition with the new boss disposition.
        """
        self.boss_disposition = self.new_boss_disposition
        self.hint_widget.replace_with(self.new_hint_widget)
        self.new_hint_widget.clear()

    def set_next_hint(self):
        """Method is called when player is being transported to the next room.
        Sets new hint text widget, explaining the rules of the game.
        """
        if self.room_pos in self.hints_history:
            text = self.hint_texts[self.hints_history[self.room_pos]]
            self.new_hint_widget.set_text(text)
        else:
            top = len(self.hints_history)
            if top <= 4 or self.game.player.level >= 2 and top == 5:
                text = self.hint_texts[top]
                self.new_hint_widget.set_text(text)
                self.hints_history[self.room_pos] = top

    def set_player_halo(self, radius):
        self.player_halo.set_size(radius)

    def set_player_trace(self, x, y, dist, alpha):
        self.player_trace.set_coords(x, y, 0.05 * dist, alpha)

    def set_destination_circle(self, x, y):
        self.destination_circle.set_pos(x, y)

    def draw_bg(self, screen):
        screen.blit(self.bg, (0, 0))

    def draw_room_bg(self, screen, dx, dy):
        for surface in self.room_bg:
            pos = surface.get_offset()
            x = SCR_W2 - ROOM_RADIUS - dx + pos[0]
            y = SCR_H2 - ROOM_RADIUS - dy + pos[1]
            screen.blit(surface, (x, y))

    def draw_hint(self, surface, dx, dy):
        self.hint_widget.draw(surface, dx, dy)

    def draw_new_hint(self, surface, dx, dy):
        self.new_hint_widget.draw(surface, dx, dy)

    def draw_player_halo(self, screen, offset_old, offset_new=None):
        self.player_halo.draw(screen, offset_old, offset_new)

    def draw_room_glares(self, surface, dx, dy):
        for glare in self.room_glares:
            glare.draw(surface, dx, dy)

    def draw_player_trace(self, screen, dx, dy, time):
        if time >= 0.1 * TRANSPORTATION_TIME:
            self.player_trace.draw(screen, dx, dy)

    def draw_destination_circle(self, surface, dx, dy):
        self.destination_circle.draw(surface, dx, dy)

    def draw_boss_skeleton(self, surface, dx, dy, transportation=False):
        if transportation:
            if (self.boss_disposition == BOSS_IN_CURRENT_ROOM or
                    self.new_boss_disposition == BOSS_IN_CURRENT_ROOM):
                self.boss_skeleton.draw(surface, dx, dy)

        elif (self.boss_disposition == BOSS_IN_CURRENT_ROOM
              or (self.boss_disposition == BOSS_IN_NEIGHBOUR_ROOM and
                  self.boss_visible_from_neighbour_room(dy))):
            self.boss_skeleton.draw(surface, dx, dy)


__all__ = ["BackgroundEnvironment"]

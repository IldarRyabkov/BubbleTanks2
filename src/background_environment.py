import pygame as pg
from math import cos, sin, sqrt, ceil, pi, hypot
from numpy import array

from body import Body
from data.paths import *
from data.config import *
from data.colors import *
from gui.text import Text
from data.gui_texts import ROOM_HINTS
from data.mobs import BOSS_SKELETON_BODY
from mob_generator import BOSS_PIECES
from utils import H, HF, WF, scaled_body


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
                 diam: float):
        self.x = x - diam / 2
        self.y = y - diam / 2
        self.image = pg.image.load(ROOM_GLARE_BG).convert_alpha()
        self.surface = pg.transform.scale(self.image, (round(diam), round(diam)))

    def draw(self, surface, dx, dy):
        surface.blit(self.surface, (round(self.x - dx), round(self.y - dy)))


class PlayerHalo:
    def __init__(self):
        self.x = None
        self.y = None
        self.radius = None
        self.surface = None
        self.set_size(HF(160))

    def reset(self):
        self.__init__()

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
    def __init__(self):
        self.bg = pg.transform.scale(pg.image.load(BG).convert(), SCR_SIZE)
        self.room_bg = room_bg()
        self.player_halo = PlayerHalo()
        self.destination_circle = DestinationCircle()
        self.player_trace = PlayerTrace()

        # Normally mobs in a neighbour rooms are not being drawn for performance reasons,
        # but Boss Skeleton is too large, so it is stored separately as a background environment object, to be drawn
        # when the Final Boss is in the current room, or if Boss skeleton is partly visible from the neighbour room.
        self.boss_skeleton = Body(scaled_body(BOSS_SKELETON_BODY))

        # Boss disposition ('in current room', 'in neighbour room', 'far away')
        # is used to check if we should draw Boss skeleton or not.
        self.boss_disposition = BOSS_IS_FAR_AWAY
        self.boss_pos = None
        self.room_pos = array([0, 0])

        # New boss disposition temporary stores the next boss disposition after transportation of the player.
        # It is used to check if we should draw boss skeleton during transportation or not.
        # When transportation is done, boss disposition is replaced with the new boss disposition.
        self.new_boss_disposition = None

        # New hint widget is a temporary text widget used to draw hint text
        # of the new room during player's transportation.
        # After transportation is done, hint widget is replaced with the new hint widget.
        self.hint_widget = Text(WF(640), HF(170), FONT_1, H(75), WHITE, 1, H(890))
        self.new_hint_widget = Text(WF(640), HF(170), FONT_1, H(75), WHITE, 1, H(890))

        self.room_glares = (
            RoomGlare(SCR_W2 - HF(550), SCR_H2 - HF(565), HF(320)),
            RoomGlare(SCR_W2 - HF(260), SCR_H2 - HF(810), HF(176)),
            RoomGlare(SCR_W2 + HF(550), SCR_H2 + HF(565), HF(320)),
            RoomGlare(SCR_W2 + HF(260), SCR_H2 + HF(810), HF(176))
        )

        # Hints shown in visited rooms are stored in hints_history dictionary.
        # Key is room position, and value is hint text for this room.
        self.hints_history = dict()
        self.hint_texts = None
        self.language = None

    @property
    def boss_offset(self):
        return (self.boss_pos - self.room_pos) * DIST_BETWEEN_ROOMS

    def reset(self):
        """Method is called when a new game is started.
        Resets background environment parameters.
        """
        self.player_halo.reset()
        self.boss_disposition = BOSS_IS_FAR_AWAY
        self.boss_pos = None
        self.room_pos = array([0, 0])
        self.hints_history = dict()
        self.hint_texts = None

    def set_language(self, language):
        self.language = language
        self.hint_texts = ROOM_HINTS[self.language].copy()[:-1]  # hints without superpower hint
        text = self.hint_texts.pop(0)
        self.hint_widget.set_text(text)
        self.hints_history[(0, 0)] = text

    def boss_visible_from_neighbour_room(self, player_offset):
        """Returns True, if Boss skeleton is partly visible from a neighbour room.
        It happens, if the room with Final Boss is located below or above the current room,
        and player is close enough to border of the room to see a part of Boss skeleton.
        """
        return (self.boss_pos[0] == self.room_pos[0] and
                abs(self.boss_offset[1] - player_offset[1]) <= ROOM_RADIUS + SCR_W2 + HF(360))

    def set_new_boss_disposition(self, new_room_pos, new_mobs):
        """Sets the new boss disposition due to transportation of the player to the next room.
        If the new boss disposition becomes equal to "far away",
        updates Boss skeleton position to draw it properly.
        """
        self.room_pos = array(new_room_pos)
        if any(mob.name in BOSS_PIECES for mob in new_mobs):
            self.new_boss_disposition = BOSS_IN_CURRENT_ROOM
            self.boss_pos = array(new_room_pos)
        elif (self.boss_disposition == BOSS_IN_CURRENT_ROOM or
                  (self.boss_pos is not None and hypot(*(self.room_pos - self.boss_pos)) == 1)):
            self.new_boss_disposition = BOSS_IN_NEIGHBOUR_ROOM
        else:
            self.new_boss_disposition = BOSS_IS_FAR_AWAY

        if self.new_boss_disposition != BOSS_IS_FAR_AWAY:
            self.boss_skeleton.move_to(*(array([SCR_W2, SCR_H2]) + self.boss_offset))

    def set_params_after_transportation(self):
        """Replaces hint widget of the old room with a hint widget of the next room.
        and old boss disposition with the new boss disposition.
        """
        self.boss_disposition = self.new_boss_disposition

        self.hint_widget.replace_with(self.new_hint_widget)

    def prepare_superpower_hint(self):
        """Prepare an extra hint to show, when player got his first superpower. """
        self.hint_texts.append(ROOM_HINTS[self.language][-1])

    def set_next_hint(self):
        """Method is called when player is being transported to the next room.
        Sets new hint text widget, explaining the rules of the game.
        """
        room_pos = tuple(self.room_pos)
        if room_pos in self.hints_history:
            # if a hint was set for current room before, load it from hints history
            self.new_hint_widget.set_text(self.hints_history[room_pos])
        else:
            try:
                text = self.hint_texts.pop(0)
            except IndexError:
                self.new_hint_widget.clear()
            else:
                self.new_hint_widget.set_text(text)
                self.hints_history[room_pos] = text

    def set_player_halo(self, radius):
        self.player_halo.set_size(radius)

    def set_player_trace(self, x, y, dist, alpha):
        self.player_trace.set_coords(x, y, 0.05 * dist, alpha)

    def set_destination_circle(self, pos):
        self.destination_circle.set_pos(*pos)

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

    def draw_player_halo(self, screen, pos1, pos2=None):
        self.player_halo.draw(screen, pos1, pos2)

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

        elif (self.boss_disposition == BOSS_IN_CURRENT_ROOM or
                  (self.boss_disposition == BOSS_IN_NEIGHBOUR_ROOM and
                       self.boss_visible_from_neighbour_room(array([dx, dy])))):
            self.boss_skeleton.draw(surface, dx, dy)


__all__ = ["BackgroundEnvironment"]

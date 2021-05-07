import pygame as pg
from math import hypot
from numpy import array

from objects.body import Body
from entities.background_environment import *
from data.paths import *
from data.config import *
from data.colors import *
from gui.text import Text
from data.gui_texts import ROOM_TEXTS
from data.mobs import BOSS_SKELETON_BODY
from mob_generator import BOSS_PIECES
from utils import H, HF, WF, scaled_body


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
        self.hint_widget = Text(WF(640), HF(176), FONT_1, H(75), WHITE, centralised=True)
        self.new_hint_widget = Text(WF(640), HF(176), FONT_1, H(75), WHITE, centralised=True)

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
        self.hint_texts = ROOM_TEXTS[self.language].copy()[:-1]  # hints without superpower hint
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
        self.hint_texts.append(ROOM_TEXTS[self.language][-1])

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

import pygame as pg
from collections import defaultdict

from constants import *
from utils import H
from gui.button import Button
from data.paths import ROOM_AIM, BOSS_AIM


class RoomAim:
    """Object that highlights the current room position on the map. """
    def __init__(self):
        self.base_image = pg.transform.scale(pg.image.load(ROOM_AIM).convert_alpha(), (H(70), H(70)))
        self.surface = None
        self.angle = 0

    def update(self, dt):
        """Updates the rotation angle of the surface. """
        self.angle -= 0.2 * dt
        self.surface = pg.transform.rotate(self.base_image, self.angle)

    def draw(self, screen, x, y):
        w, h = self.surface.get_size()
        screen.blit(self.surface, (x - w // 2, y - h // 2))


class BossAim:
    """Object that highlights the current boss position on the map. """
    def __init__(self):
        self.radius = H(42)
        image = pg.image.load(BOSS_AIM).convert_alpha()
        self.surface = pg.transform.scale(image, (2 * self.radius, 2 * self.radius))
        self.alpha = 255
        self.alpha_vel = 0.4
        self.pos = None

    def update(self, dt):
        """Updates the alpha-value of the surface. """
        self.alpha += self.alpha_vel * dt
        if self.alpha >= 255 or self.alpha <= 60:
            self.alpha_vel *= -1
            self.alpha = 255 if self.alpha >= 255 else 60
        self.surface.set_alpha((int(self.alpha)))

    def draw(self, screen, x, y):
        screen.blit(self.surface, (x - self.radius, y - self.radius))


class Map(Button):
    """ Map class stores, updates and represents in the map_window information
    about all player movements across rooms during the game.
    """
    w = H(992)  # width of map
    h = H(616)  # height of map
    d = H(50)  # distance between rooms on map

    def __init__(self, menu, xo):
        super().__init__(pg.SYSTEM_CURSOR_SIZEALL)

        self.menu = menu

        # surface on which all elements of the map will be drawn
        self.surface = pg.Surface((self.w, self.h))
        self.surface.set_colorkey(BLACK)
        self.rect = pg.Rect(xo + H(136), H(264), self.w, self.h)

        # transparent surface, on which all elements of the map will be drawn during opening/closing animation
        self.transparent_surface = pg.Surface((self.w, self.h), pg.SRCALPHA)

        # position of room the player is currently in
        self.cur_pos = (0, 0)

        # Graph of visited rooms, which is used to draw the map of visited rooms.
        # It stores all visited rooms and neighbours of each visited room.
        self.graph = defaultdict(list)
        self.graph[self.cur_pos] = []

        # the positions of the top-left and bottom-right corner of the rectangle
        # that delimits all rooms in the graph
        self.topleft = self.bottomright = (0, 0)

        self.room_aim = RoomAim()
        self.boss_aim = BossAim()

        self.moving_x = self.moving_y = False  # can map move by x- and y-axis
        self.movement_start_pos = None   # mouse position when map was pressed

        # map offset when map is moving. It changes during mouse motion.
        self.moving_offset = [0, 0]

        # map offset when map is not moving. When the mouse button is released,
        # the map is no longer moving and static_offset becomes equal to moving_offset.
        self.static_offset = [0, 0]

    @property
    def pressed(self):
        self.static_offset = self.moving_offset.copy()
        if self.cursor_on_button:
            self.is_pressed = True
            self.movement_start_pos = pg.mouse.get_pos()
            return True
        else:
            self.is_pressed = False
            return False

    def reset_all_data(self):
        """Method is called when a new game is started.
        Resets all information about the map.
        """
        self.cur_pos = self.topleft = self.bottomright = (0, 0)
        self.graph = defaultdict(list)
        self.graph[self.cur_pos] = []
        self.boss_aim.pos = None
        self.moving_x = self.moving_y = False
        self.reset()

    def reset(self):
        """Method is called when player goes to the map menu or when a new game is started.
        It resets parameters that track movement of the map by the player's mouse.
        """
        self.static_offset = [0, 0]
        self.moving_offset = [0, 0]
        self.is_pressed = False
        self.movement_start_pos = None

    def update_data(self, room_pos, boss_state):
        """Adds information about visited room and boss location to the map. """
        self.add_visited_room(room_pos)
        if boss_state == BOSS_IN_CURRENT_ROOM:
            self.boss_aim.pos = room_pos

    def add_visited_room(self, room_pos: tuple):
        """Adds new room position to the graph and updates map parameters. """
        self.graph[room_pos].append(self.cur_pos)
        self.cur_pos = room_pos
        self.topleft = (
            min(self.topleft[0], room_pos[0]),
            min(self.topleft[1], room_pos[1])
        )
        self.bottomright = (
            max(self.bottomright[0], room_pos[0]),
            max(self.bottomright[1], room_pos[1])
        )
        # check if current map size is big enough to move it by mouse
        map_size_x = (self.bottomright[0] - self.topleft[0]) * self.d
        map_size_y = (self.bottomright[1] - self.topleft[1]) * self.d
        self.moving_x = map_size_x > self.w / 2
        self.moving_y = map_size_y > self.h / 2

    def room_coords(self, room_pos) -> tuple:
        """Returns coordinates of the room by given room pos in graph. """
        x = self.w / 2 + self.moving_offset[0] + (room_pos[0] - self.cur_pos[0]) * self.d
        y = self.h / 2 + self.moving_offset[1] + (room_pos[1] - self.cur_pos[1]) * self.d
        return x, y

    def update_moving_offset(self):
        pos = pg.mouse.get_pos()
        if self.moving_x:
            self.moving_offset[0] = self.static_offset[0] + pos[0] - self.movement_start_pos[0]
        if self.moving_y:
            self.moving_offset[1] = self.static_offset[1] + pos[1] - self.movement_start_pos[1]

        # if the moving offset became too large, correct it
        left_x, top_y = self.room_coords(self.topleft)
        right_x, bottom_y = self.room_coords(self.bottomright)
        current_x, current_y = self.room_coords(self.cur_pos)

        if right_x < self.w / 2:
            self.moving_offset[0] = current_x - right_x
        elif left_x > self.w / 2:
            self.moving_offset[0] = current_x - left_x
        if bottom_y < self.h / 2:
            self.moving_offset[1] = current_y - bottom_y
        elif top_y > self.h / 2:
            self.moving_offset[1] = current_y - top_y

    def update_look(self, dt, animation_state=WAIT, time_elapsed=0):
        self.room_aim.update(dt)
        self.boss_aim.update(dt)

    def update(self, dt, animation_state=WAIT, time_elapsed=0):
        """updates map objects that change over time and the map offset. """
        if self.is_pressed:
            self.update_moving_offset()

        if self.menu.is_opening:
            alpha = round(255 * time_elapsed)
        elif self.menu.is_closing:
            alpha = round(255 - 255 * time_elapsed)
        else:
            alpha = 255
        self.transparent_surface.set_alpha(alpha)

    def draw_line(self, screen, room_pos_1, room_pos_2):
        """Draws a line between two neighbour rooms. """
        coords_1 = self.room_coords(room_pos_1)
        coords_2 = self.room_coords(room_pos_2)
        pg.draw.line(screen, WHITE, coords_1, coords_2, H(2))

    def draw_visited_room(self, screen, room_pos):
        """Draws the visited room on the map. """
        coords = self.room_coords(room_pos)
        pg.draw.circle(screen, WHITE, coords, H(8))
        pg.draw.circle(screen, GREY, coords, H(17), H(2))
        if room_pos == (0, 0):
            pg.draw.circle(screen, GREY, coords, H(26), H(2))

    def draw(self, screen):
        """Draws all map objects: visited rooms, traversed paths between rooms etc. """
        if self.menu.is_opening or self.menu.is_closing:
            surface = self.transparent_surface
        else:
            surface = self.surface

        surface.fill((0, 0, 0, 0))

        for room_pos in self.graph:
            self.draw_visited_room(surface, room_pos)
            for neighbour_pos in self.graph[room_pos]:
                self.draw_line(surface, room_pos, neighbour_pos)

        self.room_aim.draw(surface, *self.room_coords(self.cur_pos))

        if self.boss_aim.pos is not None:
            self.boss_aim.draw(surface, *self.room_coords(self.boss_aim.pos))

        pg.draw.rect(surface, WHITE, self.surface.get_rect(), H(2))
        screen.blit(surface, self.rect)


__all__ = ["Map"]

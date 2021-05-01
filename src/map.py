import pygame as pg
from collections import defaultdict

from data.colors import *
from data.config import K
from data.paths import ROOM_AIM, BOSS_AIM


class RoomAim:
    """Object that highlights the current room position on the map. """
    def __init__(self):
        size = int(round(70 * K)), int(round(70 * K))
        self.base_image = pg.transform.scale(pg.image.load(ROOM_AIM).convert_alpha(), size)
        self.surface = None
        self.angle = 0

    def update(self, dt):
        """Updates the rotation angle of the surface. """
        self.angle -= 0.32 * dt
        self.surface = pg.transform.rotate(self.base_image, self.angle)

    def draw(self, screen, x, y):
        w, h = self.surface.get_size()
        screen.blit(self.surface, (x - w // 2, y - h // 2))


class BossAim:
    """Object that highlights the current boss position on the map. """
    def __init__(self):
        self.radius = int(round(42 * K))
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


class Map:
    """ Map class stores, updates and represents in the map_window information
    about all player movements across rooms during the game.
    """
    def __init__(self):
        self.surface = pg.Surface((int(round(992 * K)), int(round(616 * K))))
        self.surface.set_colorkey(COLOR_KEY)
        # Graph of visited rooms, which is used to draw the map of visited rooms.
        # It stores all visited rooms and neighbours of each visited room.
        self.graph = defaultdict(list)
        self.cur_pos = (0, 0)
        self.graph[self.cur_pos] = []

        # the rectangle within which the map is drawn
        self.rect = pg.Rect(int(round(200 * K)), int(round(264 * K)),
                            int(round(992 * K)), int(round(616 * K)))

        self.room_aim = RoomAim()
        self.boss_aim = BossAim()

        self.distance = int(round(50 * K))  # distance between rooms on map

        # parameters that track the movement of the map by the player's mouse
        self.moving = False
        self.movement_start_pos = None
        self.main_offset = [0, 0]  # stores map offset when player is not moving the map by mouse
        self.offset = [0, 0]  # stores map offset when player is moving the map by mouse

    def reset(self):
        """Method is called when a new game is started.
        Resets all information about the map.
        """
        self.graph = defaultdict(list)
        self.cur_pos = (0, 0)
        self.graph[self.cur_pos] = []
        self.boss_aim.pos = None
        self.reset_offset()

    def reset_offset(self):
        """Method is called when player goes to the map menu or when a new game is started.
        It resets parameters that track movement of the map by the player's mouse.
        """
        self.main_offset = [0, 0]
        self.offset = [0, 0]
        self.moving = False
        self.movement_start_pos = None

    def add_visited_room(self, room_pos: tuple):
        """ Adds new room position to the graph. """
        self.graph[room_pos].append(self.cur_pos)
        self.graph[self.cur_pos].append(room_pos)
        self.cur_pos = room_pos

    def room_coords(self, room_pos) -> tuple:
        """ returns coordinates of the room by given room pos in graph. """
        x = self.rect.w // 2 + self.offset[0] + (room_pos[0] - self.cur_pos[0]) * self.distance
        y = self.rect.h // 2 + self.offset[1] + (room_pos[1] - self.cur_pos[1]) * self.distance
        return x, y

    def handle(self, e_type):
        pos = pg.mouse.get_pos()
        if e_type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
            self.moving = True
            self.movement_start_pos = pos
            self.main_offset = self.offset.copy()
        else:
            self.moving = False

    def update(self, dt):
        """updates map objects that change over time and the map offset. """
        self.room_aim.update(dt)
        self.boss_aim.update(dt)
        pos = pg.mouse.get_pos()
        if self.moving and self.rect.collidepoint(pos):
            scale = 1.8  # It is used to move the map slower than the movement of the player's mouse
            self.offset[0] = self.main_offset[0] + (pos[0] - self.movement_start_pos[0]) // scale
            self.offset[1] = self.main_offset[1] + (pos[1] - self.movement_start_pos[1]) // scale
        else:
            self.moving = False

    def draw_line(self, screen, room_pos_1, room_pos_2):
        """Draws a line between two neighbour rooms. """
        coords_1 = self.room_coords(room_pos_1)
        coords_2 = self.room_coords(room_pos_2)
        pg.draw.line(screen, WHITE, coords_1, coords_2, 2)

    def draw_visited_room(self, screen, room_pos):
        """Draws the visited room on the map. """
        coords = self.room_coords(room_pos)
        pg.draw.circle(screen, WHITE, coords, int(round(8 * K)))
        pg.draw.circle(screen, GREY, coords, int(round(17 * K)), 2)
        if room_pos == (0, 0):
            pg.draw.circle(screen, GREY, coords, int(round(26 * K)), 2)

    def draw(self, screen):
        """Draws all map objects: visited rooms, traversed paths between rooms etc. """
        self.surface.fill(BLACK)

        for room_pos in self.graph:
            self.draw_visited_room(self.surface, room_pos)
            for neighbour_pos in self.graph[room_pos]:
                self.draw_line(self.surface, room_pos, neighbour_pos)

        self.room_aim.draw(self.surface, *self.room_coords(self.cur_pos))

        if self.boss_aim.pos is not None:
            self.boss_aim.draw(self.surface, *self.room_coords(self.boss_aim.pos))

        self.surface.set_colorkey(BLACK)
        screen.blit(self.surface, self.rect)
        pg.draw.rect(screen, WHITE, self.rect, 2)

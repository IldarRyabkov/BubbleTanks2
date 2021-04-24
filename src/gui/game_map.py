import pygame
from math import pi, cos, sin

from data.colors import WHITE, GREY, RED


class Aim:
    def __init__(self):
        self.alpha = 0
        self.beta = 0.08 * pi
        self.r1 = 14
        self.r2 = 26

    def update(self, dt):
        self.alpha += dt/2000 * 2*pi
        while self.alpha >= 2*pi:
            self.alpha -= 2*pi

    def draw(self, screen, rect):
        x0, y0 = rect.centerx, rect.centery

        x1 = self.r1 * cos(self.alpha)
        y1 = self.r1 * sin(self.alpha)
        x2 = self.r2 * cos(self.alpha + self.beta)
        y2 = self.r2 * sin(self.alpha + self.beta)
        x3 = self.r2 * cos(self.alpha - self.beta)
        y3 = self.r2 * sin(self.alpha - self.beta)

        x4 = self.r1 * cos(self.alpha + pi/2)
        y4 = self.r1 * sin(self.alpha + pi/2)
        x5 = self.r2 * cos(self.alpha + pi/2 + self.beta)
        y5 = self.r2 * sin(self.alpha + pi/2 + self.beta)
        x6 = self.r2 * cos(self.alpha + pi/2 - self.beta)
        y6 = self.r2 * sin(self.alpha + pi/2 - self.beta)

        pygame.draw.polygon(screen, GREY, ((x0+x1, y0+y1), (x0+x2, y0+y2), (x0+x3, y0+y3)))
        pygame.draw.polygon(screen, GREY, ((x0-x1, y0-y1), (x0-x2, y0-y2), (x0-x3, y0-y3)))
        pygame.draw.polygon(screen, GREY, ((x0+x4, y0+y4), (x0+x5, y0+y5), (x0+x6, y0+y6)))
        pygame.draw.polygon(screen, GREY, ((x0-x4, y0-y4), (x0-x5, y0-y5), (x0-x6, y0-y6)))


class BossStar:
    def __init__(self):
        self.pos = None
        self.radius = 17

        self.alpha = 255
        self.max_alpha = 255
        self.min_alpha = 100
        self.alpha_switch = 1

        self.surface = self.create_surface()

    def get_star_vertices(self):
        alpha = 90
        beta = 126
        vertices = []
        for i in range(10):
            if i % 2 == 0:
                x = int(self.radius + self.radius * cos(alpha * pi/180))
                y = int(self.radius - self.radius * sin(alpha * pi/180))
                alpha += 72
            else:
                x = int(self.radius + 0.62 * self.radius * cos(beta * pi/180))
                y = int(self.radius - 0.62 * self.radius * sin(beta * pi/180))
                beta += 72
            vertices.append((x, y))
        vertices.append(vertices[0])

        return vertices

    def create_surface(self):
        surface = pygame.Surface((2*self.radius, 2*self.radius))
        surface.fill(RED)
        pygame.draw.polygon(surface, WHITE, self.get_star_vertices())
        pygame.draw.circle(surface, RED, (self.radius, self.radius), int(0.6 * self.radius))
        surface.set_colorkey(RED)
        return surface

    def reset(self):
        self.pos = None

    def set_pos(self, pos):
        self.pos = pos

    def update(self, dt):
        if self.alpha_switch == 1:
            self.alpha = min(int(self.alpha + 0.32 * dt), self.max_alpha)
        else:
            self.alpha = max(int(self.alpha - 0.32 * dt), self.min_alpha)

        if self.alpha == self.min_alpha:
            self.alpha_switch = 1
        elif self.alpha == self.max_alpha:
            self.alpha_switch = -1

        self.surface.set_alpha(self.alpha)

    def draw(self, screen, dx, dy, rect):
        x = rect.centerx + (self.pos[0] - dx) * 37
        y = rect.centery + (self.pos[1] - dy) * 37
        if rect.collidepoint(x, y):
            screen.blit(self.surface, (x - self.radius, y - self.radius))


class Point:
    def __init__(self, coords, is_first_point=False):
        self.coords = coords
        self.is_first_point = is_first_point
        self.scale = 37

    def draw(self, screen, dx, dy, rect):
        x = rect.centerx + (self.coords[0] - dx) * self.scale
        y = rect.centery + (self.coords[1] - dy) * self.scale

        if rect.collidepoint(x, y):
            pygame.draw.circle(screen, WHITE, (x, y), 6)
            pygame.draw.circle(screen, GREY, (x, y), 13, 1)

            if self.is_first_point:
                pygame.draw.circle(screen, GREY, (x, y), 19, 1)


class GameMap:
    def __init__(self):
        self.points = [Point((0, 0), True)]
        self.current_point = (0, 0)
        self.rect = pygame.Rect(200, 264, 992, 616)

        self.lines = []

        self.aim = Aim()
        self.boss_star = BossStar()

        self.dx = 0
        self.dy = 0

    def reset(self):
        self.points = [Point((0, 0), True)]
        self.current_point = (0, 0)
        self.boss_star.reset()
        self.lines = []
        self.dx = 0
        self.dy = 0

    def new_line(self, coords):
        for line in self.lines:
            if line in [(self.current_point, coords),
                        (coords, self.current_point)]:
                return False
        return True

    def new_point(self, coords):
        for point in self.points:
            if point.coords == coords:
                return False
        return True

    def set_boss_location(self):
        self.boss_star.set_pos(self.current_point)

    def update_data(self, room_coords):
        if self.new_line(room_coords):
            self.lines.append((self.current_point, room_coords))

        if self.new_point(room_coords):
            self.points.append(Point(room_coords))

        self.current_point = room_coords
        self.dx = room_coords[0]
        self.dy = room_coords[1]

    def update(self, dt):
        self.aim.update(dt)
        self.boss_star.update(dt)

    def line_on_screen(self, pos1, pos2):
        if self.rect.collidepoint(pos1) and self.rect.collidepoint(pos2):
            return True
        return False

    def draw_lines(self, screen):
        for line in self.lines:
            x1 = self.rect.centerx + (line[0][0] - self.dx) * 37
            y1 = self.rect.centery + (line[0][1] - self.dy) * 37
            x2 = self.rect.centerx + (line[1][0] - self.dx) * 37
            y2 = self.rect.centery + (line[1][1] - self.dy) * 37

            if self.line_on_screen((x1, y1), (x2, y2)):
                pygame.draw.line(screen, WHITE, (x1, y1), (x2, y2))

    def draw_points(self, screen):
        for point in self.points:
            point.draw(screen, self.dx, self.dy, self.rect)

    def draw_aim(self, screen):
        self.aim.draw(screen, self.rect)

    def draw_boss_position(self, screen):
        if self.boss_star.pos is not None:
            self.boss_star.draw(screen, self.dx, self.dy, self.rect)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 1)

        self.draw_lines(screen)
        self.draw_points(screen)
        self.draw_aim(screen)
        if self.current_point != self.boss_star.pos:
            self.draw_boss_position(screen)
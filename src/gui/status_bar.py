import pygame as pg

from data.colors import WHITE, STATUS_BAR_BG


class StatusBar:
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 max_value: int):

        self.width = width
        self.value = 0
        self.max_value = max_value
        self.color = STATUS_BAR_BG
        self.edge_rect = pg.Rect(x, y, width, height)
        self.value_rect = pg.Rect(x, y, 0, height)

    def update_value_rect(self):
        if self.max_value == 0:
            self.value_rect.width = 0
        else:
            self.value_rect.width = self.value/self.max_value * self.width

    def set_value(self, value: int):
        self.value = value if value != self.max_value else 0
        self.update_value_rect()

    def set_max_value(self, max_value: int):
        self.max_value = max_value

    def move_to(self, x: int, y:int):
        self.edge_rect.x = x
        self.edge_rect.y = y
        self.value_rect.x = x
        self.value_rect.y = y

    def draw(self, surface):
        pg.draw.rect(surface, WHITE, self.edge_rect, 1)
        pg.draw.rect(surface, self.color, self.value_rect)
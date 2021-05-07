import pygame as pg

ONE_SECOND = 1000

class FPSManager:
    dt_history = []
    time = 0

    def get_fps(self):
        if not self.dt_history:
            return 0
        return round(sum([1000/dt for dt in self.dt_history]) / len(self.dt_history))

    def update(self, dt):
        self.time += dt
        if dt != 0:
            self.dt_history.append(dt)
        while sum(self.dt_history) > ONE_SECOND:
            self.dt_history.pop(0)
        if self.time > ONE_SECOND:
            self.time -= ONE_SECOND
            fps = self.get_fps()
            #pg.display.set_caption('FPS: %s' % fps)
            print(fps)



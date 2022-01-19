ONE_SECOND = 1000
HALF_SECOND = 500
PRINT_FPS_EVERY = 10000


class FPSManager:
    dt_history = []
    time = 0

    def get_fps(self):
        if not self.dt_history:
            return 0
        return round(sum([ONE_SECOND / dt for dt in self.dt_history]) / len(self.dt_history))

    def update(self, dt):
        self.time += dt
        if dt != 0:
            self.dt_history.append(dt)

        while sum(self.dt_history) > HALF_SECOND:
            self.dt_history.pop(0)

        if self.time > PRINT_FPS_EVERY:
            self.time -= PRINT_FPS_EVERY
            fps = self.get_fps()
            print(fps)


__all__ = ["FPSManager"]

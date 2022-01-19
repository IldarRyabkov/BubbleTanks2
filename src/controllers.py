"""
This is an attempt to add Xbox controller support.
It works by capturing the pygame.joystick events and translating them to keyboard/mouse commands.
Some slight modifications were make to player.py to accomodate switching between controller/mouse.

"""
import pygame as pg

pg.joystick.init()
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]


def RegisterGame(g):
    global game
    game = g


mouseX = 0
mouseY = 0

DEAD_ZONE = 0.7


def ConvertJoyEventToGameEvent(event):
    global mouseX, mouseY

    if event.type in [
        pg.JOYAXISMOTION,
    ]:
        for controlName, d in controller_config.items():
            if 'axis' in d and d['axis'] == event.axis:
                if d['min'] < event.value < d['max']:
                    if 'mouse' in controlName:
                        if 'left' in controlName or 'right' in controlName:
                            mouseX = event.value
                        elif 'up' in controlName or 'down' in controlName:
                            mouseY = event.value

                        v = pg.Vector2((mouseX, mouseY))
                        game.player.controllerVector = v
                        game.player.use_controller = True


                    else:
                        ret = FakeEvent()
                        ret.type = pg.KEYDOWN if abs(event.value) > DEAD_ZONE else pg.KEYUP
                        ret.key = game.controls[controlName]
                        return ret
        else:
            return event

    elif event.type in [
        pg.JOYBUTTONUP,
        pg.JOYBUTTONDOWN,
    ]:
        for controlName, d in controller_config.items():
            if 'button' in d:
                if controlName == 'click' and d['button'] == event.button:
                    ret = FakeEvent()
                    ret.button = 1
                    ret.type = {pg.JOYBUTTONUP: pg.MOUSEBUTTONUP, pg.JOYBUTTONDOWN: pg.MOUSEBUTTONDOWN}[event.type]
                    return ret

                elif 'button' in d and event.button == d['button']:
                    ret = FakeEvent()
                    ret.type = {pg.JOYBUTTONUP: pg.KEYUP, pg.JOYBUTTONDOWN: pg.KEYDOWN}[event.type]
                    ret.key = game.controls[controlName]

                    return ret

    else:
        return event


class FakeEvent:
    def __str__(self):
        return f'<FakeEvent: {self.__dict__}>'


# todo: make this config export/import able so you can easliy configure a different controller
controller_config = {
    'up': {
        'axis': 1,
        'min': -1.0,
        'max': 0.0
    },
    'down': {
        'axis': 1,
        'min': 0,
        'max': 1.0,
    },
    'left': {
        'axis': 0,
        'min': -1.0,
        'max': 0.0,
    },
    'right': {
        'axis': 0,
        'min': 0.0,
        'max': 1.0,
    },
    ##################
    'mouse_up': {
        'axis': 3,
        'min': -1.0,
        'max': 0.0
    },
    'mouse_down': {
        'axis': 3,
        'min': 0,
        'max': 1.0,
    },
    'mouse_left': {
        'axis': 2,
        'min': -1.0,
        'max': 0.0,
    },
    'mouse_right': {
        'axis': 2,
        'min': 0.0,
        'max': 1.0,
    },
    ##################
    'pause': {
        'button': 7,
    },
    'superpower': {
        'axis': 5,
        'min': -1.0,
        'max': 1.0,
    },
    'click': {
        'button': 5,
    }
}

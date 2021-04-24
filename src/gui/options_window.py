import pygame as pg

from data.colors import WHITE
from gui.long_button import LongButton
import data.languages.english as eng
import data.languages.russian as rus


def create_buttons(texts):
    buttons = list()
    buttons.append(LongButton(208, 336, True, texts[0]))
    buttons.append(LongButton(560, 336, False, texts[1]))
    buttons.append(LongButton(208, 512, True, texts[0]))
    buttons.append(LongButton(560, 512, False, texts[1]))
    buttons.append(LongButton(944, 832, False, texts[2]))
    return buttons


class OptionsWindow:
    def __init__(self):
        self.caption = None
        self.label_music = None
        self.label_sound = None
        self.buttons = None
        self.set_language("English")

    def set_language(self, language):
        if language == 'English':
            self.set_labels(eng.OPTIONSWINDOW_CAPTION,
                            eng.OPTIONSWINDOW_LABEL_MUSIC,
                            eng.OPTIONSWINDOW_LABEL_SOUND)
            self.buttons = create_buttons(eng.OPTIONSWINDOW_BUTTONS_TEXTS)
        else:
            self.set_labels(rus.OPTIONSWINDOW_CAPTION,
                            rus.OPTIONSWINDOW_LABEL_MUSIC,
                            rus.OPTIONSWINDOW_LABEL_SOUND)
            self.buttons = create_buttons(rus.OPTIONSWINDOW_BUTTONS_TEXTS)

    def set_labels(self, caption, label_1, label_2):
        pg.font.init()
        font = pg.font.SysFont('Calibri', 56, True)
        self.caption = font.render(caption, True, WHITE)
        self.label_music = font.render(label_1, True, WHITE)
        self.label_sound = font.render(label_2, True, WHITE)

    def handle_mouse_click(self, pause_menu, pos, sound_player):
        if self.buttons[0].can_be_clicked(pos) or self.buttons[1].can_be_clicked(pos):
            self.buttons[0].clicked ^= 1
            self.buttons[1].clicked ^= 1

        if self.buttons[2].can_be_clicked(pos) or self.buttons[3].can_be_clicked(pos):
            self.buttons[2].clicked ^= 1
            self.buttons[3].clicked ^= 1

        elif self.buttons[4].cursor_on_button(pos):
            pause_menu.running = False
            pause_menu.quit_game = False

        sound_player.update_data(self.buttons[0].clicked,
                                 self.buttons[2].clicked)

    def update(self, *args, **kwargs):
        pos = pg.mouse.get_pos()
        for button in self.buttons:
            button.update_color(pos)

    def draw(self, screen):
        screen.blit(self.caption, (560, 176))
        screen.blit(self.label_music, (216, 264))
        screen.blit(self.label_sound, (216, 440))

        for button in self.buttons:
            button.draw(screen)
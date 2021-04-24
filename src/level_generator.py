import numpy as np
from random import randint, choice
from collections import defaultdict

import data.languages.english as eng
import data.languages.russian as rus

PLAYER_EXTRA_HEALTH = {0: 0, 1: 75, 2: 200, 3: 400, 4: 800, 5: 1300}

MOBS_DICT = {'BossSkeleton': 0,
             'BossLeg': 0,
             'Infusoria': 0,
             'Cell': 0,
             'Ameba': 0,
             'Baby': 0,
             'Turtle': 0,
             'Turtle_dmg': 0,
             'Terrorist': 0,
             'BenLaden': 0,
             'Ant': 0,
             'Scarab': 0,
             'Bug': 0,
             'Gull': 0,
             'Cockroach': 0,
             'GullMother': 0,
             'BugMother': 0,
             'ScarabMother': 0,
             'BomberShooter': 0,
             'Beetle': 0,
             'Spreader': 0,
             'BigEgg': 0,
             'Spider': 0,
             'MachineGunner': 0,
             'Turret': 0}


class DataMatrix:
    def __init__(self):
        self.size = 2001
        self.size2 = self.size // 2
        self.matrix = self.create_matrix()

        self.pos = np.array([self.size2, self.size2])
        self.visited_rooms = [self.pos.copy()]

        self.offset = {'UP':   np.array((0, -1)),
                       'DOWN':  np.array((0, 1)),
                       'LEFT': np.array((-1, 0)),
                       'RIGHT': np.array((1, 0))}

    def create_matrix(self):
        matrix = [[None] * self.size for _ in range(self.size)]
        matrix[self.size2][self.size2] = [{}, True]
        return matrix

    def reset(self):
        for room in self.visited_rooms:
            self.matrix[room[0]][room[1]] = None

        self.pos = np.array([self.size2, self.size2])
        self.matrix[self.size2][self.size2] = [{}, True]
        self.visited_rooms = [self.pos.copy()]

    def new_room(self):
        return self.matrix[self.pos[0]][self.pos[1]] is None

    def save_mobs(self, mobs_data):
        self.matrix[self.pos[0]][self.pos[1]][0] = mobs_data

    def get_mobs(self):
        """
        :return: dictionary of mobs in current room
        """
        return self.matrix[self.pos[0]][self.pos[1]][0]

    def get_room_pos(self):
        return [self.pos[0] - self.size2, self.pos[1] - self.size2]

    def update_pos(self, direction):
        self.pos += self.offset[direction]

    def update_visited_rooms(self, new_mobs):
        self.matrix[self.pos[0]][self.pos[1]] = [new_mobs, True]
        self.visited_rooms.append(self.pos.copy())


class RoomTextGenerator:
    room_texts = None
    player_got_first_superpower = False
    superpower_text_was_shown = False

    def __init__(self):
        self.set_language("English")

    def set_language(self, language):
        if language == 'English':
            self.room_texts = eng.ROOM_TEXTS
        else:
            self.room_texts = rus.ROOM_TEXTS

    def reset(self):
        self.player_got_first_superpower = False
        self.superpower_text_was_shown = False

    def text(self, n):
        if n in range(1, 6):
            return self.room_texts[n - 1]
        if self.player_got_first_superpower:
            self.player_got_first_superpower = False
            self.superpower_text_was_shown = True
            return self.room_texts[5]
        return ''

    def update(self, player_level):
        if player_level == 2 and not self.superpower_text_was_shown:
            self.player_got_first_superpower = True


class LevelGenerator:
    def __init__(self):
        self.data_matrix = DataMatrix()
        self.text_generator = RoomTextGenerator()
        self.num_of_visited_rooms = 1
        self.boss_generated = False

    def set_language(self, language):
        self.text_generator.set_language(language)

    def reset(self):
        self.data_matrix.reset()
        self.text_generator.reset()
        self.num_of_visited_rooms = 1
        self.boss_generated = False

    def generate_mobs(self, player, pause_menu):
        mobs = defaultdict(int)

        if player.delta_health <= -75:
            mobs["Infusoria"] = int(-player.delta_health * 0.7 / 6)
            return mobs

        if player.defeated:
            for _ in range(randint(3, 6)):
                mobs[choice(['Infusoria', 'Baby', 'Cell', 'Ameba'])] += 1
            return mobs

        if (not self.boss_generated and
                player.health + PLAYER_EXTRA_HEALTH[player.state[0]]>= 1420):
            mobs['BossLeg'] = 1
            mobs['BossHandLeft'] = 1
            mobs['BossHandRight'] = 1
            mobs['BossHead'] = 1
            self.boss_generated = True
            pause_menu.set_boss_location()
            return mobs

        room_pos = self.data_matrix.get_room_pos()
        room_distance = max(abs(room_pos[0]), abs(room_pos[1]))

        if room_distance == 1:
            n_peaceful_mobs = randint(2, 4)

        elif room_distance == 2:
            n_peaceful_mobs = randint(3, 6)

        elif room_distance == 3:
            n_peaceful_mobs = randint(1, 3)
            mobs['Turtle'] = randint(1, 3)

        elif room_distance == 4:
            n_peaceful_mobs = randint(1, 3)
            mobs['Turtle_dmg'] = randint(1, 2)

            group_1 = randint(1, 4)
            if group_1 == 1:
                mobs['Terrorist'] = 1
            elif group_1 == 2:
                mobs['Gull'] = randint(1, 3)
            elif group_1 == 3:
                mobs['Bug'] = randint(1, 3)
            else:
                mobs['Scarab'] = randint(1, 3)

        elif room_distance == 5:
            n_peaceful_mobs = randint(0, 3)
            mobs['Turtle'] = randint(1, 2)
            mobs['Turtle_dmg'] = randint(1, 2)

            group_1 = randint(1, 3)
            if group_1 == 1:
                mobs['Gull'] = randint(1, 3)
            elif group_1 == 2:
                mobs['Bug'] = randint(1, 3)
            else:
                mobs['Scarab'] = randint(1, 3)

        elif room_distance <= 6:
            n_peaceful_mobs = randint(1, 2)

            group_1 = randint(1, 4)
            if group_1 == 1:
                mobs['Ant'] = 14
            else:
                if group_1 == 2:
                    mobs['Bug'] = randint(1, 2)
                elif group_1 == 3:
                    mobs['Gull'] = randint(1, 2)
                elif group_1 == 4:
                    mobs['Scarab'] = randint(1, 2)

                group_2 = randint(1, 4)
                if group_2 == 1:
                    mobs['GullMother'] = 1
                elif group_2 == 2:
                    mobs['Cockroach'] = randint(1, 2)
                elif group_2 == 3:
                    mobs['BomberShooter'] = 1
                elif group_2 == 4:
                    mobs['Turtle'] = randint(1, 2)
                    mobs['Turtle_dmg'] = randint(1, 2)

        elif room_distance == 7:
            n_peaceful_mobs = randint(1, 2)

            group_1 = randint(1, 3)
            if group_1 == 1:
                mobs['Spider'] = randint(1, 2)
                mobs['Spreader'] = randint(1, 2)
            elif group_1 == 2:
                mobs['BigEgg'] = randint(3, 4)
            elif group_1 == 3:
                mobs['Beetle'] = randint(1, 2)

                group_2 = randint(1, 4)
                if group_2 == 1:
                    mobs['Cockroach'] = randint(2, 3)
                elif group_2 == 2:
                    mobs['Bug'] = randint(2, 3)
                elif group_2 == 3:
                    mobs['Gull'] = randint(2, 3)
                elif group_2 == 4:
                    mobs['Scarab'] = randint(2, 3)

        elif room_distance <= 8:
            n_peaceful_mobs = randint(1, 3)

            group_1 = randint(1, 1)
            if group_1 == 1:
                mobs['Beetle'] = randint(2, 3)
                mobs['Turtle'] = randint(1, 2)

            group_2 = randint(1, 4)
            if group_2 == 1:
                mobs['Cockroach'] = randint(2, 3)
            elif group_2 == 2:
                mobs['Bug'] = randint(2, 3)
            elif group_2 == 3:
                mobs['Gull'] = randint(2, 3)
            elif group_2 == 4:
                mobs['Scarab'] = randint(2, 3)

        else:
            n_peaceful_mobs = randint(1, 4)

            group_1 = randint(1, 2)
            if group_1 == 1:
                mobs['Turret'] = 2

                group_2 = randint(1, 3)
                if group_2 == 1:
                    mobs['Cockroach'] = randint(3, 5)
                elif group_2 == 2:
                    mobs['Bug'] = randint(3, 5)
                elif group_2 == 3:
                    mobs['Gull'] = randint(3, 5)
            elif group_1 == 2:
                mobs['MachineGunner'] = randint(1, 2)
                mobs['Turtle'] = randint(0, 2)

                group_2 = randint(1, 4)
                if group_2 == 1:
                    mobs['Cockroach'] = randint(1, 2)
                elif group_2 == 2:
                    mobs['Bug'] = randint(1, 2)
                elif group_2 == 3:
                    mobs['Gull'] = randint(1, 2)
                elif group_2 == 4:
                    mobs['Beetle'] = randint(1, 2)

        mobs['Baby'] = randint(0, n_peaceful_mobs // 2)
        mobs['Cell'] = randint(0, (n_peaceful_mobs - mobs['Baby']) // 2)
        mobs['Ameba'] = randint(0, (n_peaceful_mobs - mobs['Baby'] - mobs['Cell']))
        mobs['Infusoria'] = n_peaceful_mobs - mobs['Baby'] - mobs['Cell'] - mobs['Ameba']

        return mobs

    def get_room_text(self):
        return self.text_generator.text(self.num_of_visited_rooms)

    def set_room(self, room):
        room.set_new_mobs(self.data_matrix.get_mobs())
        room.set_text(self.get_room_text())

    def update(self, mobs, direction, player, pause_menu):
        self.text_generator.update(player.state[0])
        self.data_matrix.save_mobs(mobs)
        self.data_matrix.update_pos(direction)
        self.num_of_visited_rooms += 1
        if player.defeated:
            new_mobs = self.generate_mobs(player, pause_menu)
            if self.data_matrix.new_room():
                self.data_matrix.update_visited_rooms(new_mobs)
            else:
                self.data_matrix.save_mobs(new_mobs)
        else:
            if self.data_matrix.new_room():
                new_mobs = self.generate_mobs(player, pause_menu)
                self.data_matrix.update_visited_rooms(new_mobs)
        pause_menu.update_game_map(self.data_matrix.get_room_pos())


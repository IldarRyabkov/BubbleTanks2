import random
import itertools
from collections import defaultdict
from math import sqrt

from objects.mobs import get_mob


PEACEFUL_MOBS = ['Infusoria', 'Cell', 'Ameba', 'Baby']
WEAK_SLOW_MOBS = ["Turtle", "Turtle_dmg", "Terrorist"]
WEAK_FAST_MOBS = ["Scarab", "Bug", "Gull", "Ant", "Cockroach"]
STRONG_MOBS = ["Spider", "Spreader", "Beetle", "BomberShooter", "BenLaden"]
EPIC_MOBS = ["MachineGunner", "Turret"]
BOSS_PIECES = ['BossLeg', 'BossHandLeft', 'BossHandRight', 'BossHead']


def add_peaceful_mobs(mobs, n_min, n_max):
    for _ in range(random.randint(n_min, n_max)):
        mobs[random.choice(PEACEFUL_MOBS)] += 1


def generate_compensation(delta_health):
    compensation = 0
    mobs = defaultdict(int)
    while compensation < delta_health * 0.7:
        mobs["Infusoria"] += 1
        compensation += 6
    return mobs


def generate_peaceful_mobs():
    mobs = defaultdict(int)
    add_peaceful_mobs(mobs, 2, 3)
    return mobs


def generate_boss():
    mobs = defaultdict(int)
    for boss_piece in BOSS_PIECES:
        mobs[boss_piece] += 1
    return mobs


def generate_level_3():
    mobs = defaultdict(int)
    mobs["Turtle"] = random.randint(1, 2)
    add_peaceful_mobs(mobs, 0, 1)
    return mobs


def generate_level_4():
    mobs = defaultdict(int)
    group = random.choice(list(itertools.combinations(WEAK_SLOW_MOBS, 2)))
    for name in group:
        mobs[name] += 1
    add_peaceful_mobs(mobs, 0, 1)
    return mobs


def generate_level_5():
    mobs = generate_level_4()
    for _ in range(random.randint(1, 3)):
        mobs[random.choice(WEAK_FAST_MOBS)] += 1
    return mobs


def generate_level_6():
    mobs = defaultdict(int)
    group = random.choice(["Ants", "Mother", "Other"])
    if group == "Ants":
        mobs["Ant"] += 14
    elif group == "Mother":
        mobs["Mother"] += 1
        for _ in range(random.randint(2, 3)):
            mobs[random.choice(WEAK_FAST_MOBS)] += 1
    else:
        for _ in range(4):
            mobs[random.choice(["Turtle", "Turtle_dmg",
                                "Beetle", "BomberShooter"])] += 1
        for _ in range(2):
            mobs[random.choice(WEAK_FAST_MOBS)] += 1
    return mobs


def generate_level_7():
    mobs = defaultdict(int)
    group = random.choice(["Big Eggs", "Other", "Other", "Other"])
    if group == "Big Eggs":
        mobs["BigEgg"] = random.randint(4, 5)
    else:
        for _ in range(3):
            mobs[random.choice(STRONG_MOBS)] += 1
        for _ in  range(random.randint(2, 3)):
            mobs[random.choice(WEAK_FAST_MOBS)] += 1
    return mobs


def generate_level_8():
    mobs = defaultdict(int)
    group = random.choice(["Epic mobs", "Mothers", "Other"])
    if group == "Epic mobs":
        mobs[random.choice(EPIC_MOBS)] += random.randint(1, 2)
        for _ in range(2):
            mobs[random.choice(WEAK_SLOW_MOBS)] += 2
            mobs[random.choice(WEAK_FAST_MOBS)] += 2
            mobs[random.choice(STRONG_MOBS)] += 1
    elif group == "Mothers":
        for _ in range(2):
            mobs["Mother"] += 1
        for _ in range(random.randint(4, 6)):
            mobs[random.choice(WEAK_FAST_MOBS)] += 1
    else:
        mobs = generate_level_7()
        for _ in range(2):
            mobs[random.choice(WEAK_SLOW_MOBS)] += 1
    return mobs


class MobGenerator:
    """Saves mobs in all visited rooms and also generates mobs for the next room. """
    def __init__(self):
        self.mobs = {(0, 0): defaultdict(int)}  # stores mobs in all visited rooms
        self.cur_room = (0, 0)  # current room the player is in
        self.boss_generated = False  # flag to make sure boss was generated only once

    def reset(self):
        self.__init__()

    def save_mobs(self, mobs: list):
        mobs_dict = defaultdict(int)
        for mob in mobs:
            mobs_dict[mob.name] += 1
        self.mobs[self.cur_room] = mobs_dict

    def load_mobs(self) -> list:
        """Returns list of mobs in current room. """
        mobs = []
        for name, n in self.mobs[self.cur_room].items():
            mobs.extend([get_mob(name) for _ in range(n)])
        return mobs

    def generate_level(self, player) -> defaultdict(int):
        if player.delta_health <= -75:
            return generate_compensation(-player.delta_health)

        if player.defeated:
            return generate_peaceful_mobs()

        if player.level == 5 and player.health >= 150 and not self.boss_generated:
            self.boss_generated = True
            return generate_boss()

        # the difficulty of level depends on the player's distance from the starting room.
        distance = int(round(sqrt(self.cur_room[0] ** 2 + self.cur_room[1] ** 2)))
        if distance  <= 2:
            return generate_peaceful_mobs()
        if distance == 3:
            return generate_level_3()
        if distance == 4:
            return generate_level_4()
        if distance == 5:
            return generate_level_5()
        elif distance == 6:
            return generate_level_6()
        elif distance == 7:
            return generate_level_7()
        else:
            return generate_level_8()

    def generate_mobs(self, direction, player):
        """Updates current room position according to direction and
        if this is a new room or player was defeated, generates mobs for it.
        """
        self.cur_room = (self.cur_room[0] + direction[0], self.cur_room[1] + direction[1])
        if self.cur_room not in self.mobs.keys() or player.defeated:
            new_mobs = self.generate_level(player)
            self.mobs[self.cur_room] = new_mobs


__all__ = ["MobGenerator"]

from random import randint, uniform
from collections import defaultdict
from math import sqrt


def generate_test():
    enemies = defaultdict(int)
    enemies["Ameba"] = 0
    enemies["Infusoria"] = 0
    enemies["Baby"] = 0
    enemies["Cell"] = 0
    enemies["Gull"] = 0
    enemies["Cockroach"] = 0
    enemies["Ant"] = 0
    enemies["Bug"] = 0
    enemies["Scarab"] = 0
    enemies["Turret"] = 0
    enemies["StickyTurtle"] = 0
    enemies["Turtle"] = 0
    enemies["EnemySpawnerLarge"] = 0
    enemies["SmallCarrier"] = 0
    enemies["BomberShooter"] = 0
    enemies["BenLaden"] = 0
    enemies["Mortar"] = 0
    enemies["EnemySpawner"] = 0
    enemies["SeekerSpawner"] = 0
    enemies["Spider"] = 0
    enemies["Beetle"] = 0
    enemies["Spreader"] = 0
    enemies["MachineGunner"] = 0
    enemies["Propeller"] = 0
    enemies["SmallPropeller"] = 0
    enemies["BigBaby"] = 0
    enemies["StingerLarge"] = 0
    enemies["Stinger"] = 0
    enemies["InfusoriaSpawner"] = 0
    enemies["BubbleContainer"] = 0
    enemies["Sucker"] = 0
    enemies["Snail"] = 0
    enemies["FatSpreader"] = 0
    enemies["SmallVampire"] = 0
    enemies["LargeVampire"] = 0
    enemies["BubbleBomber"] = 0
    enemies["LongSpreader"] = 0
    enemies["LargeMachineGunner"] = 0
    enemies["Destroyer"] = 0
    enemies["Twins"] = 0
    enemies["LongMachineGunner"] = 0
    enemies["Predator_1"] = 0
    enemies["Predator_2"] = 0
    enemies["MixedEnemy"] = 0
    enemies["Confusion"] = 0
    return enemies


def generate_boss():
    enemies = defaultdict(int)
    enemies["BossHead"] = 1
    enemies["BossLeg"] = 1
    enemies["BossLeftHand"] = 1
    enemies["BossRightHand"] = 1
    return enemies


def generate_easy(health_change):
    def add(name, n_min, n_max):
        enemies[name] = randint(n_min, n_max)

    enemies = defaultdict(int)
    enemy_set_1 = randint(1, 2)
    enemy_set_2 = randint(1, 2)

    if health_change < 75:
        add("Ameba", 2, 3)
        add("Infusoria", 3, 4)
        if enemy_set_2 == 1:
            add("Baby", 1, 3)
        elif enemy_set_2 == 2:
            add("Cell", 1, 3)

    elif health_change < 200:
        add("Ameba", 2, 3)
        add("Infusoria", 5, 6)
        if enemy_set_2 == 1:
            add("Baby", 2, 3)
        elif enemy_set_2 == 2:
            add("Cell", 2, 3)

    elif health_change < 400:
        add("Ameba", 2, 3)
        add("BigBaby", 2, 2)
        if enemy_set_2 == 1:
            add("Baby", 2, 3)
        elif enemy_set_2 == 2:
            add("Cell", 2, 3)

    elif health_change < 800:
        add("Ameba", 2, 3)
        add("BigBaby", 4, 5)
        add("Infusoria", 2, 3)

    else:
        choice = randint(1, 100)
        if choice <= 50:
            add("Ameba", 2, 3)
            add("BigBaby", 6, 8)
            add("Infusoria", 2, 3)
        else:
            add("BigBaby", 5, 7)
            if enemy_set_1 == 1:
                add("BubbleContainer", 1, 1)
            elif enemy_set_1 == 2:
                add("InfusoriaSpawner", 1, 1)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
    return enemies


def generate_help(world_distance):
    def add(name, n_min, n_max):
        enemies[name] = randint(n_min, n_max)

    enemies = defaultdict(int)
    enemy_set_2 = randint(1, 2)

    if world_distance < 7:
        add("Ameba", 1, 2)
        add("Infusoria", 2, 3)
        if enemy_set_2 == 1:
            add("Baby", 0, 2)
        elif enemy_set_2 == 2:
            add("Cell", 0, 2)

    elif world_distance < 20:
        add("Ameba", 1, 2)
        add("Infusoria", 3, 5)
        if enemy_set_2 == 1:
            add("Baby", 1, 3)
        elif enemy_set_2 == 2:
            add("Cell", 1, 3)

    else:
        choice = randint(1, 60)
        if choice <= 20:
            add("BigBaby", 1, 2)
            add("Infusoria", 2, 4)
            if enemy_set_2 == 1:
                add("Baby", 1, 3)
            elif enemy_set_2 == 2:
                add("Cell", 1, 3)
        elif choice <= 40:
            add("InfusoriaSpawner", 1, 1)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
        elif choice <= 60:
            add("Infusoria", 1, 2)
            add("BubbleContainer", 1, 1)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
    return enemies


def generate_enemies(world_distance):
    def add(name, n_min, n_max):
        enemies[name] = randint(n_min, n_max)

    enemies = defaultdict(int)
    enemy_set_1 = randint(1, 3)
    enemy_set_2 = randint(1, 2)

    if world_distance < 2:
        add("Ameba", 1, 2)
        add("Infusoria", 0, 1)
        if enemy_set_2 == 1:
            add("Cell", 0, 2)
        else:
            add("Baby", 0, 2)

    elif world_distance < 4:
        choice = randint(1, 4)
        if choice == 1:
            add("Ameba", 1, 2)
            add("Infusoria", 1, 2)
        elif choice == 2:
            add("Infusoria", 0, 1)
            add("StickyTurtle", 1, 3)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            else:
                add("Baby", 0, 2)
        else:
            add("Infusoria", 1, 2)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            else:
                add("Baby", 0, 2)

    elif world_distance < 6:
        choice = randint(1, 21)
        if choice <= 6:
            add("Infusoria", 0, 2)
            if enemy_set_1 == 1:
                add("Gull", 1, 4)
            elif enemy_set_1 == 2:
                add("Bug", 1, 4)
            else:
                add("Scarab", 1, 4)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            else:
                add("Baby", 0, 2)
        elif choice <= 12:
            add("Turtle", 1, 2)
            if enemy_set_1 == 1:
                add("Gull", 1, 2)
            elif enemy_set_1 == 2:
                add("Scarab", 1, 2)
            else:
                add("Bug", 2, 3)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            else:
                add("Baby", 0, 2)
        elif choice <= 18:
            add("Turtle", 1, 2)
            add("Mortar", 1, 1)
            add("Infusoria", 0, 2)
        elif choice <= 20:
            add("Infusoria", 0, 1)
            add("StickyTurtle", 1, 2)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            elif enemy_set_2 == 2:
                add("Baby", 0, 2)
        else:
            add("Infusoria", 0, 3)
            add("EnemySpawnerLarge", 1, 1)

    elif world_distance < 8:
        choice = randint(1, 20)
        if choice <= 6:
            add("Infusoria", 1, 2)
            if enemy_set_1 == 1:
                add("Gull", 2, 3)
            elif enemy_set_1 == 2:
                add("Scarab", 2, 3)
            elif enemy_set_1 == 3:
                add("Bug", 3, 4)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            elif enemy_set_2 == 2:
                add("Baby", 0, 2)
        elif choice <= 12:
            add("Turtle", 1, 1)
            if enemy_set_1 == 1:
                add("Gull", 2, 3)
            elif enemy_set_1 == 2:
                add("Scarab", 2, 3)
            elif enemy_set_1 == 3:
                add("Bug", 2, 3)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            elif enemy_set_2 == 2:
                add("Baby", 0, 2)
        elif choice <= 16:
            add("Turtle", 2, 2)
            add("SeekerSpawner", 1, 1)
            add("Infusoria", 0, 2)
        elif choice <= 18:
            add("Infusoria", 0, 1)
            add("StickyTurtle", 1, 3)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            elif enemy_set_2 == 2:
                add("Baby", 0, 2)
        elif choice <= 19:
            add("Confusion", 1, 1)
            if enemy_set_2 == 1:
                add("Cell", 1, 3)
            elif enemy_set_2 == 2:
                add("Baby", 1, 3)
        else:
            add("EnemySpawnerLarge", 1, 1)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            elif enemy_set_2 == 2:
                add("Baby", 0, 2)

    elif world_distance < 10:
        choice = randint(1, 21)
        if choice <= 4:
            add("Ameba", 1, 2)
            if enemy_set_1 == 1:
                add("Gull", 3, 4)
            elif enemy_set_1 == 2:
                add("Scarab", 3, 4)
            elif enemy_set_1 == 3:
                add("Bug", 3, 4)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            elif enemy_set_2 == 2:
                add("Baby", 0, 2)
        elif choice <= 12:
            add("StickyTurtle", 0, 2)
            add("Turtle", 0, 2)
            if enemy_set_1 == 1:
                add("Gull", 2, 3)
            elif enemy_set_1 == 2:
                add("Scarab", 2, 3)
            elif enemy_set_1 == 3:
                add("Bug", 2, 3)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            elif enemy_set_2 == 2:
                add("Baby", 0, 2)
        elif choice <= 16:
            add("Ant", 12, 16)
            add("Ameba", 0, 2)
        elif choice <= 20:
            add("SmallCarrier", 1, 3)
            add("Ameba", 0, 2)
            if enemy_set_1 == 1:
                add("Gull", 1, 2)
            elif enemy_set_1 == 2:
                add("Scarab", 1, 2)
            elif enemy_set_1 == 3:
                add("Bug", 1, 2)
        else:
            add("Infusoria", 0, 1)
            add("StickyTurtle", 1, 3)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            elif enemy_set_2 == 2:
                add("Baby", 0, 2)

    elif world_distance < 12:
        choice = randint(1, 98)
        if choice <= 20:
            add("Cockroach", 2, 3)
            add("Infusoria", 0, 2)
            if enemy_set_1 == 1:
                add("Gull", 1, 2)
            elif enemy_set_1 == 2:
                add("Scarab", 1, 2)
            elif enemy_set_1 == 3:
                add("Bug", 1, 2)
        elif choice <= 45:
            add("Cockroach", 2, 3)
            add("Turtle", 1, 1)
            add("Ameba", 1, 2)
            if enemy_set_1 == 1:
                add("Gull", 0, 1)
            elif enemy_set_1 == 2:
                add("Scarab", 0, 1)
            elif enemy_set_1 == 3:
                add("Bug", 0, 1)
        elif choice <= 55:
            add("Ant", 9, 12)
            add("StickyTurtle", 1, 2)
        elif choice <= 65:
            add("StickyTurtle", 2, 2)
            add("SmallCarrier", 3, 4)
            add("Infusoria", 1, 1)
            if enemy_set_2 == 1:
                add("Cell", 0, 2)
            elif enemy_set_2 == 2:
                add("Baby", 0, 2)
        elif choice <= 75:
            add("EnemySpawner", 1, 1)
            if enemy_set_2 == 1:
                add("Cell", 1, 3)
            elif enemy_set_2 == 2:
                add("Baby", 1, 3)
        elif choice <= 90:
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("BomberShooter", 1, 1)
                add("Cell", 1, 2)
            elif enemy_set_2 == 2:
                add("BenLaden", 1, 1)
                add("Baby", 1, 2)
            if enemy_set_1 == 1:
                add("Gull", 2, 4)
            elif enemy_set_1 == 2:
                add("Scarab", 2, 4)
            elif enemy_set_1 == 3:
                add("Bug", 3, 4)
        elif choice <= 95:
            add("StickyTurtle", 0, 2)
            add("Infusoria", 1, 5)
            add("Ameba", 0, 2)
            add("Propeller", 1, 1)
        else:
            add("Infusoria", 1, 5)
            add("Destroyer", 1, 1)
            add("Ameba", 0, 2)

    elif world_distance < 14:
        choice = randint(1, 115)
        if choice <= 20:
            add("Infusoria", 0, 2)
            add("StickyTurtle", 1, 2)
            add("Cockroach", 3, 4)
        elif choice <= 40:
            add("Cockroach", 2, 3)
            add("Infusoria", 0, 2)
            add("Beetle", 2, 2)
        elif choice <= 60:
            add("Cockroach", 1, 3)
            add("Beetle", 1, 2)
            add("StickyTurtle", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
        elif choice <= 70:
            add("Cockroach", 2, 3)
            add("Beetle", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
        elif choice <= 80:
            add("Cockroach", 2, 3)
            add("Sucker", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
        elif choice <= 90:
            add("Beetle", 0, 2)
            add("EnemySpawner", 1, 1)
            if enemy_set_2 == 1:
                add("Cell", 1, 2)
            elif enemy_set_2 == 2:
                add("Baby", 1, 2)
        elif choice <= 105:
            add("StingerLarge", 2, 4)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
            if enemy_set_2 == 1:
                add("BomberShooter", 0, 1)
            elif enemy_set_2 == 2:
                add("BenLaden", 0, 1)
        elif choice <= 110:
            add("Propeller", 1, 1)
            add("StickyTurtle", 0, 1)
            add("Infusoria", 1, 5)
            add("Ameba", 0, 2)
        else:
            add("Destroyer", 1, 1)
            add("Infusoria", 1, 5)
            add("Ameba", 0, 2)

    elif world_distance < 16:
        choice = randint(1, 145)
        if choice <= 30:
            add("Beetle", 1, 2)
            if enemy_set_2 == 1:
                add("Twins", 2, 2)
                add("Baby", 1, 2)
            elif enemy_set_2 == 2:
                add("MachineGunner", 2, 2)
                add("Cell", 1, 2)
        elif choice <= 50:
            add("Beetle", 1, 2)
            add("StickyTurtle", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
            if enemy_set_2 == 1:
                add("Twins", 1, 2)
            elif enemy_set_2 == 2:
                add("MachineGunner", 1, 2)
        elif choice <= 70:
            add("Ameba", 1, 2)
            add("Spider", 1, 2)
            add("Sucker", 1, 1)
            if enemy_set_1 == 1:
                add("Gull", 1, 1)
            elif enemy_set_1 == 2:
                add("Scarab", 1, 1)
            elif enemy_set_1 == 3:
                add("Bug", 1, 1)
        elif choice <= 90:
            add("Cockroach", 3, 4)
            add("Sucker", 2, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
        elif choice <= 110:
            add("Cockroach", 2, 4)
            add("SeekerSpawner", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
        elif choice <= 130:
            add("SeekerSpawner", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
            if enemy_set_2 == 1:
                add("Twins", 1, 2)
            elif enemy_set_2 == 2:
                add("MachineGunner", 1, 2)
        elif choice <= 140:
            add("EnemySpawner", 1, 1)
            add("Beetle", 1, 2)
            if enemy_set_2 == 1:
                add("Cell", 1, 2)
            elif enemy_set_2 == 2:
                add("Baby", 1, 2)
        else:
            add("StingerLarge", 3, 4)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
            if enemy_set_2 == 1:
                add("BomberShooter", 0, 1)
            elif enemy_set_2 == 2:
                add("BenLaden", 0, 1)

    elif world_distance < 18:
        choice = randint(1, 170)
        if choice <= 20:
            add("Beetle", 1, 2)
            if enemy_set_2 == 1:
                add("Baby", 1, 2)
                add("Twins", 2, 4)
            elif enemy_set_2 == 2:
                add("MachineGunner", 2, 4)
                add("Cell", 1, 2)
        elif choice <= 50:
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Twins", 2, 3)
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("MachineGunner", 1, 3)
                add("Cell", 0, 2)
            if enemy_set_1 == 1:
                add("Predator_1", 1, 2)
            elif enemy_set_1 == 2:
                add("Predator_2", 1, 2)
            elif enemy_set_1 == 3:
                add("LongMachineGunner", 1, 2)
        elif choice <= 60:
            add("Ameba", 1, 2)
            add("Spider", 1, 1)
            add("Sucker", 2, 3)
            if enemy_set_1 == 1:
                add("Gull", 1, 1)
            elif enemy_set_1 == 2:
                add("Scarab", 1, 1)
            elif enemy_set_1 == 3:
                add("Bug", 1, 1)
        elif choice <= 70:
            add("Ameba", 1, 2)
            add("Spider", 2, 3)
            add("Sucker", 1, 1)
            if enemy_set_1 == 1:
                add("Gull", 1, 1)
            elif enemy_set_1 == 2:
                add("Scarab", 1, 1)
            elif enemy_set_1 == 3:
                add("Bug", 1, 1)
        elif choice <= 90:
            add("Cockroach", 3, 4)
            add("Sucker", 2, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 2)
        elif choice <= 110:
            add("Beetle", 2, 3)
            add("SeekerSpawner", 1, 3)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 2)
        elif choice <= 130:
            add("SeekerSpawner", 2, 3)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 2)
            if enemy_set_2 == 1:
                add("Twins", 2, 3)
            elif enemy_set_2 == 2:
                add("MachineGunner", 1, 2)
        elif choice <= 150:
            add("Stinger", 12, 16)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("Cell", 0, 2)
        elif choice <= 160:
            add("Propeller", 1, 1)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
            if enemy_set_2 == 1:
                add("Twins", 2, 3)
            elif enemy_set_2 == 2:
                add("MachineGunner", 1, 2)
        else:
            add("EnemySpawnerLarge", 1, 1)
            add("StickyTurtle", 1, 3)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 1)

    elif world_distance < 20:
        choice = randint(1, 150)
        if choice <= 30:
            add("Spider", 1, 1)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 2)
            if enemy_set_2 == 1:
                add("SmallTurret", 1, 2)
            elif enemy_set_2 == 2:
                add("Spreader", 1, 2)
        elif choice <= 50:
            add("Infusoria", 1, 2)
            add("Ameba", 0, 1)
            add("Turret", 1, 2)
            add("Scarab", 3, 4)
        elif choice <= 70:
            add("Infusoria", 1, 2)
            add("Ameba", 0, 1)
            add("Mite", 1, 2)
            add("Bug", 3, 4)
        elif choice <= 90:
            add("SeekerSpawner", 0, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 2)
            if enemy_set_1 == 1:
                add("Predator_1", 2, 2)
            elif enemy_set_1 == 2:
                add("Predator_2", 2, 2)
            elif enemy_set_1 == 3:
                add("LongMachineGunner", 2, 2)
        elif choice <= 110:
            add("EnemySpawner", 1, 1)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
                add("Twins", 3, 4)
            elif enemy_set_2 == 2:
                add("MachineGunner", 2, 3)
                add("Cell", 0, 2)
        elif choice <= 130:
            add("Stinger", 12, 16)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("Cell", 0, 2)
        elif choice <= 140:
            add("Propeller", 1, 1)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 1)
            if enemy_set_2 == 1:
                add("Twins", 2, 3)
            elif enemy_set_2 == 2:
                add("MachineGunner", 1, 2)
        else:
            add("EnemySpawnerLarge", 1, 1)
            add("StickyTurtle", 1, 3)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 1)

    elif world_distance < 25:
        choice = randint(1, 170)
        if choice <= 20:
            add("BubbleBomber", 2, 4)
            add("StickyTurtle", 1, 2)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 1)
        elif choice <= 40:
            add("FatSpreader", 1, 3)
            add("StickyTurtle", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 0, 2)
        elif choice <= 60:
            add("BubbleBomber", 2, 2)
            add("SmallVampire", 1, 2)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
        elif choice <= 70:
            add("BomberShooter", 1, 1)
            add("Spider", 0, 1)
            add("Ameba", 0, 2)
            if enemy_set_2 == 1:
                add("Twins", 3, 4)
            elif enemy_set_2 == 2:
                add("MachineGunner", 2, 3)
        elif choice <= 80:
            add("BomberShooter", 1, 1)
            add("Spider", 1, 1)
            add("Ameba", 0, 2)
            if enemy_set_2 == 1:
                add("Twins", 2, 3)
            elif enemy_set_2 == 2:
                add("MachineGunner", 1, 2)
        elif choice <= 100:
            add("BigSpreader", 2, 2)
            add("SmallVampire", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 0, 2)
        elif choice <= 120:
            add("Mite", 2, 3)
            add("SmallCarrier", 1, 2)
            add("Ameba", 0, 2)
        elif choice <= 125:
            add("InfusoriaSpawner", 1, 1)
            add("Infusoria", 1, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
        elif choice <= 130:
            add("BubbleContainer", 1, 1)
            add("Infusoria", 2, 3)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
        elif choice <= 140:
            add("Propeller", 1, 1)
            add("BubbleBomber", 2, 3)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
        elif choice <= 150:
            add("Snail", 1, 1)
            add("BubbleBomber", 0, 1)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
        elif choice <= 160:
            add("EnemySpawner", 1, 1)
            if enemy_set_1 == 1:
                add("Gull", 5, 6)
            elif enemy_set_1 == 2:
                add("Scarab", 5, 6)
            elif enemy_set_1 == 3:
                add("Bug", 5, 6)
        else:
            add("SeekerSpawner", 0, 1)
            if enemy_set_1 == 1:
                add("Predator_1", 2, 3)
            elif enemy_set_1 == 2:
                add("Predator_2", 2, 3)
            elif enemy_set_1 == 3:
                add("LongMachineGunner", 2, 3)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("Cell", 0, 2)

    elif world_distance < 30:
        choice = randint(1, 150)
        if choice <= 20:
            add("BubbleBomber", 2, 3)
            add("Spider", 2, 2)
            add("SeekerSpawner", 0, 2)
            add("Infusoria", 1, 2)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("Cell", 0, 2)
        elif choice <= 40:
            add("BubbleBomber", 2, 3)
            add("LongSpreader", 1, 1)
            add("Infusoria", 0, 2)
            add("Ameba", 0, 2)
        elif choice <= 60:
            add("SmallVampire", 2, 3)
            add("Beetle", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 0, 2)
        elif choice <= 80:
            add("Infusoria", 0, 1)
            add("Ameba", 0, 2)
            add("LargeVampire", 1, 1)
            if enemy_set_1 == 1:
                add("Gull", 2, 4)
            elif enemy_set_1 == 2:
                add("Scarab", 2, 4)
            elif enemy_set_1 == 3:
                add("Bug", 2, 4)
        elif choice <= 100:
            add("LargeVampire", 1, 1)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
                add("SmallVampire", 2, 2)
            elif enemy_set_2 == 2:
                add("Cell", 1, 2)
                add("BigSpreader", 2, 2)
        elif choice <= 105:
            add("InfusoriaSpawner", 1, 1)
            add("Infusoria", 1, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 1, 2)
        elif choice <= 110:
            add("BubbleContainer", 1, 1)
            add("Infusoria", 2, 3)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 1, 2)
        elif choice <= 120:
            add("Propeller", 1, 1)
            add("BubbleBomber", 3, 4)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 1, 2)
            elif enemy_set_2 == 2:
                add("Cell", 1, 2)
        elif choice <= 130:
            add("Snail", 1, 1)
            add("BubbleBomber", 2, 3)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 2)
            elif enemy_set_2 == 2:
                add("Cell", 2, 2)
        elif choice <= 140:
            add("EnemySpawnerLarge", 1, 1)
            add("StickyTurtle", 2, 3)
            add("Infusoria", 0, 2)
        elif choice <= 150:
            add("Ameba", 1, 2)
            add("Spider", 1, 2)
            add("Sucker", 2, 3)
            if enemy_set_1 == 1:
                add("Gull", 1, 3)
            elif enemy_set_1 == 2:
                add("Scarab", 1, 3)
            elif enemy_set_1 == 3:
                add("Bug", 1, 3)

    elif world_distance < 35:
        choice = randint(1, 160)
        if choice <= 20:
            add("SmallPropeller", 1, 2)
            add("Ant", 2, 3)
            add("SeekerSpawner", 0, 1)
        elif choice <= 40:
            add("SmallPropeller", 1, 2)
            add("LongSpreader", 1, 1)
            add("Infusoria", 0, 2)
            add("Ameba", 0, 2)
        elif choice <= 60:
            add("MixedEnemy", 2, 3)
            add("BubbleBomber", 1, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 0, 2)
        elif choice <= 80:
            add("MixedEnemy", 1, 3)
            add("Spider", 0, 1)
            add("Ameba", 0, 2)
            if enemy_set_1 == 1:
                add("Gull", 3, 5)
            elif enemy_set_1 == 2:
                add("Scarab", 3, 5)
            elif enemy_set_1 == 3:
                add("Bug", 3, 5)
        elif choice <= 100:
            add("LargeVampire", 0, 1)
            add("LargeMachineGunner", 1, 1)
            add("BubbleBomber", 1, 3)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("Cell", 0, 2)
        elif choice <= 110:
            add("BigBaby", 1, 1)
            add("Infusoria", 1, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
        elif choice <= 120:
            add("Destroyer", 1, 1)
            add("BubbleBomber", 1, 2)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 3)
            elif enemy_set_2 == 2:
                add("Cell", 2, 3)
        elif choice <= 130:
            add("Propeller", 1, 1)
            add("SmallPropeller", 2, 2)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 0, 3)
            elif enemy_set_2 == 2:
                add("Cell", 0, 3)
        elif choice <= 140:
            add("EnemySpawnerLarge", 1, 1)
            add("LargeMachineGunner", 1, 1)
            add("Infusoria", 0, 2)
        elif choice <= 150:
            add("FatSpreader", 0, 1)
            if enemy_set_2 == 1:
                add("Spider", 1, 2)
            elif enemy_set_2 == 2:
                add("MachineGunner", 1, 2)
            add("Sucker", 2, 2)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 2)
        elif choice <= 160:
            if enemy_set_2 == 1:
                add("Turret", 1, 2)
            elif enemy_set_2 == 2:
                add("SmallTurret", 1, 2)
            if enemy_set_1 == 1:
                add("Gull", 3, 4)
            elif enemy_set_1 == 2:
                add("Scarab", 3, 4)
            elif enemy_set_1 == 3:
                add("Bug", 3, 4)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 1)

    elif world_distance >= 35:
        choice = randint(1, 158)
        if choice <= 15:
            add("Infusoria", 0, 3)
            for _ in range(3):
                choice_2 = randint(1, 15)
                if choice_2 == 1:
                    add("LargeMachineGunner", 1, 1)
                elif choice_2 == 2:
                    add("SmallPropeller", 1, 2)
                elif choice_2 == 3:
                    add("MixedEnemy", 1, 2)
                elif choice_2 == 4:
                    add("Destroyer", 1, 1)
                    if enemy_set_2 == 1:
                        add("Baby", 1, 4)
                    elif enemy_set_2 == 2:
                        add("Cell", 1, 4)
                elif choice_2 == 5:
                    if enemy_set_2 == 1:
                        add("Baby", 1, 4)
                    elif enemy_set_2 == 2:
                        add("Cell", 1, 4)
                elif choice_2 == 6:
                    if enemy_set_2 == 1:
                        add("Twins", 1, 2)
                    elif enemy_set_2 == 2:
                        add("MachineGunner", 1, 2)
                elif choice_2 == 7:
                    add("SeekerSpawner", 1, 2)
                elif choice_2 == 8:
                    add("Infusoria", 1, 2)
                elif choice_2 == 9:
                    add("LargeMachineGunner", 1, 1)
                elif choice_2 == 10:
                    add("BubbleBomber", 1, 1)
                elif choice_2 == 11:
                    add("StickyTurtle", 1, 2)
                elif choice_2 == 12:
                    if enemy_set_1 == 1:
                        add("Predator_1", 1, 2)
                    elif enemy_set_1 == 2:
                        add("Predator_2", 1, 2)
                    elif enemy_set_1 == 3:
                        add("LongMachineGunner", 1, 2)
                elif choice_2 == 13:
                    add("SmallCarrier", 1, 2)
                elif choice_2 == 14:
                    add("Ant", 2, 4)
                else:
                    continue
        elif choice <= 20:
            add("SmallPropeller", 2, 2)
            add("Ant", 3, 6)
            add("Infusoria", 0, 2)
        elif choice <= 25:
            add("SmallPropeller", 1, 2)
            add("MixedEnemy", 2, 2)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("Cell", 0, 2)
        elif choice <= 30:
            add("MixedEnemy", 1, 3)
            add("StickyTurtle", 1, 3)
            add("Infusoria", 0, 2)
            add("Ameba", 0, 2)
        elif choice <= 35:
            add("LargeMachineGunner", 1, 2)
            add("BubbleBomber", 2, 3)
            add("Infusoria", 1, 3)
            add("Ameba", 0, 2)
        elif choice <= 40:
            add("LargeMachineGunner", 2, 2)
            add("Cockroach", 1, 2)
            add("StickyTurtle", 0, 1)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 2)
        elif choice <= 45:
            add("Infusoria", 0, 2)
            add("SmallVampire", 0, 2)
            if enemy_set_1 == 1:
                add("Twins", 4, 4)
            elif enemy_set_1 == 2:
                add("MachineGunner", 3, 4)
            elif enemy_set_1 == 3:
                add("MachineGunner", 1, 2)
                add("BigSpreader", 2, 3)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("Cell", 0, 2)
        elif choice <= 50:
            add("EnemySpawner", 1, 2)
            add("BubbleBomber", 2, 4)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 2)
        elif choice <= 53:
            add("LongSpreader", 1, 2)
            add("BubbleBomber", 1, 3)
            add("Ameba", 1, 2)
        elif choice <= 56:
            add("LongSpreader", 1, 2)
            add("SmallPropeller", 1, 1)
            add("Ameba", 1, 2)
        elif choice <= 61:
            add("FatSpreader", 1, 2)
            add("MixedEnemy", 1, 2)
            add("BubbleBomber", 0, 2)
            add("Ameba", 0, 2)
        elif choice <= 66:
            add("BigBaby", 1, 2)
            add("Turtle", 1, 2)
            add("BubbleBomber", 0, 2)
            add("Ameba", 0, 2)
        elif choice <= 69:
            add("Destroyer", 1, 1)
            add("Turtle", 0, 2)
            add("Infusoria", 1, 2)
        elif choice <= 72:
            add("Destroyer", 1, 1)
            add("StickyTurtle", 0, 2)
            add("Infusoria", 1, 2)
        elif choice <= 79:
            if enemy_set_2 == 1:
                add("Turret", 2, 3)
            elif enemy_set_2 == 2:
                add("SmallTurret", 2, 3)
            if enemy_set_1 == 1:
                add("Gull", 3, 4)
            elif enemy_set_1 == 2:
                add("Scarab", 3, 4)
            elif enemy_set_1 == 3:
                add("Bug", 3, 4)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 1)
        elif choice <= 86:
            add("Mite", 2, 3)
            add("Bug", 3, 4)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 1)
        elif choice <= 106:
            add("SeekerSpawner", 0, 2)
            add("Infusoria", 0, 2)
            add("Ameba", 1, 2)
            if enemy_set_1 == 1:
                add("Predator_1", 2, 2)
            elif enemy_set_1 == 2:
                add("Predator_2", 2, 2)
            elif enemy_set_1 == 3:
                add("LongMachineGunner", 2, 2)
        elif choice <= 116:
            add("Propeller", 1, 1)
            add("SmallPropeller", 2, 2)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 0, 3)
            elif enemy_set_2 == 2:
                add("Cell", 0, 3)
        elif choice <= 126:
            add("EnemySpawnerLarge", 1, 1)
            add("LargeMachineGunner", 1, 1)
            add("Infusoria", 0, 2)
        elif choice <= 136:
            add("Snail", 1, 1)
            add("BubbleBomber", 2, 3)
            add("Infusoria", 0, 2)
            if enemy_set_2 == 1:
                add("Baby", 2, 2)
            elif enemy_set_2 == 2:
                add("Cell", 2, 2)
        elif choice <= 146:
            add("FatSpreader", 1, 2)
            if enemy_set_2 == 1:
                add("Spider", 2, 2)
            elif enemy_set_2 == 2:
                add("MachineGunner", 2, 3)
            add("Sucker", 2, 3)
            add("Infusoria", 1, 2)
            add("Ameba", 0, 2)
        elif choice <= 148:
            add("Confusion", 1, 1)
            add("Infusoria", 1, 2)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("Cell", 0, 2)
        elif choice <= 158:
            add("LargeVampire", 1, 1)
            add("LargeMachineGunner", 1, 1)
            add("BubbleBomber", 3, 4)
            if enemy_set_2 == 1:
                add("Baby", 0, 2)
            elif enemy_set_2 == 2:
                add("Cell", 0, 2)
    return enemies


class BubbleTanksWorld:
    def __init__(self, player):
        self.player = player
        self.cur_room = None
        self.visited_rooms = dict()  # stores enemies in all visited rooms
        self.boss_generated = False
        self.boss_pos = None

    @property
    def current_enemies(self):
        return self.visited_rooms[self.cur_room]

    def room_visited(self, dx: int, dy: int) -> bool:
        """

        :param dx: horizontal shift of neighbour room
        :param dy: vertical shift of neighbour room

        Returns True if a neighbour room is already visited.
        """
        neigh_room = self.cur_room[0] + dx, self.cur_room[1] + dy
        return neigh_room in self.visited_rooms

    def set_save_data(self, save_data: dict):
        """
        :param save_data: dictionary that stores all save data

        Sets the parameters of the world according to the save data.
        """
        self.visited_rooms.clear()
        for key, value in save_data["enemies"].items():
            self.visited_rooms[tuple(map(int, key.split()))] = value
        self.cur_room = tuple(save_data["current room"])
        self.boss_generated = save_data["boss generated"]
        self.boss_pos = None if save_data["boss position"] is None else tuple(save_data["boss position"])

    def save_enemies(self, enemies: list):
        """
        :param enemies: list of enemies in current room

        Saves data on the types and number of enemies in current room to the dictionary.
        """
        data = defaultdict(int)
        for enemy in enemies:
            data[enemy.name] += 1
        self.visited_rooms[self.cur_room] = data

    def move(self, dx: int, dy: int):
        """
        :param dx: horizontal shift
        :param dy: vertical shift

        Shifts the coordinates of the current room in the given direction.
        """
        self.cur_room = self.cur_room[0] + dx, self.cur_room[1] + dy

    def estimate_difficulty(self, enemies=None, dx=0, dy=0):
        if enemies is None:
            room = self.cur_room[0] + dx, self.cur_room[1] + dy
            enemies = self.visited_rooms[room]
        difficulty = 0
        for enemy, n in enemies.items():
            if enemy in ("Infusoria", "Cell"):
                difficulty -= 0.2 * n
            elif enemy in ("Baby", "Ameba"):
                difficulty -= 0.02 * n
            elif enemy in ("InfusoriaSpawner", "BubbleContainer", "BigBaby"):
                difficulty -= 2.5 * n
                difficulty += n
        return difficulty

    def create_easy_enemies(self):
        return generate_easy(self.player.health_change)

    def confirm_enemies(self, enemies: dict, dx: int, dy: int):
        room = self.cur_room[0] + dx, self.cur_room[1] + dy
        self.visited_rooms[room] = enemies

    def create_enemies(self, dx: int, dy: int):
        room = self.cur_room[0] + dx, self.cur_room[1] + dy
        if room in self.visited_rooms:
            return
        if not self.boss_generated and self.player.cumulative_health > 1400:
            enemies = generate_boss()
            self.boss_generated = True
            self.boss_pos = room
        else:
            world_distance = round(sqrt(room[0] ** 2 + room[1] ** 2))
            help_chance = 0
            if self.player.is_help_needed:
                help_chance = uniform(0, 100)
            if help_chance > 50:
                enemies = generate_help(world_distance)
            else:
                enemies = generate_enemies(world_distance)
        self.visited_rooms[room] = enemies


__all__ = ["BubbleTanksWorld"]

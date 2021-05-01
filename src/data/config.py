# screen
ASPECT_RATIO = 4/3
SCR_H = 960
SCR_W = int(ASPECT_RATIO * SCR_H)
SCR_W2 = SCR_W // 2
SCR_H2= SCR_H // 2
SCR_SIZE = (SCR_W, SCR_H)
K = SCR_H / 960

# start menu
START_MENU_SHOW = 1
START_MENU_WAIT = 0
START_MENU_HIDE = -1
START_MENU_ANIMATION_TIME = 1500

# upgrade_menu
UPGRADE_MENU_ANIMATION_TIME = 350

# game
ROOM_RADIUS = int(7/6 * SCR_H)
DIST_BETWEEN_ROOMS = int(3.05 * SCR_H)
TRANSPORTATION_TIME = 600
MU = 0.00064


# room
BOSS_IS_FAR_AWAY = 0
BOSS_IN_NEIGHBOUR_ROOM = 1
BOSS_IN_CURRENT_ROOM = 2

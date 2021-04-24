from data.colors import BUBBLE_COLOR, BUBBLE_COLOR_2


BUBBLES = {"small":
               {"radius": 19,
                "health": 1,
                "body": ((19, 3, BUBBLE_COLOR, 0, 0, True, 0.028, 18, 0, True, False),)
                },
           "medium":
               {"radius": 28,
                "health": 5,
                "body": ((28, 3, BUBBLE_COLOR, 0, 0, True, 0.022, 13, 0, True, False),)
                },
           "big":
               {"radius": 39,
                "health": 25,
                "body": ((39, 5, BUBBLE_COLOR_2, 0, 0, True, 0.029, 18, 0, True, False),)
                }
           }

MAX_VEL = 0.64
ACC = 0.0024

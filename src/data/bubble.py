from data.colors import BUBBLE_COLOR, BUBBLE_COLOR_2
from utils import scaled_body, HF


BUBBLES = {"small":
               {"radius": HF(17),
                "health": 1,
                "body": scaled_body([[17, 3, BUBBLE_COLOR, 0, 0, True, 0.030, 16, True, False]])
                },
           "medium":
               {"radius": HF(24),
                "health": 5,
                "body": scaled_body([[24, 3, BUBBLE_COLOR, 0, 0, True, 0.02, 11, True, False]])
                },
           "big":
               {"radius": HF(34),
                "health": 25,
                "body": scaled_body([[34, 4, BUBBLE_COLOR_2, 0, 0, True, 0.026, 16, True, False]])
                }
           }

BUBBLE_MAX_VEL = HF(0.7)
BUBBLE_ACC = HF(0.0024)


__all__ = [

    "BUBBLES",
    "BUBBLE_MAX_VEL",
    "BUBBLE_ACC"

]

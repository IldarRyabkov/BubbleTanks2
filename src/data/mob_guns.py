"""
Stores for each mobs basic guns parameters:
radius, bullet velocity, bullet damage, bullet name, cooldown time, delay time.

"""

from utils import HF


GUN_BOSS_HEAD_PARAMS      = HF(64),  HF(0.88), 0,   'StickyBullet',         900,  -1000
GUN_BOSS_HAND_PARAMS      = HF(64),  HF(1.1),  -3,  'SmallScalingBullet_2', 900,  -1000
GUN_BOSS_LEG_PARAMS       = HF(228), HF(0.56), -10, 'HomingMissile_2',      1500, -1000
GUN_TURTLE_PARAMS         = HF(57),  HF(0.88), 0,   'StickyBullet',         1700, -2000
GUN_TURTLE_DMG_PARAMS     = HF(57),  HF(0.88), -10, 'BigBullet_2',          1700, -2000
GUN_TERRORIST_PARAMS      = 0,       0,        -10, 'BombBullet_2',         3000, -2000
GUN_BENLADEN_PARAMS       = 0,       0,        -10, 'BombBullet_2',         3000, -2000
GUN_BUG_PARAMS            = HF(17),  HF(0.8),  -2,  'SmallBullet_2',        900,  -1000
GUN_ANT_PARAMS            = HF(14),  HF(0.8),  -2,  'SmallBullet_2',        900,  -1000
GUN_SCARAB_PARAMS         = HF(14),  HF(0.8),  -2,  'SmallBullet_2',        900,  -1000
GUN_GULL_PARAMS           = HF(14),  HF(0.8),  -2,  'SmallBullet_2',        900,  -1000
GUN_COCKROACH_PARAMS      = HF(14),  HF(0.8),  -2,  'SmallBullet_2',        900,  -1000
GUN_BOMBERSHOOTER_PARAMS  = HF(17),  HF(0.8),  -2,  'SmallBullet_2',        900,  -1000
GUN_BEETLE_PARAMS         = 0,       HF(0.88), -2,  'SmallScalingBullet_2', 450,  -1000
GUN_BEETLE_REVERSE_PARAMS = 0,       HF(0.88), -2,  'SmallScalingBullet_2', 900,  -900
GUN_SPREADER_PARAMS       = 0,       HF(0.44), -2,  'SmallBullet_2',        1500, -1000
GUN_BIGEGG_PARAMS         = HF(92),  HF(0.88), -2,  'SmallBullet_2',        900,  -1000
GUN_SPIDER_PARAMS         = 0,       HF(0.88), -2,  'SmallBullet_2',        900,  -1000
GUN_MACHINEGUNNER_PARAMS  = 0,       HF(1.3),  -2,  'SmallBullet_2',        3000, -2000
GUN_TURRET_PARAMS         = 0,       HF(1.3),  -4,  'SmallBullet_2',        2000, -2000


__all__ = [
    
    "GUN_TURRET_PARAMS",
    "GUN_BOMBERSHOOTER_PARAMS",
    "GUN_BEETLE_PARAMS",
    "GUN_SPREADER_PARAMS",
    "GUN_SPIDER_PARAMS",
    "GUN_MACHINEGUNNER_PARAMS",
    "GUN_BIGEGG_PARAMS",
    "GUN_BEETLE_REVERSE_PARAMS",
    "GUN_COCKROACH_PARAMS",
    "GUN_GULL_PARAMS",
    'GUN_SCARAB_PARAMS',
    "GUN_ANT_PARAMS",
    "GUN_BUG_PARAMS",
    "GUN_BENLADEN_PARAMS",
    "GUN_TERRORIST_PARAMS",
    "GUN_TURTLE_DMG_PARAMS",
    "GUN_TURTLE_PARAMS",
    "GUN_BOSS_HAND_PARAMS",
    "GUN_BOSS_HEAD_PARAMS",
    "GUN_BOSS_LEG_PARAMS"
    
]
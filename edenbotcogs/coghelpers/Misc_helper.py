# Author: triple-lariat a.k.a: Tranquille, Desarroi, M.B.
# Any issues you encounter can be posted to https://github.com/triple-lariat/edenAHcheckerPY
# You may also find me on Eden or Eden's discord under the name Tranquille

exp_tnl = {
    1: 500,
    2: 750,
    3: 1000,
    4: 1250,
    5: 1500,
    6: 1750,
    7: 2000,
    8: 2200,
    9: 2400,
    10: 2600,
    11: 2800,
    12: 3000,
    13: 3200,
    14: 3400,
    15: 3600,
    16: 3800,
    17: 4000,
    18: 4200,
    19: 4400,
    20: 4600,
    21: 4800,
    22: 5000,
    23: 5100,
    24: 5200,
    25: 5300,
    26: 5400,
    27: 5500,
    28: 5600,
    29: 5700,
    30: 5800,
    31: 5900,
    32: 6000,
    33: 6100,
    34: 6200,
    35: 6300,
    36: 6400,
    37: 6500,
    38: 6600,
    39: 6700,
    40: 6800,
    41: 6900,
    42: 7000,
    43: 7100,
    44: 7200,
    45: 7300,
    46: 7400,
    47: 7500,
    48: 7600,
    49: 7700,
    50: 7800,
    51: 8000,
    52: 9200,
    53: 10400,
    54: 11600,
    55: 12800,
    56: 14000,
    57: 15200,
    58: 16400,
    59: 17600,
    60: 18800,
    61: 20000,
    62: 21500,
    63: 23000,
    64: 24500,
    65: 26000,
    66: 27500,
    67: 29000,
    68: 30500,
    69: 32000,
    70: 34000,
    71: 36000,
    72: 38000,
    73: 40000,
    74: 42000,
    75: 44000
}


def get_tnl(init_lv, target_lv):
    if init_lv not in exp_tnl or target_lv not in exp_tnl:
        return "Invalid levels provided."
    if init_lv > target_lv:
        return "Target level less than initial level."
    tnl = 0
    for level in range(init_lv, target_lv):
        tnl += exp_tnl[level]
    return f"Exp from Level {init_lv} to Level {target_lv} is {tnl}."
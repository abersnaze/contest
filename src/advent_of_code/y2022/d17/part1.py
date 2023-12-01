#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product, repeat
import math
from functools import reduce


rock_shapes = [
    (30,),
    (
        8,
        28,
        8,
    ),
    (
        28,
        4,
        4,
    ),
    (
        16,
        16,
        16,
        16,
    ),
    (
        24,
        24,
    ),
]

jets = list(map(lambda x: x.strip(), fileinput.input()))[0]
chamber = defaultdict(lambda: 0)
chamber[0] = 127
next_rock = 0


def chamber_height():
    y = 0
    while chamber[y] != 0:
        y += 1
    return y


def new_rock():
    global next_rock
    r = list(rock_shapes[next_rock])
    next_rock = (next_rock + 1) % len(rock_shapes)
    return r, chamber_height() + 3


rock_shape, rock_y = new_rock()


def dump():
    height = max(len(chamber) - 1, len(rock_shape) + rock_y - 1)
    for y in range(height, -1, -1):
        row = chamber[y]
        s = 64
        while s > 0:
            rock_row = 0
            if rock_y <= y and y < rock_y + len(rock_shape):
                rock_row = rock_shape[y - rock_y]
            if row & s != 0:
                print("#", end="")
            elif rock_row & s != 0:
                print("@", end="")
            else:
                print(".", end="")
            s >>= 1
        print()


def move_rock(jet):
    global rock_y
    if jet == "<":
        bump = False
        for i in range(len(rock_shape)):
            chamber_row = 128 | chamber[i + rock_y]
            if chamber_row & (rock_shape[i] << 1) != 0:
                bump = True
        if not bump:
            for i in range(len(rock_shape)):
                rock_shape[i] <<= 1
    else:
        bump = False
        for i in range(len(rock_shape)):
            chamber_row = chamber[i + rock_y]
            if chamber_row & (rock_shape[i] >> 1) != 0 or rock_shape[i] & 1 != 0:
                bump = True
        if not bump:
            for i in range(len(rock_shape)):
                rock_shape[i] >>= 1

    bump = False
    for i in range(len(rock_shape)):
        chamber_row = chamber[i + rock_y - 1]
        if chamber_row & rock_shape[i]:
            bump = True
    if not bump:
        rock_y -= 1

    return bump


def settle_rock():
    for i in range(len(rock_shape)):
        chamber_row = chamber[i + rock_y]
        chamber[i + rock_y] = chamber_row | rock_shape[i]


num_rocks = 0
dump()
while True:
    for i in range(len(jets)):
        # print(jets[i])
        if move_rock(jets[i]):
            settle_rock()
            num_rocks += 1
            if num_rocks == 1000000000000:
                print(chamber_height() - 1)
                exit(0)
            rock_shape, rock_y = new_rock()
    # dump()

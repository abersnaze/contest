#!python3

import fileinput
import re
from collections import defaultdict, Counter
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
_h = len(jets) * 10
print(_h)
_chamber = [127 for _ in range(_h)]


def chamber(r, v=None):
    global _chamber
    if v is not None:
        _chamber[r % _h] = v
        return v
    return _chamber[r % _h]


chamber_height = 0
next_rock = 0


def new_rock():
    global next_rock
    r = list(rock_shapes[next_rock])
    next_rock = (next_rock + 1) % len(rock_shapes)
    # clear out some of the ring
    for i in range(chamber_height, chamber_height + len(rock_shapes) + 4):
        chamber(i, 0)
    return r, chamber_height + 3


rock_shape, rock_y = new_rock()


def dump(h=10):
    for y in range(chamber_height + 5, chamber_height - h, -1):
        row = chamber(y)
        s = 64
        line = str(y) + "\t"
        while s > 0:
            rock_row = 0
            if rock_y <= y and y < rock_y + len(rock_shape):
                rock_row = rock_shape[y - rock_y]
            if row & s != 0:
                line += "#"
            elif rock_row & s != 0:
                line += "@"
            else:
                line += "."
            s >>= 1
        print(line)


def move_rock(jet):
    global rock_y
    if jet == "<":
        bump = False
        for i in range(len(rock_shape)):
            chamber_row = 128 | chamber(i + rock_y)
            if chamber_row & (rock_shape[i] << 1) != 0:
                bump = True
        if not bump:
            for i in range(len(rock_shape)):
                rock_shape[i] <<= 1
    else:
        bump = False
        for i in range(len(rock_shape)):
            chamber_row = chamber(i + rock_y)
            if chamber_row & (rock_shape[i] >> 1) != 0 or rock_shape[i] & 1 != 0:
                bump = True
        if not bump:
            for i in range(len(rock_shape)):
                rock_shape[i] >>= 1

    bump = False
    for i in range(len(rock_shape)):
        chamber_row = chamber(i + rock_y - 1)
        if chamber_row & rock_shape[i]:
            bump = True
    if not bump:
        rock_y -= 1

    return bump


def settle_rock():
    global chamber_height
    chamber_height = max(chamber_height, rock_y + len(rock_shape))
    for i in range(len(rock_shape)):
        chamber_row = chamber(i + rock_y)
        chamber(i + rock_y, chamber_row | rock_shape[i])


start_loop_search = 100


def scan_for_loops():
    print(".", end="")
    matches = []
    lookback = chamber_height - start_loop_search
    seed = chamber(lookback)
    for i in range(1, 1000):
        if seed == chamber(lookback - i):
            matches.append(lookback - i)

    while len(matches) > 1:
        for i in range(1, _h):
            sample = chamber(lookback - i)
            still_matches = []
            # print(matches)
            # dump(chamber_height - matches[1] + 2)
            # print()
            for match in matches:
                if sample == chamber(match - i):
                    still_matches.append(match)
            matches = still_matches
            if len(matches) > 0 and lookback - i == matches[0] and i > 5:
                return lookback, i
    return None, None


num_rocks = 0
loop_rocks = 0
loop_start = None
loop_size = None
skip_height = 0
loop_applied = False


def has_loop_repeat():
    for i in range(loop_size):
        if chamber(chamber_height - i - start_loop_search) != chamber(loop_start - i):
            return False
    return True


# dump()
while True:
    for i in range(len(jets)):
        # print(str(jets[i]) +" "+ str(chamber_height))
        # dump()
        if move_rock(jets[i]):
            settle_rock()
            if loop_start is not None:
                loop_rocks += 1
                if has_loop_repeat() and not loop_applied:
                    skip_times = (1000000000000 - num_rocks) // loop_rocks
                    num_rocks += skip_times * loop_rocks
                    skip_height = skip_times * loop_size
                    loop_applied = True
            if chamber_height > _h and loop_start is None and not loop_applied:
                loop_start, loop_size = scan_for_loops()
            num_rocks += 1
            if num_rocks == 1000000000000:
                print(chamber_height, skip_height)
                print(chamber_height + skip_height)
                print(1514285714288)
                exit(0)
            rock_shape, rock_y = new_rock()
        if num_rocks % 1000 == 0:
            print(str(num_rocks) + "\t" + str(chamber_height))

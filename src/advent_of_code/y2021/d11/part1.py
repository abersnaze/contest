#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice


octopi = {}

lines = map(lambda x: x.strip(), fileinput.input())
for y, line in enumerate(lines):
    for x, level in enumerate(line):
        octopi[(x, y)] = int(level)


def adjacent(a):
    x, y = a
    return [
        (x + 1, y + 1),
        (x + 0, y + 1),
        (x - 1, y + 1),
        (x - 1, y + 0),
        (x - 1, y - 1),
        (x + 0, y - 1),
        (x + 1, y - 1),
        (x + 1, y + 0),
    ]


def dump(m, default):
    for y in range(10):
        for x in range(10):
            xy = (x, y)
            if xy in m:
                print(str(m.get(xy, default)) + " ", end="")
        print()
    print()


total = 0
for step in range(100):
    dump(octopi, "-")
    nxt = {xy: v + 1 for xy, v in octopi.items()}
    done = False
    flashed = set()
    while not done:
        flashing = set([xy for xy, v in nxt.items() if v > 9 and v not in flashed])
        print(flashing)
        if not flashing:
            total += len(flashed)
            for xy in flashed:
                nxt[xy] = 0
            done = True
        else:
            flashed.update(flashing)
            for xy in flashing:
                for adj in adjacent(xy):
                    if adj in nxt:
                        nxt[adj] += 1
                nxt[xy] -= 1000
            flashing = set()
        nxt = nxt
    octopi = nxt

print(total)

#!python3

import fileinput
import re
from collections import defaultdict, Counter
from itertools import islice, product, repeat
from functools import reduce
from math import inf
from enum import Enum


class Dir(Enum):
    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    SE = (1, 1)
    S = (0, 1)
    SW = (-1, 1)
    W = (-1, 0)
    NW = (-1, -1)

    def add(self, x, y):
        return (x + self.value[0], y + self.value[1])


def update_bounds(p):
    global width, height
    height = (min(height[0], p[1]), max(height[1], p[1] + 1))
    width = (min(width[0], p[0]), max(width[1], p[0] + 1))


space = defaultdict(lambda: ".")
lines = list(map(lambda x: x.rstrip(), fileinput.input()))
width = (inf, -inf)
height = (inf, -inf)
elves = set()
for y, line in enumerate(lines):
    for x, s in enumerate(line):
        p = (x, y)
        space[p] = s
        if s == "#":
            elves.add(p)
        update_bounds(p)


def dump():
    for y in range(*height):
        line = ""
        for x in range(*width):
            c = "#" if (x, y) in elves else "."
            line += c
        print(line)


dump()


def consider(p, round):
    order = [
        (Dir.N, 0b11000001),
        (Dir.S, 0b00011100),
        (Dir.W, 0b00000111),
        (Dir.E, 0b01110000),
        (Dir.N, 0b11000001),
        (Dir.S, 0b00011100),
        (Dir.W, 0b00000111),
        (Dir.E, 0b01110000),
    ]
    count = 0
    for dir in Dir:
        count <<= 1
        if dir.add(*p) in elves:
            count += 1
    if count == 0:
        return
    for i in range(4):
        dir, test = order[round % 4 + i]
        if count & test == 0:
            yield dir.add(*p)
            return


round = 0
success = 1
while success > 0:
    proposals = defaultdict(list)

    for elf in elves:
        for propose in consider(elf, round):
            proposals[propose].append(elf)

    success = 0
    for proposed, proposed_by in proposals.items():
        if len(proposed_by) == 1:
            elves.discard(proposed_by[0])
            elves.add(proposed)
            update_bounds(proposed)
            success += 1
    print("round", round + 1, success)
    round += 1

dump()

width = (inf, -inf)
height = (inf, -inf)
for elf in elves:
    update_bounds(elf)

w = width[1] - width[0]
h = height[1] - height[0]

print(w, h, w * h)
print(w * h - len(elves))

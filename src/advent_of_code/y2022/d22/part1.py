#!python3

import fileinput
import re
from collections import defaultdict, Counter
from itertools import islice, product, repeat
from functools import reduce
from math import inf
from enum import Enum


class Dir(Enum):
    U = (0, -1)
    D = (0, 1)
    L = (-1, 0)
    R = (1, 0)

    def rotate(self, turn):
        if turn == "r":
            if self == Dir.U:
                return Dir.R
            if self == Dir.R:
                return Dir.D
            if self == Dir.D:
                return Dir.L
            if self == Dir.L:
                return Dir.U
        if turn == "l":
            if self == Dir.U:
                return Dir.L
            if self == Dir.L:
                return Dir.D
            if self == Dir.D:
                return Dir.R
            if self == Dir.R:
                return Dir.U

    def step(self, cx, cy):
        return (cx + self.value[0], cy + self.value[1])

    def symbol(self):
        if self == Dir.U:
            return "↑"
        if self == Dir.R:
            return "→"
        if self == Dir.D:
            return "↓"
        if self == Dir.L:
            return "←"

    def num(self):
        if self == Dir.U:
            return 3
        if self == Dir.R:
            return 0
        if self == Dir.D:
            return 1
        if self == Dir.L:
            return 2


lines = list(map(lambda x: x.rstrip(), fileinput.input()))
size = int(lines.pop(0))
edges = lines.pop(0)
movements = lines.pop()
moves = {}
space = defaultdict(lambda: " ")
row_bounds = defaultdict(lambda: [inf, -inf])
col_bounds = defaultdict(lambda: [inf, -inf])
w, h = 0, 0
for y, line in enumerate(lines):
    for x, s in enumerate(line):
        space[(x, y)] = s
        if s == " ":
            continue
        w = max(w, x)
        h = max(h, y)
        r_min, r_max = row_bounds[y]
        row_bounds[y] = [min(r_min, x), max(r_max, x)]
        c_min, c_max = col_bounds[x]
        col_bounds[x] = [min(c_min, y), max(c_max, y)]

start = (row_bounds[0][0], col_bounds[row_bounds[0][0]][0])
curr = start
face = Dir.R


def in_front():
    adjacent = face.step(*curr)
    s = space[adjacent]
    if s == " ":
        if face == Dir.U:
            adjacent = (curr[0], col_bounds[curr[0]][1])
        if face == Dir.D:
            adjacent = (curr[0], col_bounds[curr[0]][0])
        if face == Dir.L:
            adjacent = (row_bounds[curr[1]][1], curr[1])
        if face == Dir.R:
            adjacent = (row_bounds[curr[1]][0], curr[1])
        s = space[adjacent]
    return adjacent, s


def dump():
    for y in range(h):
        line = ""
        for x in range(w):
            c = space[(x, y)]
            if (x, y) in moves:
                c = moves[(x, y)]
            line += c
        print(line)


for dist, turn in re.findall("([0-9]+)([RL])", movements):
    for d in range(int(dist)):
        moves[curr] = face.symbol()
        next, s = in_front()
        if s != ".":
            break
        curr = next
    face = face.rotate(turn.lower())
    moves[curr] = face.symbol()

dump()
print(curr, start)
print(1000 * (curr[1] + 1) + 4 * (curr[0] + 1) + face.num())

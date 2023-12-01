#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product, repeat
import math
from functools import reduce

x_min = 500
x_max = 500
y_min = 0
y_max = 0
space = defaultdict(lambda: ".")
space[(500, 0)] = "+"
lines = map(lambda x: x.strip(), fileinput.input())
for line in lines:
    px, py = None, None
    for point in line.split(" -> "):
        cx, cy = point.split(",")
        cx = int(cx)
        cy = int(cy)
        x_min = min(x_min, cx)
        x_max = max(x_max, cx)
        y_min = min(y_min, cy)
        y_max = max(y_max, cy)
        if px == cx:
            dir = 1 if cy < py else -1
            for y in range(cy, py + dir, dir):
                space[(cx, y)] = "#"
        if py == cy:
            dir = 1 if cx < px else -1
            for x in range(cx, px + dir, dir):
                space[(x, cy)] = "#"
        px = cx
        py = cy


def dump():
    print(x_min, x_max, y_min, y_max)
    for y in range(y_min - 1, y_max + 2):
        for x in range(x_min - 1, x_max + 2):
            print(space[(x, y)], end="")
        print()


def down(frm):
    return (frm[0], frm[1] + 1)


def downleft(frm):
    return (frm[0] - 1, frm[1] + 1)


def downright(frm):
    return (frm[0] + 1, frm[1] + 1)


def fall(frm):
    to = down(frm)
    if space[to] == ".":
        return to
    to = downleft(frm)
    if space[to] == ".":
        return to
    to = downright(frm)
    if space[to] == ".":
        return to
    return None


def drop():
    curr = (500, 0)
    next = fall(curr)
    while next is not None:
        if next[1] > y_max:
            return False
        curr = next
        next = fall(next)
    space[curr] = "o"
    return True


dump()

accumulate = 0
while drop():
    accumulate += 1
    # dump()

dump()

print(accumulate)

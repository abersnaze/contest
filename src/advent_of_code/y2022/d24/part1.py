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

    def step(self, cx, cy):
        return (cx + self.value[0], cy + self.value[1])


blizzard_U = defaultdict(lambda: False)
blizzard_D = defaultdict(lambda: False)
blizzard_L = defaultdict(lambda: False)
blizzard_R = defaultdict(lambda: False)
walls = defaultdict(lambda: False)
lines = list(map(lambda x: x.rstrip(), fileinput.input()))
start = None
end = None
height = len(lines)
for y, line in enumerate(lines):
    width = len(line)
    print(line)
    for x, s in enumerate(line):
        p = (x, y)
        if s == "." and y == 0:
            start = p
        if s == "." and y == height - 1:
            end = p
        if s == "#":
            walls[p] = True
        if s == ">":
            blizzard_R[p] = True
        if s == "<":
            blizzard_L[p] = True
        if s == "^":
            blizzard_U[p] = True
        if s == "v":
            blizzard_D[p] = True

space = defaultdict(lambda: False)
filled_to = -1
print(start, end)


def dump(cx, cy, cd):
    fill(cd)
    for y in range(height):
        line = ""
        for x in range(width):
            s = "#" if space[((x, y, cd))] else "."
            if x == cx and y == cy:
                s = "@"
            line += s
        print(line)


def fill(d):
    if d <= filled_to:
        return
    for x in range(width):
        for y in range(height):
            space[(x, y, d)] = (
                walls[(x, y)]
                or blizzard_U[(x, (y + d - 1) % (height - 2) + 1)]
                or blizzard_D[(x, (y - d - 1) % (height - 2) + 1)]
                or blizzard_L[((x + d - 1) % (width - 2) + 1, y)]
                or blizzard_R[((x - d - 1) % (width - 2) + 1, y)]
            )


def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


queue = [(*start, 0)]
costs = defaultdict(lambda: inf)
costs[(*start, 0)] = 0
done = False
best = inf
while not done and queue:
    curr = queue.pop()
    curr_dist = dist(curr, end)
    curr_x, curr_y, curr_t = curr
    fill(curr_t + 1)
    cost = costs[curr]
    if curr_dist < best:
        best = curr_dist
        print("cost", cost, "dist", curr_dist, "at", curr)
        dump(*curr)
        print()
    for adjacent in [
        (curr_x, curr_y, curr_t + 1),
        (curr_x, curr_y - 1, curr_t + 1),
        (curr_x, curr_y + 1, curr_t + 1),
        (curr_x - 1, curr_y, curr_t + 1),
        (curr_x + 1, curr_y, curr_t + 1),
    ]:
        if adjacent[0] < 0 or adjacent[1] < 0:
            continue
        if adjacent[0] == end[0] and adjacent[1] == end[1]:
            done = True
            print(adjacent)
        if not space[adjacent] and costs[adjacent] > cost + 1:
            costs[adjacent] = cost + 1
            queue.append(adjacent)
    queue.sort(key=lambda p: costs[p], reverse=True)

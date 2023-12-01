#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product


lines = map(lambda x: x.strip(), fileinput.input())

heatmap = {}
assigned = {}
unassigneds = []
basin = Counter()

w = 0
h = 0
for y, line in enumerate(lines):
    for x, n in enumerate(line):
        heatmap[(x, y)] = int(n)
        unassigneds.append((x, y))
    w = len(line)
    h += 1


def adjacent(x, y):
    yield (x, y - 1)
    yield (x, y + 1)
    yield (x + 1, y)
    yield (x - 1, y)


for x in range(w):
    for y in range(h):
        here = heatmap[(x, y)]
        min_adj = min([heatmap[a] for a in adjacent(x, y) if a in heatmap])
        if here < min_adj:
            assigned[(x, y)] = (x, y)
            unassigneds.remove((x, y))
            basin[(x, y)] = 1
        if here == 9:
            unassigneds.remove((x, y))


while unassigneds:
    ux, uy = unassigneds.pop(0)
    bs = [assigned[a] for a in adjacent(ux, uy) if a in assigned]
    near_basin = min(bs, key=lambda b: heatmap[b]) if bs else None
    if near_basin:
        assigned[(ux, uy)] = near_basin
        basin[near_basin] += 1
    else:
        unassigneds.append((ux, uy))
    pass

print(basin)
largest = sorted(basin.values())[-3:]

print(largest[0] * largest[1] * largest[2])

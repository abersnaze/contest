#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice


lines = map(lambda x: x.strip(), fileinput.input())

heatmap = []

w = 0
h = 0

for y, line in enumerate(lines):
    heatmap.append([])
    for n in line:
        heatmap[y].append(int(n))
    w = len(line)
    h += 1


def adjacent(x, y):
    if y > 0:
        yield (x, y - 1)
    if y < h - 1:
        yield (x, y + 1)
    if x < w - 1:
        yield (x + 1, y)
    if x > 0:
        yield (x - 1, y)


risk = 0
for y in range(h):
    for x in range(w):
        here = heatmap[y][x]
        min_adj = min([heatmap[j][i] for i, j in adjacent(x, y)])
        if here < min_adj:
            risk += here + 1


print("\n".join(map(str, heatmap)))

print(risk)

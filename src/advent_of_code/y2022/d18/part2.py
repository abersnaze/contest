#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product, repeat
from math import inf
from functools import reduce

lines = list(map(lambda x: x.strip(), fileinput.input()))
x_min = inf
x_max = -inf
y_min = inf
y_max = -inf
z_min = inf
z_max = -inf
lava = defaultdict(lambda: False)
for line in lines:
    x, y, z = map(int, line.split(","))
    x_min = min(x_min, x)
    x_max = max(x_max, x)
    y_min = min(y_min, y)
    y_max = max(y_max, y)
    z_min = min(z_min, z)
    z_max = max(z_max, z)
    lava[(x, y, z)] = True


def bounded(x, y, z):
    if x < x_min - 1 or x_max + 1 < x:
        return False
    if y < y_min - 1 or y_max + 1 < y:
        return False
    if z < z_min - 1 or z_max + 1 < z:
        return False
    return True


def adjcent(x, y, z):
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


air = defaultdict(lambda: False)
queue = [(0, 0, 0)]
total_air = 0
while len(queue) > 0:
    p = queue.pop()
    if not lava.get(p, False):
        air[p] = True
        total_air += 1
        for adj in adjcent(*p):
            if not air[adj] and bounded(*p):
                queue.append(adj)
print(total_air)

total = 0
for x, y, z in lava.keys():
    for adj in adjcent(x, y, z):
        if air[adj]:
            total += 1

print(total)

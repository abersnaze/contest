#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product
import math
from functools import reduce

space = defaultdict(lambda: 0)
steps = defaultdict(lambda: math.inf)


class Dir(Enum):
    U = (0, -1)
    D = (0, +1)
    L = (-1, 0)
    R = (+1, 0)

    def add(self, p):
        return (p[0] + self.value[0], p[1] + self.value[1])


lines = map(lambda x: x.strip(), fileinput.input())
for y, line in enumerate(lines):
    for x, v in enumerate(line):
        if v == "S":
            start = (x, y)
        if v == "E":
            end = (x, y)
        space[(x, y)] = ord(v) - ord("a")
space[start] = 0
space[end] = 25

print(space)

poi = [end]
steps[end] = 0
while poi:
    print(len(poi))
    curr_p = poi.pop()
    curr_s = steps[curr_p]
    curr_h = space[curr_p]
    next_p = Dir.U.add(curr_p)
    next_s = curr_s + 1
    if next_p in space and space[next_p] - curr_h >= -1 and next_s < steps[next_p]:
        steps[next_p] = next_s
        poi.append(next_p)
    next_p = Dir.D.add(curr_p)
    if next_p in space and space[next_p] - curr_h >= -1 and next_s < steps[next_p]:
        steps[next_p] = next_s
        poi.append(next_p)
    next_p = Dir.L.add(curr_p)
    if next_p in space and space[next_p] - curr_h >= -1 and next_s < steps[next_p]:
        steps[next_p] = next_s
        poi.append(next_p)
    next_p = Dir.R.add(curr_p)
    if next_p in space and space[next_p] - curr_h >= -1 and next_s < steps[next_p]:
        steps[next_p] = next_s
        poi.append(next_p)

best = math.inf
for p in [p for p in space.keys() if space[p] == 0]:
    s = steps[p]
    if s == math.inf:
        continue
    print(p, s)
    if s < best:
        best = s
print(best)

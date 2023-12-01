#!python3

import fileinput
import re
from collections import defaultdict, Counter, deque
from enum import Enum
from itertools import islice, product
import math
from typing import List

lines = list(map(lambda x: x.strip(), fileinput.input()))

xmin, xmax, ymin, ymax = re.match(
    r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", lines[0]
).groups()

xmin = int(xmin)
xmax = int(xmax)
ymin = int(ymin)
ymax = int(ymax)


def hit(dx, dy):
    px, py = 0, 0
    pymax = 0
    while px <= xmax and py >= ymin:
        if px >= xmin and py <= ymax:
            return pymax
        px += dx
        py += dy
        pymax = max(pymax, py)
        if dx != 0:
            dx -= 1 if dx > 0 else -1
        dy -= 1
    return None


print(xmin, xmax, ymin, ymax)

dxmin = int(-0.5 + math.sqrt(0.25 + 2 * xmin)) + 1

count = 0
for dx in range(dxmin, xmax + 1):
    for dy in range(ymin - 1, 300):
        pymax = hit(dx, dy)
        if pymax is not None:
            count += 1

print(count)

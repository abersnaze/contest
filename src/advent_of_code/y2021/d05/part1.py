#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys
from enum import Enum
from itertools import islice

lines = map(lambda x: x.strip(), fileinput.input())

counts = Counter()

for line in lines:
    x1, y1, x2, y2 = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line).groups()
    if x1 != x2 and y1 != y2:
        print("\tskip", x1, y1, "->", x2, y2)
        continue
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    counts.update({(x, y): 1 for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)})

# didn't bother printing anything but the example
for y in range(10):
    for x in range(10):
        c = counts[(x, y)]
        print(c if c > 0 else ".", end="")
    print()

intersections = 0
for coords, count in counts.items():
    if count > 1:
        intersections += 1

print(intersections)

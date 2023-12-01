#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys
from enum import Enum
from itertools import islice


lines = map(lambda x: x.strip(), fileinput.input())

counts = Counter()


def steps(s, e, l):
    """custom range function for a list of values of a given length between two numbers (inclusive)"""
    if s == e:
        out = [s for i in range(l + 1)]
    elif s > e:
        out = list(range(s, e - 1, -1))
    else:
        out = list(range(s, e + 1, 1))
    return out


for line in lines:
    x1, y1, x2, y2 = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line).groups()
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    length = max(abs(x1 - x2), abs(y1 - y2))

    # switch to using zip with a custom range function
    counts.update(
        {coords: 1 for coords in zip(steps(x1, x2, length), steps(y1, y2, length))}
    )

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

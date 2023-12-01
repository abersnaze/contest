#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product
import math

lines = map(lambda x: x.strip(), fileinput.input())

risks = {}
for y, line in enumerate(lines):
    size = len(line)
    for x, risk in enumerate(line):
        risks[(x, y)] = int(risk)

cumulative = defaultdict(lambda: math.inf)
cumulative[(0, 0)] = 0


def adjacent(x, y):
    return [
        (x - 0, y + 1),
        (x - 1, y + 0),
        (x + 0, y - 1),
        (x + 1, y - 0),
    ]


def dump():
    for y in range(size):
        for x in range(size):
            r = cumulative[(x, y)]
            if math.isinf(r):
                print(".", end=" ")
            else:
                print(r, end=" ")
        print()
    print()


dump()

unchecked = set([(0, 0)])
while unchecked:
    curr = unchecked.pop()

    for adj in [a for a in adjacent(*curr) if a in risks]:
        adj_risk = risks[adj] + cumulative[curr]
        if adj_risk < cumulative[adj]:
            cumulative[adj] = adj_risk
            unchecked.add(adj)
    # dump()
    print(len(unchecked))
    pass
dump()

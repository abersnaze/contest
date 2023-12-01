#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product, repeat
from math import inf
from functools import reduce

lines = list(map(lambda x: x.strip(), fileinput.input()))
lava = defaultdict(lambda: False)
for line in lines:
    x, y, z = map(int, line.split(","))
    lava[(x, y, z)] = True


def adjcent(x, y, z):
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


total = len(lava) * 6
for x, y, z in lava.keys():
    for adj in adjcent(x, y, z):
        if adj in lava:
            total -= 1

print(total)

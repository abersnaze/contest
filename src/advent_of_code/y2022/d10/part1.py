#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product
import math

lines = map(lambda x: x.strip(), fileinput.input())

xs = [1]
for line in lines:
    parts = line.split(" ")
    x = xs[-1]
    if parts[0] == "addx":
        xs.extend([x, x + int(parts[1])])
    elif parts[0] == "noop":
        xs.append(x)

strengths = [(xs[cycle - 1], cycle) for cycle in range(20, 221, 40)]
print(strengths)

print(sum(map(lambda v: v[0] * v[1], strengths)))

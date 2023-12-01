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

for y in range(6):
    scan = []
    for x in range(40):
        cycle = y * 40 + x
        pos = xs[cycle]
        scan.append("#" if abs(x - pos) < 2 else ".")
    print("".join(scan))

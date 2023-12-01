#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

lines = fileinput.input()
stacks = defaultdict(list)
moves = []
for line in lines:
    if "[" in line:
        for i in range(1, len(line), 4):
            if line[i] != " ":
                stacks[1 + (i - 1) // 4].insert(0, line[i])
    if line.startswith("move"):
        _, n, _, fm, _, to = line.strip().split(" ")
        moves.append((int(n), int(fm), int(to)))

print(stacks)

for n, fm, to in moves:
    print(n, fm, to)
    for i in range(n):
        stacks[to].append(stacks[fm].pop())
    print(stacks)

for k in sorted(stacks.keys()):
    print(stacks[k][-1], end="")
print()

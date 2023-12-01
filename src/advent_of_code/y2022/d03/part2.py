#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

lines = map(lambda x: x.strip(), fileinput.input())

total = 0
stinking_badges = set()
for i, line in enumerate(lines):
    half = int(len(line) / 2)
    first = set(line[:half])
    second = set(line[half:])
    if i % 3 == 0:
        print(stinking_badges)
        if stinking_badges:
            common = next(iter(stinking_badges))
            if common.lower() == common:
                score = ord(common) - ord("a") + 1
            else:
                score = ord(common) - ord("A") + 26 + 1
            total += score

        stinking_badges = first.union(second)
    else:
        stinking_badges = stinking_badges.intersection(first.union(second))
print(stinking_badges)
common = next(iter(stinking_badges))
if common.lower() == common:
    score = ord(common) - ord("a") + 1
else:
    score = ord(common) - ord("A") + 26 + 1
total += score

print(total)

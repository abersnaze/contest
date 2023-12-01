#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

lines = map(lambda x: x.strip(), fileinput.input())

total = 0
sinbadge
for i, line in enumerate(lines):
    i % 3
    half = int(len(line) / 2)
    print(half)
    first = set(line[:half])
    second = set(line[half:])
    common = next(iter(first.intersection(second)))
    if common.lower() == common:
        score = ord(common) - ord("a") + 1
    else:
        score = ord(common) - ord("A") + 26 + 1
    total += score
    print(common, score)

print(total)

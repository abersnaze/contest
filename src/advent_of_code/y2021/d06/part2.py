#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys
from enum import Enum
from itertools import islice

lines = map(lambda x: x.strip(), fileinput.input())


def zero():
    return 0


today = defaultdict(zero)

for age in next(lines).split(","):
    today[int(age)] += 1

print(today)

for day in range(1, 256 + 1):
    print(day, today)

    tomorrow = defaultdict(zero)
    for age, count in today.items():
        if age == 0:
            tomorrow[6] += count
            tomorrow[8] += count
        else:
            tomorrow[age - 1] += count

    today = tomorrow

print(sum(today.values()))

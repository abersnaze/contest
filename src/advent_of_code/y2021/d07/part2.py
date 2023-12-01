#!python3

import fileinput
from os import truncate
import re
from collections import defaultdict, Counter
import sys
from enum import Enum
from itertools import islice
import statistics

lines = map(lambda x: x.strip(), fileinput.input())
depths = [int(x) for x in next(lines).split(",")]
fuel = lambda d: d * (d + 1) / 2
align = statistics.median(depths)

done = False
while not done:
    print(align)
    cost_plus1 = sum([fuel(abs(align + 1 - x)) for x in depths])
    cost_at = sum([fuel(abs(align - x)) for x in depths])

    if cost_at < cost_plus1:
        done = True
    else:
        align += 1

print(cost_at)

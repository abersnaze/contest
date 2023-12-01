#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys
from enum import Enum
from itertools import islice
import statistics

lines = map(lambda x: x.strip(), fileinput.input())
depths = [int(x) for x in next(lines).split(",")]
align = statistics.median(depths)
cost = sum([abs(align - x) for x in depths])

print(cost)

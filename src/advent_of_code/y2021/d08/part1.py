#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice


lines = map(lambda x: x.strip(), fileinput.input())

sum = 0
for line in lines:
    patterns, digits = line.split("|")
    patterns = map(lambda p: "".join(sorted(p)), patterns.strip().split(" "))
    digits = map(lambda p: "".join(sorted(p)), digits.strip().split(" "))

    mapping = {}

    for pattern in patterns:
        if len(pattern) == 2:
            mapping[pattern] = 1
        if len(pattern) == 3:
            mapping[pattern] = 7
        if len(pattern) == 4:
            mapping[pattern] = 4
        if len(pattern) == 7:
            mapping[pattern] = 8

    found = [d for d in digits if d in mapping]
    count = len(found)
    print(found, count, mapping)
    sum += count

print(sum)

#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import accumulate, islice
from yaml import dump


lines = map(lambda x: x.strip(), fileinput.input())


def only(f, i: iter):
    rs = list(filter(f, i))
    assert len(rs) == 1
    return rs[0]


actual = []
for i, line in enumerate(lines):
    patterns, digits = line.split("|")
    patterns = list(map(lambda p: "".join(sorted(p)), patterns.strip().split(" ")))
    digits = list(map(lambda p: "".join(sorted(p)), digits.strip().split(" ")))

    mapping_235 = list()
    mapping_069 = list()

    for pattern in patterns:
        if len(pattern) == 2:
            mapping_1 = pattern
        if len(pattern) == 3:
            mapping_7 = pattern
        if len(pattern) == 4:
            mapping_4 = pattern
        if len(pattern) == 5:
            mapping_235.append(pattern)
        if len(pattern) == 6:
            mapping_069.append(pattern)
        if len(pattern) == 7:
            mapping_8 = pattern

    mapping_9 = only(lambda x: len(set(mapping_4) - set(x)) == 0, mapping_069)
    mapping_6 = only(lambda x: len(set(mapping_1) - set(x)) == 1, mapping_069)
    mapping_0 = only(lambda x: x != mapping_6 and x != mapping_9, mapping_069)
    mapping_3 = only(lambda x: len(set(mapping_1) - set(x)) == 0, mapping_235)
    mapping_2 = only(lambda x: len(set(x) - set(mapping_9)) != 0, mapping_235)
    mapping_5 = only(lambda x: x != mapping_3 and x != mapping_2, mapping_235)

    mapping = [
        mapping_0,
        mapping_1,
        mapping_2,
        mapping_3,
        mapping_4,
        mapping_5,
        mapping_6,
        mapping_7,
        mapping_8,
        mapping_9,
    ]

    display = 0
    for digit in digits:
        display = display * 10 + mapping.index(digit)

    print(display)
    actual.append(display)

print(sum(actual))

#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

lines = map(lambda x: x.strip(), fileinput.input())

template = next(lines)
next(lines)

rules = {}
for line in lines:
    input, output = line.split(" -> ")
    rules[input] = input[0] + output


def apply(t: str):
    nxt = ""
    for i in range(0, len(t) - 1):
        x = t[i : i + 2]
        if x in rules:
            nxt += rules[x]
    return nxt + x[1]


for step in range(10):
    print(template)
    template = apply(template)


freq = Counter(template).values()

print(max(freq), "-", min(freq), "=", max(freq) - min(freq))

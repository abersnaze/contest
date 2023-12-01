#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

lines = map(lambda x: x.strip(), fileinput.input())

template = next(lines)
first = template[0]
last = template[-1]

pairs = Counter()
for i in range(0, len(template) - 1):
    pair = template[i : i + 2]
    pairs[pair] += 1

next(lines)

rules = {}
for line in lines:
    input, output = line.split(" -> ")
    rules[input] = output


def apply(ps: Counter):
    nxt = Counter()
    for p, c in ps.items():
        if p in rules:
            o = rules[p]
            nxt.update(
                {
                    p[0] + o: c,
                    o + p[1]: c,
                }
            )
    return nxt


for step in range(40):
    print(step + 1, sum(pairs.values()) + 1)
    pairs = apply(pairs)

letters = Counter(
    {
        first: 1,
        last: 1,
    }
)
for pair, count in pairs.items():
    letters[pair[0]] += count
    letters[pair[1]] += count

print(letters)

freq = list(map(lambda x: x // 2, letters.values()))

print(max(freq), "-", min(freq), "=", max(freq) - min(freq))

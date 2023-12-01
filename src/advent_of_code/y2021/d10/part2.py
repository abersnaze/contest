#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice
from functools import reduce


lines = map(lambda x: x.strip(), fileinput.input())
match = {
    "]": "[",
    ")": "(",
    ">": "<",
    "}": "{",
}
score = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

scores = []
for line in lines:
    stack = []
    for i, c in enumerate(line):
        if c in match:
            if not stack or stack[-1] != match[c]:
                break
            else:
                stack.pop()
        else:
            stack.append(c)
    if i + 1 == len(line):
        stack.reverse()
        s = reduce(lambda q, r: q * 5 + r, map(score.get, stack), 0)
        print("incomplete", s, line, stack)
        scores.append(s)

scores.sort()
l = len(scores)
print(scores[l // 2])

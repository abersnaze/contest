#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice


lines = map(lambda x: x.strip(), fileinput.input())
match = {
    "]": "[",
    ")": "(",
    ">": "<",
    "}": "{",
}
score = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

total = 0
for line in lines:
    stack = []
    for i, c in enumerate(line):
        if c in match:
            if not stack or stack[-1] != match[c]:
                print("corrupt", score[c], line[0:i], "\t", line[i:-1])
                total += score[c]
                break
            else:
                stack.pop()
        else:
            stack.append(c)

print(total)

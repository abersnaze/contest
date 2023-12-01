#!python3

import fileinput
import re
from collections import defaultdict


def parse_line(line):
    return int(line)


content = list(map(parse_line, fileinput.input()))

content.sort()

ones = 0
threes = 1
for i in range(len(content)):
    diff = content[i] - content[i - 1] if i > 0 else content[i]
    print(f"[{i}] = {content[i]} ∆ {diff}")
    if diff == 1:
        ones += 1
    if diff == 3:
        threes += 1

print(ones, "*", threes, "=", ones * threes)

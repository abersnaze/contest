#!python3

import fileinput
import re
from collections import defaultdict
from operator import mul
from functools import reduce


def parse_line(line):
    return int(line)


content = list(map(parse_line, fileinput.input()))
content.sort()

# calc diffs
diffs = []
for i in range(len(content)):
    diffs.append(content[i] - content[i - 1] if i > 0 else content[i])
diffs.append(3)
print("diffs", diffs)

# only the 1s might be removable.
# count the runs of ones found between 3s
runs = []
ones = 0
for i in range(len(diffs)):
    if diffs[i] == 1:
        ones += 1
    if diffs[i] == 3:
        # map the number of 1s to the number of permutation
        if ones == 0:
            # 33 -> 33
            runs.append(1)
        if ones == 1:
            # 313 -> 313
            runs.append(1)
        if ones == 2:
            # 3113 -> 3113, 323
            runs.append(2)
        if ones == 3:
            # 31113 -> 31113, 3123, 3213, 333
            runs.append(4)
        if ones == 4:
            # 311113 -> 311113, 31123, 31213, 32113, 3223, 3133, 3313
            runs.append(7)
        ones = 0
# multiple all the posibilities
print("runs", runs, reduce(mul, runs, 1))

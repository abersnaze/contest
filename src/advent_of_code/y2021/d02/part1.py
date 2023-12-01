#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys
from enum import Enum


class Dir(Enum):
    forward = (1, 0)
    down = (0, 1)
    up = (0, -1)


curr = (0, 0)
for line in map(lambda x: x.strip(), fileinput.input()):
    dir, amount = line.split(" ")

    d = Dir[dir]
    a = int(amount)

    nex = (curr[0] + d.value[0] * a, curr[1] + d.value[1] * a)
    print(curr, d, a, nex)
    curr = nex

print("final", curr, curr[0] * curr[1])

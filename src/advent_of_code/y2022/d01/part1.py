#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

lines = map(lambda x: x.strip(), fileinput.input())

elves = defaultdict(list)
elf_num = 1
for line in lines:
    if line == "":
        elf_num += 1
        continue
    elves[elf_num].append(int(line))

print(max([sum(cals) for cals in elves.values()]))

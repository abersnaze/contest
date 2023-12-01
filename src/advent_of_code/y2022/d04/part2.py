#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

lines = map(lambda x: x.strip(), fileinput.input())


def elf_assignment(s) -> set:
    start, end = s.split("-")
    return set(range(int(start), int(end) + 1))


total = 0
for line in lines:
    a, b = line.split(",")
    a = elf_assignment(a)
    b = elf_assignment(b)
    if a.intersection(b):
        total += 1

print(total)

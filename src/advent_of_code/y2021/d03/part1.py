#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys
from enum import Enum

total = 0
bits = Counter()

for line in map(lambda x: x.strip(), fileinput.input()):
    total += 1
    for i, bit in enumerate(line):
        if bit == "1":
            bits[i] += 1
    # print(bits)

gamma = 0
epsilon = 0
for i, count in bits.items():
    x = 1 << (len(bits) - i - 1)
    print(i, count, bin(x))
    gamma |= x if count > total // 2 else 0
    epsilon |= 0 if count > total // 2 else x

print(gamma, "*", epsilon, "=", gamma * epsilon)

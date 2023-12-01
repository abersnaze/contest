#!python3

import sys
import re

content = sys.stdin.readlines()

total = 0
yeses = set()
for line in content:
    if line == "\n":
        print(yeses)
        total += len(yeses)
        yeses = set()
    yeses = yeses.union(line.strip())

total += len(yeses)
print(total)

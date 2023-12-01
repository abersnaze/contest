#!python3

import sys
import re

content = sys.stdin.readlines()

total = 0
yeses = None
for line in content:
    if line == "\n":
        print(yeses)
        total += len(yeses)
        yeses = None
    else:
        if yeses == None:
            yeses = set(line.strip())
        else:
            yeses = yeses.intersection(line.strip())

total += len(yeses)
print(total)

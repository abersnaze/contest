#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys

previous = None
decrease = 0
for line in map(lambda x: x.strip(), fileinput.input()):
    if previous:
        if int(line) - previous > 0:
            decrease += 1
    print(line, previous, decrease)
    previous = int(line)

print(decrease)

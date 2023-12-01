#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys

window = []
previous = None
decrease = 0
for line in map(lambda x: x.strip(), fileinput.input()):
    x = int(line)
    if len(window) == 3:
        window.pop(0)
    window.append(x)
    curr = sum(window)
    if len(window) == 3:
        if previous:
            if curr - previous > 0:
                decrease += 1
        print(window, curr, previous, decrease)
        previous = curr

print(decrease)

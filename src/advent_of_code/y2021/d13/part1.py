#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

dots = {}
folds = []

lines = map(lambda x: x.strip(), fileinput.input())

dot_mode = True
for line in lines:
    if dot_mode:
        if line:
            x, y = line.split(",")
            dots[(int(x), int(y))] = True
        else:
            dot_mode = False
    else:
        dir, dist = re.match("fold along (.)=(\d+)", line).groups()
        folds.append((dir, int(dist)))


def dump(dots):
    w = max(map(lambda c: c[0], dots.keys())) + 1
    h = max(map(lambda c: c[1], dots.keys())) + 1
    print(w, h)
    for y in range(h):
        for x in range(w):
            if (x, y) in dots:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print(len(dots))


def fold(dots, dir, dist):
    print(dir, dist)
    if dir == "x":
        return {(x if x < dist else dist - (x - dist), y): True for x, y in dots}
    else:
        return {(x, y if y < dist else dist - (y - dist)): True for x, y in dots}


for dir, dist in [folds[0]]:
    dump(dots)
    dots = fold(dots, dir, dist)
dump(dots)

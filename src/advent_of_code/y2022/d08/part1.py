#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

lines = map(lambda x: x.strip(), fileinput.input())

trees = {}
for y, line in enumerate(lines):
    for x, cover in enumerate(line):
        trees[(x, y)] = int(cover)
    w = x + 1
h = y + 1

visible = defaultdict(lambda: False)


def print_map(m, w, h):
    print()
    for y in range(0, h):
        for x in range(0, w):
            v = m[(x, y)]
            if type(v) == bool:
                print("#" if v else ".", end="")
            else:
                print(v, end="")
        print()


print_map(trees, w, h)
print_map(visible, w, h)

# from top
for x in range(w):
    tallest = -1
    for y in range(h):
        if tallest < trees[(x, y)]:
            visible[(x, y)] = True
            tallest = trees[(x, y)]
print_map(visible, w, h)

# from bottom
for x in range(w):
    tallest = -1
    for y in range(h - 1, 0, -1):
        if tallest < trees[(x, y)]:
            visible[(x, y)] = True
            tallest = trees[(x, y)]
print_map(visible, w, h)

# from left
for y in range(h):
    tallest = -1
    for x in range(w):
        if tallest < trees[(x, y)]:
            visible[(x, y)] = True
            tallest = trees[(x, y)]
print_map(visible, w, h)

# from right
for y in range(h):
    tallest = -1
    for x in range(w - 1, 0, -1):
        if tallest < trees[(x, y)]:
            visible[(x, y)] = True
            tallest = trees[(x, y)]
print_map(visible, w, h)

print(sum(map(lambda v: 1 if v else 0, visible.values())))

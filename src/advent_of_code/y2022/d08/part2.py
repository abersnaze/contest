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


def score_dir(x, y, dx, dy, size):
    next_p = (x + dx, y + dy)
    if next_p not in trees:
        return 0
    if trees[next_p] >= size:
        return 1
    return score_dir(*next_p, dx, dy, size) + 1


def score(p):
    size = trees[p]
    total = 1
    total *= score_dir(*p, -1, 0, size)
    total *= score_dir(*p, +1, 0, size)
    total *= score_dir(*p, 0, -1, size)
    total *= score_dir(*p, 0, +1, size)
    return total


print(max(map(score, visible.keys())))

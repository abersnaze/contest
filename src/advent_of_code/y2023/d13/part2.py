#!/usr/bin/env python3

from collections import Counter, defaultdict
from fileinput import input
from functools import cmp_to_key
from itertools import count, product
from math import ceil, floor, inf, prod, sqrt
from common.space import Space, adjacent4


def ingest(files=None):
    space = Space(".")
    ids = count()
    next(ids)
    rows = set()
    cols = set()
    for y, line in enumerate(input(files)):
        for x, char in enumerate(line.strip()):
            if char == ".":
                continue
            space[(x, y)] = next(ids)
            rows.add(y)
            cols.add(x)
    print(space)
    return space, rows, cols


def process(space, rows, cols):
    return distances(expand(space, rows, cols))


def expand(space, rows, cols):
    expasion = 1000000 - 1
    dx = 0
    expanded = Space(".")
    for x in space.range(0):
        if x not in cols:
            dx += expasion
        dy = 0
        for y in space.range(1):
            if y not in rows:
                dy += expasion
            if (x, y) in space:
                expanded[(x + dx, y + dy)] = space[(x, y)]
    # print(expanded)
    return expanded


def distances(space):
    dists = {}
    points = sorted(space.points.items(), key=lambda x: x[1])
    for a, b in product(points, points):
        if a[1] >= b[1]:
            continue
        dist = abs(a[0][0] - b[0][0]) + abs(a[0][1] - b[0][1])
        dists[(a[1], b[1])] = dist
    return sum(dists.values())


if __name__ == "__main__":
    print(process(*ingest()))

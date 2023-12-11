#!/usr/bin/env python3

from collections import Counter, defaultdict
from fileinput import input
from functools import cmp_to_key
from math import ceil, floor, inf, prod, sqrt
from common.space import Space, adjacent4


def ingest(files=None):
    start = None
    space = Space(".")
    for y, line in enumerate(input(files)):
        for x, char in enumerate(line.strip()):
            if char == "S":
                start = (x, y)
            space[(x, y)] = char
    return start, space


def process(start, space):
    print(space)
    dist = Space(
        inf, to_str=lambda x: hex(x)[2:] if x != inf else ".", dim_range=space.dim_range
    )
    dist[start] = 0
    points = [start]
    while points:
        # print(dist)
        p = points.pop()
        value = dist[p]
        n, e, s, w = adjacent4(p)
        if space[n] in ("|", "F", "7") and space[p] in ("S", "|", "L", "J"):
            if dist[n] > value + 1:
                dist[n] = value + 1
                points.append(n)
        if space[e] in ("-", "J", "7") and space[p] in ("S", "-", "F", "L"):
            if dist[e] > value + 1:
                dist[e] = value + 1
                points.append(e)
        if space[s] in ("|", "L", "J") and space[p] in ("S", "|", "F", "7"):
            if dist[s] > value + 1:
                dist[s] = value + 1
                points.append(s)
        if space[w] in ("-", "F", "L") and space[p] in ("S", "-", "J", "7"):
            if dist[w] > value + 1:
                dist[w] = value + 1
                points.append(w)

    return max(dist.points.values())


if __name__ == "__main__":
    print(process(*ingest()))

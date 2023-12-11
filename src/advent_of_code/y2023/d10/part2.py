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
    print(space)
    return start, space


def spread(start):
    return (start[0] * 2 + 1, start[1] * 2 + 1)


def mid(a, b):
    return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)


def process(start, space):
    print(space)
    dist = Space(inf, to_str=lambda x: str(x)[-1] if x != inf else ".")
    dist[spread(start)] = 0
    points = [start]
    while points:
        # print(dist)
        p = points.pop()
        value = dist[spread(p)]
        n, e, s, w = adjacent4(p)
        if space[n] in ("|", "F", "7") and space[p] in ("S", "|", "L", "J"):
            if dist[spread(n)] > value + 1:
                dist[mid(spread(n), spread(p))] = value
                dist[spread(n)] = value + 1
                points.append(n)
        if space[e] in ("-", "J", "7") and space[p] in ("S", "-", "F", "L"):
            if dist[spread(e)] > value + 1:
                dist[mid(spread(e), spread(p))] = value
                dist[spread(e)] = value + 1
                points.append(e)
        if space[s] in ("|", "L", "J") and space[p] in ("S", "|", "F", "7"):
            if dist[spread(s)] > value + 1:
                dist[mid(spread(s), spread(p))] = value
                dist[spread(s)] = value + 1
                points.append(s)
        if space[w] in ("-", "F", "L") and space[p] in ("S", "-", "J", "7"):
            if dist[spread(w)] > value + 1:
                dist[mid(spread(w), spread(p))] = value
                dist[spread(w)] = value + 1
                points.append(w)

    print(dist)
    return count_inside(dist, space.copy())


def count_inside(dist, space):
    space = Space(" ")
    count = 0
    for y in dist.range(1):
        state = "outside"
        for x in dist.range(0):
            if dist[(x, y)] != inf:
                space[(x, y)] = "#"
                if state in "outside":
                    state = "enter"
                if state == "inside":
                    state = "exit"
                continue
            else:
                if state == "enter":
                    state = "inside"
                elif state == "exit":
                    state = "outside"

                if state == "inside":
                    count += 1
                    space[(x, y)] = "I"
                else:
                    space[(x, y)] = "O"
    print(space)
    return count


if __name__ == "__main__":
    print(process(*ingest()))

#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product, repeat
import math
from functools import reduce


def dist(ax, ay, bx, by):
    if ax < bx:
        ax, bx = bx, ax
    if ay < by:
        ay, by = by, ay
    return (ax - bx) + (ay - by)


lines = list(map(lambda x: x.strip(), fileinput.input()))
row, _min, _max = map(int, lines.pop(0).split(" "))
print("params", row, _min, _max)
sensors = []
for line in lines:
    if line == "":
        continue
    _, _, sx, sy, _, _, _, _, bx, by = line.split(" ")
    # sensors.append(int(sx))
    sx, sy, bx, by = int(sx[2:-1]), int(sy[2:-1]), int(bx[2:-1]), int(by[2:])
    sensor = (sx, sy, dist(sx, sy, bx, by))
    print("sensor", sensor)
    sensors.append(sensor)


def splice(range_start, range_end, xmin, xmax):
    # if it doesn't overlap
    if range_end < xmin:
        yield (range_start, range_end)
        return
    if xmax < range_start:
        yield (range_start, range_end)
        return
    # if it does
    if range_start < xmin and xmin < range_end:
        yield (range_start, xmin)
    if range_start < xmax and xmax < range_end:
        yield (xmax, range_end)


def not_present(ry):
    alloweds = [(-math.inf, math.inf)]
    for sx, sy, dst in sensors:
        size = dst - (sy - ry if sy > ry else ry - sy)
        if size < 1:
            continue
        rx_min = sx - size
        rx_max = sx + size + 1
        print("gap", rx_min, rx_max)

        new_alloweds = []
        for allowed in alloweds:
            new_alloweds.extend(splice(*allowed, rx_min, rx_max))
        alloweds = new_alloweds
        print(alloweds)

    # no invert the allowed into not allowed
    not_allowed = 0
    prev = None
    for allowed in alloweds:
        if prev:
            not_allowed += allowed[0] - prev[1] - 1
        prev = allowed
    return not_allowed


print(row)
print(not_present(row))

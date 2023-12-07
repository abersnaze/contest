#!/usr/bin/env python3

from collections import defaultdict
from fileinput import input
from math import ceil, floor, prod, sqrt

from common.space import Dir, Space, adjencent8


def ingest(files=None):
    lines = input(files)
    times = map(int, next(lines).strip().split(":")[1].split())
    dists = map(int, next(lines).strip().split(":")[1].split())

    return list(zip(times, dists))


def process(races):
    total = []
    for race in races:
        total.append(margin(*race))
    return prod(total)


def margin(time, dist):
    # - x**2 + time*x - dist = 0
    foo = sqrt(time**2 - 4 * dist)
    min_z, max_z = (-time + foo) / 2 * -1, (-time - foo) / 2 * -1
    next_min = floor(min_z) + 1
    next_max = ceil(max_z) - 1
    opts = next_max - next_min + 1
    return opts


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))

#!/usr/bin/env python3

from collections import Counter, defaultdict
from fileinput import input
from functools import cmp_to_key
from itertools import count, product
import json
from math import ceil, floor, inf, prod, sqrt
import re
from common.space import Space, Dir


def ingest(files=None):
    mirrors = []
    mirror = Space()
    y = 0
    for line in input(files):
        if line.strip() == "":
            mirrors.append(mirror)
            mirror = Space()
            y = 0
            continue
        for x, c in enumerate(line.strip()):
            if c != ".":
                mirror[(x, y)] = c
        y += 1
    if len(mirror) > 0:
        mirrors.append(mirror)

    return mirrors


def process(mirrors):
    nums = []
    for mirror in mirrors:
        if rx := find_reflection(mirror):
            nums.append(rx)
        elif ry := find_reflection(mirror.transpose()):
            nums.append(ry * 100)
        else:
            print("No reflection found")
            print(mirror)
    return sum(nums)

# 18589
# 23887
# 33681
# 31278

def find_reflection(mirror):
    xs = list(mirror.range(0))
    x_min, x_max = xs[0], xs[-1]
    for r in range(1, x_max):
        pass
        for x, y in mirror.keys():
            rx = r + (r - x) + 1
            if x < r or rx not in xs:
                continue
            if (rx, y) not in mirror:
                break
        else:
            return r + 1
    return 0


# 0123456
# 1.      r=1
# 32..    r=2
# 543...  r=3
# _654... r=4
# ___65.. r=5
# _____66 r=6


if __name__ == "__main__":
    print(process(ingest()))

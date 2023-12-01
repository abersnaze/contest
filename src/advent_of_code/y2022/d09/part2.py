#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product
import math

lines = map(lambda x: x.strip(), fileinput.input())


class Dir(Enum):
    U = (0, -1)
    D = (0, +1)
    L = (-1, 0)
    R = (+1, 0)


rope = [(0, 0) for i in range(10)]


def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


visit = {}


def follow(head, tail):
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    mx = abs(dx)  # magnitude
    my = abs(dy)
    dx = sign(dx)  # sign
    dy = sign(dy)
    if math.sqrt(mx * mx + my * my) >= 2:  # more than two steps away
        mx = min(mx, 1)  # clamp it to 0..1 so diagonals work
        my = min(my, 1)
        if mx > my:
            tail = (tail[0] + dx, tail[1])
        elif mx < my:
            tail = (tail[0], tail[1] + dy)
        else:
            tail = (tail[0] + dx, tail[1] + dy)
    return tail


def dump():
    return
    w = 25
    for y in range(-w, w):
        for x in range(-w, w):
            ch = "."
            if x == 0 and y == 0:
                ch = "s"
            if (x, y) in visit:
                ch = "#"
            if (x, y) in rope:
                ch = rope.index((x, y))

            print(ch, end="")
        print()
    print()


for line in lines:
    d, c = line.split(" ")
    dir = Dir[d]
    count = int(c)
    for i in range(count):
        dump()
        rope[0] = (rope[0][0] + dir.value[0], rope[0][1] + dir.value[1])
        for i in range(len(rope) - 1):
            rope[i + 1] = follow(rope[i], rope[i + 1])
        visit[rope[-1]] = 1

print(visit)
print(sum(visit.values()))

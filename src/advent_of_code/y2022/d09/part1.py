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


head = (0, 0)
tail = (0, 0)


def sign(x):
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


visit = {}


def step(dir: Dir):
    global head, tail
    head = (head[0] + dir.value[0], head[1] + dir.value[1])
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    mx = abs(dx)
    my = abs(dy)
    dx = sign(dx)
    dy = sign(dy)
    if math.sqrt(mx * mx + my * my) >= 2:
        mx = min(mx, 1)
        my = min(my, 1)
        if mx > my:
            tail = (tail[0] + dx, tail[1])
        elif mx < my:
            tail = (tail[0], tail[1] + dy)
        else:
            tail = (tail[0] + dx, tail[1] + dy)
    visit[tail] = 1


def dump():
    for y in range(-5, 5):
        for x in range(-5, 5):
            ch = "."
            if x == 0 and y == 0:
                ch = "s"
            if (x, y) in visit:
                ch = "#"
            if head == (x, y):
                ch = "H"
                if tail == (x, y):
                    ch = "B"
            elif tail == (x, y):
                ch = "T"

            print(ch, end="")
        print()
    print()


for line in lines:
    d, c = line.split(" ")
    dir = Dir[d]
    count = int(c)
    for i in range(count):
        dump()
        step(dir)

print(visit)
print(sum(visit.values()))

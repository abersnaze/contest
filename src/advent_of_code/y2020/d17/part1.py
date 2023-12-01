#!python3

import fileinput
import re
from collections import defaultdict
import sys

ACTIVE = "#"
INACTIVE = "."
space = defaultdict(lambda: INACTIVE)

for y, line in enumerate(map(lambda x: x.strip(), fileinput.input())):
    for x, point in enumerate(line):
        if point == "#":
            space[(x, y, 0)] = point


def write(s):
    count = 0
    active = s.keys()
    minx = min([p[0] for p in active])
    maxx = max([p[0] for p in active])
    miny = min([p[1] for p in active])
    maxy = max([p[1] for p in active])
    minz = min([p[2] for p in active])
    maxz = max([p[2] for p in active])
    for z in range(minz, maxz + 1):
        sys.stdout.write(f"z={z}\n")
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                v = s[(x, y, z)]
                if v == ACTIVE:
                    count += 1
                sys.stdout.write(v)
            sys.stdout.write("\n")
        sys.stdout.write("\n")
    sys.stdout.write(f"count = {count}\n")
    return count


def all(s):
    active = map(lambda p: p[0], filter(lambda p: p[1] == ACTIVE, s.items()))
    return set(
        [
            (x + dx, y + dy, z + dz)
            for x, y, z in active
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            for dz in [-1, 0, 1]
        ]
    )


def adjacent(p):
    x = set(
        [
            (p[0] + dx, p[1] + dy, p[2] + dz)
            for dx in [-1, 0, 1]
            for dy in [-1, 0, 1]
            for dz in [-1, 0, 1]
        ]
    )
    x.remove(p)
    assert len(x) == 26
    return x


write(space)

round = 0
while round < 6:
    next_space = defaultdict(lambda: INACTIVE)
    for p in all(space):
        count = list(adjacent(p))
        count = list(map(lambda a: space[a], count))
        # print("\tadj cont", count)
        count = list(filter(lambda v: v == ACTIVE, count))
        # print("\tadj act", count)
        count = len(count)
        # print("\tadj count", count)
        sys.stdout.write(f"{p}, {space[p]}, {count}")
        if space[p] == ACTIVE:
            if count == 2 or count == 3:
                next_space[p] = ACTIVE
                sys.stdout.write(" keep\n")
            else:
                next_space[p] = INACTIVE
                sys.stdout.write(" off\n")
        else:
            if count == 3:
                next_space[p] = ACTIVE
                sys.stdout.write(" on\n")
            else:
                sys.stdout.write(" skip\n")
        sys.stdout.flush()

    space = next_space

    write(space)
    round += 1

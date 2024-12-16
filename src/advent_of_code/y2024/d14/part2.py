from collections import defaultdict
from math import prod
import math
from common.input import input, compile
from common.space import Space, adjacent4
from collections import Counter


def to_str(value):
    if value == ".":
        return "."
    return "@"


_floor = Space(to_str=to_str)
floor_pattern = compile("<int>,<int>")
robot_pattern = compile("p=<int>,<int> v=<int>,<int>")

robots = []
lines = input()
fx, fy = floor_pattern(next(lines))
for r, line in enumerate(lines):
    px, py, vx, vy = robot_pattern(line)
    _floor[(r, px, py)] = (vx, vy)
_floor.cover((0, 0, 0))
_floor.cover((r, fx - 1, fy - 1))

print("0")
print(_floor.project(0))


def move(floor: Space, seconds):
    next_floor = Space(to_str=to_str)
    minr, maxr = floor.minmax(0)
    minx, maxx = floor.minmax(1)
    miny, maxy = floor.minmax(2)
    for (r, x, y), (vx, vy) in floor.items():
        next_x = ((x + vx * seconds) - minx) % (maxx - minx + 1) + minx
        next_y = ((y + vy * seconds) - miny) % (maxy - miny + 1) + miny
        next_floor[(r, next_x, next_y)] = (vx, vy)
    next_floor.cover((minr, minx, miny))
    next_floor.cover((maxr, maxx, maxy))
    return next_floor


def is_tree(floor: Space):
    seen = set()
    for r, x, y in floor.keys():
        if (x, y) in seen:
            return False
        seen.add((x, y))
    return True


for i in range(1, 100000000):
    _floor = move(_floor, 1)
    if is_tree(_floor):
        print(i)
        print(_floor.project(0))
        print(i)
        pass

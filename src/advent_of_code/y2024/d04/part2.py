from common.input import input
from common.space import Dir4, Dir8, Space
import re

space = Space()
map = []
for y, line in enumerate(input()):
    map.append(line)
    for x, ch in enumerate(line):
        if ch == "A":
            space[(x, y)] = ch

print(space)


def map_get(p):
    x, y = p
    if 0 <= y < len(map) and 0 <= x < len(map[y]):
        return map[y][x]
    return '.'


def is_xmas(p):
    if map_get(p + Dir8.NW) + map_get(p + Dir8.SE) not in ("MS", "SM"):
        return False
    if map_get(p + Dir8.NE) + map_get(p + Dir8.SW) not in ("MS", "SM"):
        return False
    return True


print(len(space))
sum = 0
for p in space.keys():
    if is_xmas(p):
        print(p)
        sum += 1

print(sum)

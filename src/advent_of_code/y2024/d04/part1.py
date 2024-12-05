from common.input import input
from common.space import Space, Dir8
import re

space = Space()
map = []
for y, line in enumerate(input()):
    map.append(line)
    for x, ch in enumerate(line):
        if ch == "X":
            space[(x, y)] = ch

print(space)


def map_get(p):
    x, y = p
    if 0 <= y < len(map) and 0 <= x < len(map[y]):
        return map[y][x]
    return "."


def is_xmas(p, d):
    p += d
    if map_get(p) != "M":
        return False
    p += d
    if map_get(p) != "A":
        return False
    p += d
    if map_get(p) != "S":
        return False
    return True


print(len(space))
sum = 0
for p in space.keys():
    for d in Dir8:
        if is_xmas(p, d):
            print(p, d)
            sum += 1

print(sum)

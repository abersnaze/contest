from math import prod
from common.input import input, compile
from common.space import Space, adjacent4


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


def safety_factor(floor: Space):
    minr, maxr = floor.minmax(0)
    minx, maxx = floor.minmax(1)
    miny, maxy = floor.minmax(2)
    midx = (minx + maxx) // 2
    midy = (miny + maxy) // 2
    quad = [0, 0, 0, 0]
    for r, x, y in floor.keys():
        if x < midx:
            if y < midy:
                quad[0] += 1
            elif y > midy:
                quad[1] += 1
        elif x > midx:
            if y < midy:
                quad[2] += 1
            elif y > midy:
                quad[3] += 1
    print(quad)
    print(prod(quad))


end = move(_floor, 100)
print("100")
print(end.project(0))

safety_factor(end)

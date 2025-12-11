import regex as re
from common.input import input

lines = list(input())
ranges: list[tuple[int, int]] = []

def in_range(value: int) -> int | None:
    for idx, (rmin, rmax) in enumerate(ranges):
        if rmin <= value and value <= rmax:
            return idx
    return None

def add_range(rmin, rmax):
    if (idx := in_range(rmin)) is not None:
        rmin = min(ranges[idx][0], rmin)
        rmax = max(ranges[idx][1], rmax)
        del ranges[idx]
        add_range(rmin, rmax)
    elif (idx := in_range(rmax)) is not None:
        rmin = min(ranges[idx][0], rmin)
        rmax = max(ranges[idx][1], rmax)
        del ranges[idx]
        add_range(rmin, rmax)
    else:
        ranges.append((rmin, rmax))

while lines[0] != "":
    line = lines.pop(0)
    rmin, rmax = line.split('-')
    add_range(int(rmin), int(rmax))
lines.pop(0)

# print(ranges)

fresh_count = 0
for id in lines:
    id = int(id)
    if in_range(id) is not None:
        print("\t", id)
        fresh_count += 1

print(fresh_count)
import regex as re
from common.input import input

lines = list(input())
ranges: list[tuple[int, int]] = []

def in_range(value: int) -> int | None:
    for idx, (rmin, rmax) in enumerate(ranges):
        if rmin <= value and value <= rmax:
            return idx
    return None

def merge_range(rmin, rmax, r2: tuple[int, int]) -> tuple[int, int]:
    return (
        min(rmin, r2[0]),
        max(rmax, r2[1])
    )

def add_range(rmin, rmax):
    if (idx := in_range(rmin)) is not None:
        add_range(*merge_range(rmin, rmax, ranges.pop(idx)))
    elif (idx := in_range(rmax)) is not None:
        add_range(*merge_range(rmin, rmax, ranges.pop(idx)))
    else:
        for idx, (rmin2, rmax2) in enumerate(ranges):
            if rmin < rmin2 and rmax2 < rmax:
                add_range(*merge_range(rmin, rmax, ranges.pop(idx)))
                break
        else:
            ranges.append((rmin, rmax))

while lines[0] != "":
    line = lines.pop(0)
    rmin, rmax = line.split('-')
    add_range(int(rmin), int(rmax))
lines.pop(0)

fresh_count = 0
for rmin, rmax in ranges:
    ids = rmax - rmin + 1
    fresh_count += ids

print(fresh_count)
print(361615643045059)
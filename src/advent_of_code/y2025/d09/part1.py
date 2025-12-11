import math
from common.input import input

tiles = []
for line in input():
    x, y = line.split(",")
    tiles.append((int(x), int(y)))

largest = 0
for idx_a, (ax, ay) in enumerate(tiles):
    for bx, by in tiles[idx_a + 1 :]:
        w = abs(ax - bx) + 1
        h = abs(ay - by) + 1
        area = w * h
        if largest < area:
            largest = area

print(largest)

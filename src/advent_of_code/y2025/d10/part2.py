from common.space import Space, line
from common.input import input

s = Space()
tiles = []
prev = None
first = None
for cords in input():
    x, y = cords.split(",")
    curr = (int(x), int(y))
    if first is None:
        first = curr
    s[curr] = '#'
    if prev:
        for l in line(prev, curr):
            if l not in s:
                s[l] = 'X'
    prev = curr
for l in line(prev, first):
    if l not in s:
        s[l] = 'X'

print(s)

# fill inside.
for y in range(*s.minmax(1)):
    inside = False
    for x in range(*s.minmax(0)):
        if (x,y) in s and (x+1, y) not in s:
            inside = not inside
        elif inside:
            s[(x,y)] = '%'

print(s)

largest = 0
for idx_a, (ax, ay) in enumerate(tiles):
    for bx, by in tiles[idx_a + 1 :]:
        w = abs(ax - bx) + 1
        h = abs(ay - by) + 1
        area = w * h
        if largest < area:
            largest = area
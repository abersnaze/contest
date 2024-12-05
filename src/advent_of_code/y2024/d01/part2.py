from fileinput import input
from collections import Counter

locs = []

for line in input():
    line.strip()
    locs.append(tuple(map(int, line.split())))

lefts = sorted(locs, key=lambda l: l[0])
rights = sorted(locs, key=lambda l: l[1])
right_count = Counter(map(lambda l: l[1], rights))

sum = 0
for l, r in zip(lefts, rights):
    diff = l[0] * right_count[l[0]]
    sum += diff

print("sum", sum)
assert sum == 23177084

from fileinput import input

locs = []

for line in input():
    line.strip()
    locs.append(tuple(map(int, line.split())))

lefts = sorted(locs, key=lambda l: l[0])
rights = sorted(locs, key=lambda l: l[1])

sum = 0
for l, r in zip(lefts, rights):
    diff = abs(l[0] - r[1])
    sum += diff

print("sum", sum)
assert sum == 2057374
